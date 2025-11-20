from pathlib import Path
import shutil
from ..utils.paths import resource_path

def cleanup_tmp():
    tmp_dir = resource_path("data/tmp")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
