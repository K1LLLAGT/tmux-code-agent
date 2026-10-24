from pathlib import Path
def detect_runner(workspace:Path):
 if (workspace/'pytest.ini').exists() or any(workspace.glob('test_*.py')) or (workspace/'tests').exists():return ['pytest']
 if (workspace/'package.json').exists():return ['npm','test','--']
 if (workspace/'Cargo.toml').exists():return ['cargo','test']
 return None
