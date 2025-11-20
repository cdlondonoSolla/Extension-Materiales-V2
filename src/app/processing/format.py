import pandas as pd

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    # Ejemplo: limpiar espacios y convertir a mayúsculas
    if "Material" in df:
        df["Material"] = df["Material"].astype(str).str.strip().str.upper()
    if "Centro" in df:
        df["Centro"] = df["Centro"].astype(str).str.strip()
    return df