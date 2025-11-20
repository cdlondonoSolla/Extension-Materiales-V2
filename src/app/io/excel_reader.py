import pandas as pd
from typing import Dict, Any
from ..utils.paths import resource_path
from ..utils.exceptions import TemplateNotFoundError, TemplateInvalidError

def load_template(cfg: Dict[str, Any]) -> pd.DataFrame:
    tpl_path = resource_path(cfg["excel"]["template_relative"])
    if not tpl_path.exists():
        raise TemplateNotFoundError(f"Plantilla no encontrada: {tpl_path}")

    try:
        df = pd.read_excel(
            tpl_path,
            sheet_name=cfg["excel"]["sheet_name"],
            dtype=cfg["excel"]["dtype"],
            parse_dates=cfg["excel"]["parse_dates"],
            engine="openpyxl"
        )
    except Exception as e:
        raise TemplateInvalidError(f"Error leyendo Excel: {e}")

    missing = [c for c in cfg["excel"]["required_columns"] if c not in df.columns]
    if missing:
        raise TemplateInvalidError(f"Faltan columnas requeridas: {missing}")

    return df