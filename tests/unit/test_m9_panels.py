from pathlib import Path
def test_m9_assets():
 s=Path('frontend/src/components/v1_panels.js').read_text();assert all(x in s for x in ('Files','Editor','Git','Activity','Settings','tablet'))
