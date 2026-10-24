from redact.env import filter_environment, is_safe_name
from redact.scrub import collect_secret_values, scrub_text


def test_environment_filter_excludes_secret_names() -> None:
    source = {
        "HOME": "/home/u",
        "PATH": "/bin",
        "LANG": "en_US.UTF-8",
        "API_TOKEN": "do-not-copy",
        "DB_PASSWORD": "also-secret",
        "UNRELATED": "drop-me",
    }
    result = filter_environment(source)
    assert result == {"HOME": "/home/u", "LANG": "en_US.UTF-8", "PATH": "/bin"}
    assert not is_safe_name("API_TOKEN")


def test_scrub_text_removes_known_and_structured_secrets() -> None:
    text = "token=swordfish Authorization: Bearer abc.def.ghi"
    scrubbed = scrub_text(text, secret_values=("swordfish",))
    assert "swordfish" not in scrubbed
    assert "abc.def.ghi" not in scrubbed


def test_collect_secret_values_uses_secret_names() -> None:
    assert collect_secret_values({"HOME": "/h", "ACCESS_TOKEN": "x"}) == ("x",)
