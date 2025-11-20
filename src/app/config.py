import json
from typing import Dict, Any
from .utils.paths import resource_path
from .utils.exceptions import ConfigError

def load_config() -> Dict[str, Any]:
    cfg_path = resource_path("config/config.json")
    if not cfg_path.exists():
        raise ConfigError(f"No se encontró config.json en {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg