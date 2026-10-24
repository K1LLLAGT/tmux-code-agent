from pathlib import Path
def test_all_section30_areas_represented():
 s=Path('frontend/src/components/v1_panels.js').read_text();assert all(x in s for x in ['Agent','Terminal','Files','Editor','Git','Activity','Settings'])
