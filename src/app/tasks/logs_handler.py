from pathlib import Path
import shutil
from datetime import datetime
from ..utils.paths import logs_dir

def archive_logs():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = logs_dir() / timestamp
    dest.mkdir(parents=True, exist_ok=True)
    for file in logs_dir().glob("*.*"):
        shutil.move(str(file), dest)