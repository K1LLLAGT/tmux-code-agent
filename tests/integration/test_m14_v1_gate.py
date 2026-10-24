from pathlib import Path
def test_review_checklist_exists():assert 'Threat-model walkthrough' in Path('docs/review/threat-model-checklist.md').read_text()
