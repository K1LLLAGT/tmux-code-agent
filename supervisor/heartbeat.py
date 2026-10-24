from datetime import datetime, timezone
from pathlib import Path

def write_heartbeat(path:Path)->str:
 value=datetime.now(timezone.utc).isoformat(); path.write_text(value+"\n"); return value
