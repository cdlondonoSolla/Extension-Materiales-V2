import pandas as pd
import numpy as np
from typing import Dict, Any
from ..utils.paths import resource_path, logs_dir

def generate_txt(cfg: Dict[str, Any]) -> str:
    # Rutas seguras
    tmp_path = resource_path("data/tmp/tmp.xlsx")
    solicitud_path = resource_path(cfg["excel"]["template_relative"])
    out_path = logs_dir() / cfg["output"]["txt_filename"]

    # Leer archivos
    df_tmp = pd.read_excel(tmp_path, dtype=str, engine="openpyxl")
    df_solicitud = pd.read_excel(solicitud_path, dtype=str, engine="openpyxl")

    # Renombrar columna clave
    df_solicitud = df_solicitud.rename(columns={"Codigo": "Material"})
    df_solicitud["Material"] = df_solicitud["Material"].astype(str)
    df_tmp["Material"] = df_tmp["Material"].astype(str)

    # Merge
    df_merged = pd.merge(df_solicitud[["Material"]], df_tmp, on="Material", how="left")
    df_final_txt = df_merged.dropna(subset=["Ramo"])  # Ajusta columna clave según tu lógica

    # Log de no encontrados
    no_encontrados = df_merged[df_merged["Ramo"].isna()][["Material"]]
    no_encontrados.to_csv(logs_dir() / "log_materiales_no_encontrados.csv", index=False, encoding="utf-8")

    # Columnas adicionales
    vistas_cols = [
        "Datos básicos 1","Clasificación","ventas 1","ventas 2","Ventas Gnal","Texto comercial",
        "Texto comercial expo","Compras","Texto comercial impo","Texto pedido compras",
        "Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4","Pronostico",
        "Preparación trabajo","Almacenamiento","calidad","Contabilidad","coste"
    ]
    for col in vistas_cols:
        if col not in df_final_txt.columns:
            df_final_txt[col] = np.nan

    # Ordenar columnas
    existing_cols = [c for c in df_final_txt.columns if c not in vistas_cols]
    df_final_txt = df_final_txt[vistas_cols + existing_cols]

    # Rellenar con 'X'
    for col in ["Compras","Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4","Almacenamiento","Contabilidad","coste"]:
        if col in df_final_txt.columns:
            df_final_txt[col] = "X"

    # Actualizar columnas específicas
    df_final_txt["Centro"] = df_solicitud["Centro"]
    df_final_txt["Almacén"] = df_solicitud["Almacen"]
    df_final_txt["Centro de beneficio.1"] = df_solicitud["CentroBeneficio"]
    df_final_txt["Centro de beneficio"] = pd.NA
    df_final_txt["Precio variable"] = pd.NA
    df_final_txt["Precio estándar"] = pd.NA
    df_final_txt["Stat.mat.específ.ce."] = pd.NA

    # Eliminar columnas no deseadas
    for col in ["Grupo tolerancia CW","Co-producto"]:
        if col in df_final_txt.columns:
            df_final_txt.drop(columns=col, inplace=True)

    # # Completar Almacén si está vacío
    # mask = df_final_txt["Almacén"].isna()
    # df_final_txt.loc[mask,"Almacén"] = df_final_txt.loc[mask,"Centro"].str.strip().str[:3] + "1"

    # Normalizar
    df_final_txt["Centro"] = df_final_txt["Centro"].str.upper()
    df_final_txt["Almacén"] = df_final_txt["Almacén"].str.upper()

    # Vaciar columnas de vista para centros específicos
    centros_objetivo = {"1400","B400","A400"}
    columnas_a_vaciar = ["Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4"]
    df_final_txt.loc[df_final_txt["Centro"].isin(centros_objetivo), columnas_a_vaciar] = pd.NA

    #print(df_final_txt.columns.tolist())
    
    # Vaciar columnas de datos para centros específicos
    columnas_a_vaciar = [
            'Grupo planif.nec.',
            'Caract.planif.nec.',
            'Punto de pedido',
            'Planif.necesidades',
            'Tam.lote planif.nec.',
            'Tamaño lote mínimo',
            'Tamaño lote máximo',
            'Tamaño lote fijo',
            'Stock máximo',
            'Rechazo conjunto (%)',
            'Valor de redondeo',
            'Clase aprovisionam.',
            'Aprovis.especial',
            'Almacén producción',
            'Toma retrograda',
            'Alm.aprov.externo',
            'Tiempo fabric.propia',
            'Plazo entrega prev.',
            'Clave de horizonte',
            'Stock de seguridad',
            'Perfil de cobertura',
            'Grupo estrategia planificación',
            'Modo de compensación',
            'IntvCompens.atrás',
            'IntCompens.adelante',
            'Verif.disponibilidad.1',
            'TiempoGlobalReaprov',
            'SelecciónAltern',
            'Individual/Colectivo',
            'Fabricación repetit.',
            'Perfil fabr.repet.'


    ]
    df_final_txt.loc[df_final_txt["Centro"].isin(centros_objetivo), columnas_a_vaciar] = pd.NA

    # Guardar TXT
    df_final_txt.to_csv(out_path, sep="\t", index=False, header=False, encoding="utf-8-sig")
    return str(out_path)
