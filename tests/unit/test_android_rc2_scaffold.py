from pathlib import Path

def test_android_rc2_manifest_and_gradle():
    root=Path(__file__).resolve().parents[2]
    manifest=(root/'android/app/src/main/AndroidManifest.xml').read_text()
    gradle=(root/'android/app/build.gradle.kts').read_text()
    launcher=(root/'android/app/src/main/java/io/github/g19479574996t/tmuxcodeagent/TermuxLauncher.kt').read_text()
    assert 'com.termux.permission.RUN_COMMAND' in manifest
    assert '<package android:name="com.termux"' in manifest
    assert 'applicationId = "io.github.g19479574996t.tmuxcodeagent"' in gradle
    assert 'versionName = "1.0.0-rc2"' in gradle
    assert 'versionCode = 10002' in gradle
    assert 'com.termux.app.RunCommandService' not in launcher  # contract centralizes magic strings
    assert 'TermuxContract.RUN_COMMAND_SERVICE' in launcher
