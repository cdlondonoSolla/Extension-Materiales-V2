from pathlib import Path
import sys, logging


def app_root() -> Path:
    if getattr(sys, 'frozen', False):
        root = Path(sys.executable).parent
    else:
        root = Path(__file__).resolve().parents[3]
    logging.getLogger(__name__).info(f"[paths] app_root = {root}")
    return root


def resource_path(relative: str) -> Path:
    return app_root() / relative

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def logs_dir() -> Path:
    d = app_root() / "logs"
    ensure_dir(d)
    return d