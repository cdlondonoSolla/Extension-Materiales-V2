import pandas as pd
import numpy as np
from typing import Dict, Any
from ..utils.paths import resource_path, logs_dir

EXPECTED_COLS = [
    "Datos básicos 1","Clasificación","ventas 1","ventas 2","Ventas Gnal","Texto comercial",
    "Texto comercial expo","Compras","Texto comercial impo","Texto pedido compras",
    "Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4","Pronostico",
    "Preparación trabajo","Almacenamiento","calidad","Contabilidad","coste",
    "Material","Ramo","Tipo de material","Centro","Almacén","Organización ventas","Canal distribución",
    "Descripción material","Unidad medida base","Grupo de artículos","Nº antiguo material","Sector",
    "Peso bruto","Unidad de peso","Peso neto","Volumen","Unidad de volumen","Tamaño/Dimensión",
    "Código EAN/UPC","Gr.materiales ME","Grupo artíc. externo","Laboratorio/oficina","Texto datos basicos",
    "Categoría de la clase","Caracteristicas","Un.medida venta","Grupo un.medida","StatMat todas CadDis",
    "Validez de","Stat.esp.caden.distr","Validez de.1","Centro suministrador","Derecho a descuento",
    "Clasificación fiscal","Cantidad de rechazo","Cant.mínima entrega","Cantidad mínima partición",
    "Grupo estadísticas","Grupo de materiales","Grupo de rappels","Gr.imputación mat.","Gpo.tipos pos.gral.",
    "Grupo tipos posición","Material precio","Jerarquía productos","Grupo de comisiones","Grupo materiales 1",
    "Grupo de material 2","Grupo de material 3","Grupo de material 4","Grupo de material 5",
    "Verif.disponibilidad","Grupo de transporte","Grupo de carga","Tiempo preparación","Tiempo tratamiento",
    "Cantidad base","Tipo mat.embalaje","Stocks neg.centro","Centro de beneficio","Perfil número serie",
    "Perfil distrib.","Nivel serialización","Texto de comercial","Unidad medida pedido","UM de pedido variable",
    "Grupo de compras","Ident.impuest.mat.","Grp.porte mat.","Ind.pedido autom.","Requ.gest.lotes",
    "Clave-valores-comp","Tmpo.tratamiento EM","Perfil piezas fabric.","Nº mcía./Nº cód.imp.",
    "Texto Pedido de Compras","Grupo planif.nec.","Caract.planif.nec.","Punto de pedido","Planif.necesidades",
    "Tam.lote planif.nec.","Tamaño lote mínimo","Tamaño lote máximo","Tamaño lote fijo","Stock máximo",
    "Rechazo conjunto (%)","Valor de redondeo","Clase aprovisionam.","Aprovis.especial","Almacén producción",
    "Toma retrograda","Alm.aprov.externo","Tiempo fabric.propia","Plazo entrega prev.","Clave de horizonte",
    "Stock de seguridad","Perfil de cobertura","Grupo estrategia planificación","Modo de compensación",
    "IntvCompens.atrás","IntCompens.adelante","Verif.disponibilidad.1","TiempoGlobalReaprov","SelecciónAltern",
    "Individual/Colectivo","Fabricación repetit.","Perfil fabr.repet.","Modelo de pronóstico","Indicador de período",
    "Periodos del pasado","Períodos pronóstico","Inicialización","Límite de alarma","Selección de modelo",
    "Proced.selec.modelo","Alis.valor tendencia","Alisamiento DMA","UdM fabricación","Unidad med.salida",
    "Resp.ctrl.producción","Perf.ctrl.fabric.","Grupo de materiales.1","Tol.entrg.incompleta","Tol.exc.suministro",
    "Exceso sumin.ilim.","Tiempo preparación.1","Tiempo tratamiento.1","Cantidad base.1","Ubicación",
    "Tmpo.mín.durac.rest.","Dur.total conserv.","Cond.almacenaje","Categoría valoración","Liquidación LM: Control",
    "Control de precios","Precio variable","Precio estándar","Tipo de valoración","Cantidad base.2","Origen material",
    "C/estruct.cuant.","Grupo gastos gral.","Clave de desviación","Stat.mat.específ.ce.","Válido de",
    "Centro de beneficio.1","Alternativa LMat","Utilizac.lista mat.","Grupo de orígenes","Aprov.esp.CC",
    "Entrada lotes","No efectuar CC","Medio","Cont.grupo HRuta","Indicador ABC"
]


def generate_txt(cfg: Dict[str, Any]) -> str:
    tmp_path = resource_path("data/tmp/tmp.xlsx")
    solicitud_path = resource_path(cfg["excel"]["template_relative"])

    if not solicitud_path.exists():
        raise FileNotFoundError(
            f"No se encontró la plantilla en {solicitud_path}. Colócala en data/templates/"
        )

    out_path = logs_dir() / cfg["output"]["txt_filename"]

    df_tmp = pd.read_excel(tmp_path, dtype=str, engine="openpyxl")
    df_solicitud = pd.read_excel(solicitud_path, dtype=str, engine="openpyxl")

    # Renombrar columnas (solicitud)
    df_solicitud = df_solicitud.rename(columns={
        "Título": "Codigo",
        "CentroExtender": "Centro",
        "Almacen": "Almacen",
        "CentroModelo": "CentroModelo",
        "CentroBeneficio": "CentroBeneficio",
        "ID": "Secuencia",
        "Estado": "Estado",
        "TipoMaterial": "TipoMaterial",
        "Mensaje": "Mensaje",
        "id_axuliar": "Id_auxiliar",
    })

    # Normalización clave
    df_solicitud = df_solicitud.rename(columns={"Codigo": "Material"})
    df_solicitud["Material"] = df_solicitud["Material"].astype(str).str.strip()
    df_tmp["Material"] = df_tmp["Material"].astype(str).str.strip()

    # Filtro requerido
    if "Mensaje" not in df_solicitud.columns:
        raise KeyError("La columna 'Mensaje' no existe en df_solicitud (revisa el nombre en el Excel).")

    mask_msg = (
        df_solicitud["Mensaje"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        == "extender centro".casefold()
    )
    df_solicitud = df_solicitud.loc[mask_msg].copy()

    # Evitar duplicación por múltiples filas de tmp por Material
    if "Material" in df_tmp.columns:
        df_tmp = df_tmp.drop_duplicates(subset=["Material"], keep="first").copy()

    # Merge trayendo campos de solicitud sin romper nombres de tmp
    cols_solicitud = ["Material", "Centro", "Almacen", "CentroBeneficio", "TipoMaterial"]
    for c in cols_solicitud:
        if c not in df_solicitud.columns:
            if c == "TipoMaterial":
                df_solicitud[c] = pd.NA
            else:
                raise KeyError(f"Falta columna requerida en df_solicitud: {c}")

    df_merged = pd.merge(
        df_solicitud[cols_solicitud],
        df_tmp,
        on="Material",
        how="left",
        suffixes=("_sol", "_tmp")
    )

    # Base salida: solo encontrados por Ramo
    if "Ramo" not in df_merged.columns:
        raise KeyError("La columna 'Ramo' no existe en tmp.xlsx (df_tmp).")

    df_final_txt = df_merged.dropna(subset=["Ramo"]).copy()

    # Log de no encontrados
    no_encontrados = df_merged[df_merged["Ramo"].isna()][["Material"]]
    no_encontrados.to_csv(
        logs_dir() / "log_materiales_no_encontrados.csv",
        index=False,
        encoding="utf-8"
    )

    # Centro / Almacén / Beneficio: SIEMPRE desde solicitud
    if "Centro_sol" in df_final_txt.columns:
        df_final_txt["Centro"] = df_final_txt["Centro_sol"]
    elif "Centro" not in df_final_txt.columns:
        df_final_txt["Centro"] = pd.NA

    if "Almacen_sol" in df_final_txt.columns:
        df_final_txt["Almacen"] = df_final_txt["Almacen_sol"]
    elif "Almacen" not in df_final_txt.columns:
        df_final_txt["Almacen"] = pd.NA

    if "CentroBeneficio_sol" in df_final_txt.columns:
        df_final_txt["CentroBeneficio"] = df_final_txt["CentroBeneficio_sol"]
    elif "CentroBeneficio" not in df_final_txt.columns:
        df_final_txt["CentroBeneficio"] = pd.NA

    # Mapear a columnas finales
    df_final_txt["Almacén"] = df_final_txt["Almacen"]
    df_final_txt["Centro de beneficio.1"] = df_final_txt["CentroBeneficio"]

    # Si no existe "Tipo de material" (depende de tmp), úsalo desde solicitud
    if "Tipo de material" not in df_final_txt.columns or df_final_txt["Tipo de material"].isna().all():
        df_final_txt["Tipo de material"] = df_final_txt.get("TipoMaterial", pd.NA)

    # Completar Almacén si está vacío
    mask_a = df_final_txt["Almacén"].isna() | (df_final_txt["Almacén"].astype(str).str.strip() == "")
    df_final_txt.loc[mask_a, "Almacén"] = (
        df_final_txt.loc[mask_a, "Centro"].astype(str).str.strip().str[:2] + "01"
    )

    # Normalizar
    df_final_txt["Centro"] = df_final_txt["Centro"].astype(str).str.upper()
    df_final_txt["Almacén"] = df_final_txt["Almacén"].astype(str).str.upper()

    # Organización ventas desde CentroBeneficio
    def asignar_org_ventas(centro_beneficio):
        if centro_beneficio == "10900011":
            return "VNSO"
        elif centro_beneficio == "AA990006":
            return "VNMS"
        elif centro_beneficio == "AA900011":
            return "VNDS"
        elif centro_beneficio == "BB990006":
            return "VNMS"
        else:
            return ""

    df_final_txt["Organización ventas"] = df_final_txt["Centro de beneficio.1"].apply(asignar_org_ventas)

    # Asegurar columnas de vistas y marcarlas con X
    vistas_cols = [
        "Datos básicos 1","Clasificación","ventas 1","ventas 2","Ventas Gnal","Texto comercial",
        "Texto comercial expo","Compras","Texto comercial impo","Texto pedido compras",
        "Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4","Pronostico",
        "Preparación trabajo","Almacenamiento","calidad","Contabilidad","coste"
    ]
    for col in vistas_cols:
        if col not in df_final_txt.columns:
            df_final_txt[col] = np.nan

    for col in ["Compras","Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4",
                "Almacenamiento","Contabilidad","coste"]:
        if col in df_final_txt.columns:
            df_final_txt[col] = "X"

    # Defaults obligatorios
    if "Canal distribución" in df_final_txt.columns:
        mask = df_final_txt["Canal distribución"].isna() | (df_final_txt["Canal distribución"].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Canal distribución"] = "07"

    if "Derecho a descuento" in df_final_txt.columns:
        mask = df_final_txt["Derecho a descuento"].isna() | (df_final_txt["Derecho a descuento"].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Derecho a descuento"] = "X"

    # Planif necesidades por tipo material
    def asignar_planif_necesidades(tipo_material):
        if tipo_material == "Z120":
            return "Z07"
        elif tipo_material in ("Z130", "Z140"):
            return "Z06"
        elif tipo_material == "Z150":
            return "Z09"
        else:
            return ""

    if "Planif.necesidades" in df_final_txt.columns and "Tipo de material" in df_final_txt.columns:
        mask = df_final_txt["Planif.necesidades"].isna() | (df_final_txt["Planif.necesidades"].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Planif.necesidades"] = df_final_txt["Tipo de material"].apply(asignar_planif_necesidades)

    if "Tam.lote planif.nec." in df_final_txt.columns:
        mask = df_final_txt["Tam.lote planif.nec."].isna() | (df_final_txt["Tam.lote planif.nec."].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Tam.lote planif.nec."] = "EX"

    if "Clase aprovisionam." in df_final_txt.columns:
        mask = df_final_txt["Clase aprovisionam."].isna() | (df_final_txt["Clase aprovisionam."].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Clase aprovisionam."] = "F"

    if "Grupo planif.nec." in df_final_txt.columns:
        mask = df_final_txt["Grupo planif.nec."].isna() | (df_final_txt["Grupo planif.nec."].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Grupo planif.nec."] = "Z001"

    if "Caract.planif.nec." in df_final_txt.columns:
        mask = df_final_txt["Caract.planif.nec."].isna() | (df_final_txt["Caract.planif.nec."].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Caract.planif.nec."] = "PD"

    if "Clave de horizonte" in df_final_txt.columns:
        mask = df_final_txt["Clave de horizonte"].isna() | (df_final_txt["Clave de horizonte"].astype(str).str.strip() == "")
        df_final_txt.loc[mask, "Clave de horizonte"] = "P0"

    # Vaciar columnas para centros específicos (solo si existen)
    centros_objetivo = {"1400","B400","A400"}

    columnas_vista_vaciar = ["Planif.nece 1","Planif.nece 2","Planif.nece 3","Planif.nece 4"]
    cols_exist = [c for c in columnas_vista_vaciar if c in df_final_txt.columns]
    if cols_exist:
        df_final_txt.loc[df_final_txt["Centro"].isin(centros_objetivo), cols_exist] = pd.NA

    columnas_datos_vaciar = [
        'Grupo planif.nec.','Caract.planif.nec.','Punto de pedido','Planif.necesidades','Tam.lote planif.nec.',
        'Tamaño lote mínimo','Tamaño lote máximo','Tamaño lote fijo','Stock máximo','Rechazo conjunto (%)',
        'Valor de redondeo','Clase aprovisionam.','Aprovis.especial','Almacén producción','Toma retrograda',
        'Alm.aprov.externo','Tiempo fabric.propia','Plazo entrega prev.','Clave de horizonte','Stock de seguridad',
        'Perfil de cobertura','Grupo estrategia planificación','Modo de compensación','IntvCompens.atrás',
        'IntCompens.adelante','Verif.disponibilidad.1','TiempoGlobalReaprov','SelecciónAltern','Individual/Colectivo',
        'Fabricación repetit.','Perfil fabr.repet.'
    ]
    cols_exist = [c for c in columnas_datos_vaciar if c in df_final_txt.columns]
    if cols_exist:
        df_final_txt.loc[df_final_txt["Centro"].isin(centros_objetivo), cols_exist] = pd.NA

    # Clasificación fiscal fallback
    if "Clasificación fiscal" in df_final_txt.columns and "Ident.impuest.mat." in df_final_txt.columns:
        df_final_txt["Clasificación fiscal"] = df_final_txt.apply(
            lambda row: row["Clasificación fiscal"]
            if pd.notna(row["Clasificación fiscal"]) and str(row["Clasificación fiscal"]).strip() != ""
            else (
                row["Ident.impuest.mat."]
                if pd.notna(row["Ident.impuest.mat."]) and str(row["Ident.impuest.mat."]).strip() != ""
                else "0"
            ),
            axis=1
        )

    # Defaults NA requeridos
    for col in ["Centro de beneficio", "Precio variable", "Precio estándar", "Stat.mat.específ.ce."]:
        df_final_txt[col] = pd.NA
        # if col not in df_final_txt.columns:
        #     df_final_txt[col] = pd.NA
        # else:
        #     df_final_txt[col] = df_final_txt[col].where(pd.notna(df_final_txt[col]), pd.NA)

    # Forzar EXACTAMENTE columnas esperadas (ni una más, ni una menos) y en el orden correcto
    df_final_txt = df_final_txt.reindex(columns=EXPECTED_COLS)

    # Guardar TXT
    df_final_txt.to_csv(out_path, sep="\t", index=False, header=False, encoding="utf-8-sig")
    return str(out_path)


#--------------------------------------------------------------------------------------<
#--------------------------------------------------------------------------------------<
#--------------------------------------------------------------------------------------<
#--------------------------------------------------------------------------------------<
#--------------------------------------------------------------------------------------<

""" import pandas as pd
import numpy as np
from typing import Dict, Any
from ..utils.paths import resource_path, logs_dir

def generate_txt(cfg: Dict[str, Any]) -> str:
    # Rutas seguras
    tmp_path = resource_path("data/tmp/tmp.xlsx")
    solicitud_path = resource_path(cfg["excel"]["template_relative"])
    

    if not solicitud_path.exists():
        raise FileNotFoundError(f"No se encontró la plantilla en {solicitud_path}. Colócala en data/templates/")

    
    out_path = logs_dir() / cfg["output"]["txt_filename"]

    # Leer archivos
    df_tmp = pd.read_excel(tmp_path, dtype=str, engine="openpyxl")
    df_solicitud = pd.read_excel(solicitud_path, dtype=str, engine="openpyxl")

    # Renombrar columna clave
    
    df_solicitud = df_solicitud.rename(columns={"Título":"Codigo"})
    df_solicitud = df_solicitud.rename(columns={"CentroExtender":"Centro"})
    df_solicitud = df_solicitud.rename(columns={"Almacen":"Almacen"})
    df_solicitud = df_solicitud.rename(columns={"CentroModelo":"CentroModelo"})
    df_solicitud = df_solicitud.rename(columns={"CentroBeneficio":"CentroBeneficio"})
    df_solicitud = df_solicitud.rename(columns={"ID":"Secuencia"})
    df_solicitud = df_solicitud.rename(columns={"Estado":"Estado"})
    df_solicitud = df_solicitud.rename(columns={"TipoMaterial":"TipoMaterial"})
    df_solicitud = df_solicitud.rename(columns={"Mensaje":"Mensaje"})
    df_solicitud = df_solicitud.rename(columns={"id_axuliar":"Id_auxiliar"})

    # Normalizacion de columnas clave
    df_solicitud = df_solicitud.rename(columns={"Codigo": "Material"})
    df_solicitud["Material"] = df_solicitud["Material"].astype(str)
    df_tmp["Material"] = df_tmp["Material"].astype(str)

    
    # =========================
    # ✅ FILTRO REQUERIDO
    # =========================
    if "Mensaje" not in df_solicitud.columns:
        raise KeyError("La columna 'Mensaje' no existe en df_solicitud (revisa el nombre en el Excel).")

    mask_msg = (
        df_solicitud["Mensaje"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        == "extender centro".casefold()
    )

    # Nos quedamos SOLO con los registros que cumplen la condición
    df_solicitud = df_solicitud.loc[mask_msg].copy()
    
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

    # Completar Almacén si está vacío
    mask = df_final_txt["Almacén"].isna()
    df_final_txt.loc[mask,"Almacén"] = df_final_txt.loc[mask,"Centro"].str.strip().str[:2] + "01"

    # Normalizar
    df_final_txt["Centro"] = df_final_txt["Centro"].str.upper()
    df_final_txt["Almacén"] = df_final_txt["Almacén"].str.upper()


    
    def asignar_org_ventas(centro_beneficio):
        if centro_beneficio == "10900011":
            return "VNSO"
        elif centro_beneficio == "AA990006":
            return "VNMS"
        elif centro_beneficio == "AA900011":
            return "VNDS"
        elif centro_beneficio == "BB990006":
            return "VNMS"
        else:
            return ""  # Valor por defecto

    df_final_txt["Organización ventas"] = df_final_txt["Centro de beneficio.1"].apply(asignar_org_ventas)
    
    
    # Asignar planificador de necesidades según tipo material
    def asignar_planif_necesidades(tipo_material):
        if tipo_material == "Z120":
            return "Z07"
        elif tipo_material == "Z130":
            return "Z06"
        elif tipo_material == "Z140":
            return "Z06"
        elif tipo_material == "Z150":
            return "Z09"
        else:
            return ""  # Valor por defecto

    mask = df_final_txt["Planif.necesidades"].isna() | (df_final_txt["Planif.necesidades"].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Planif.necesidades"] = df_final_txt["Tipo de material"].apply(asignar_planif_necesidades)
    
    mask = df_final_txt["Tam.lote planif.nec."].isna() | (df_final_txt["Tam.lote planif.nec."].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Tam.lote planif.nec."] = "EX"
    
    mask = df_final_txt["Clase aprovisionam."].isna() | (df_final_txt["Clase aprovisionam."].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Clase aprovisionam."] = "F"   

    mask = df_final_txt["Grupo planif.nec."].isna() | (df_final_txt["Grupo planif.nec."].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Grupo planif.nec."] = "Z001"   
    
    mask = df_final_txt["Caract.planif.nec."].isna() | (df_final_txt["Caract.planif.nec."].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Caract.planif.nec."] = "PD"   
    
    mask = df_final_txt["Clave de horizonte"].isna() | (df_final_txt["Clave de horizonte"].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Clave de horizonte"] = "P0"

    mask = df_final_txt["Canal distribución"].isna() | (df_final_txt["Canal distribución"].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Canal distribución"] = "07"

    mask = df_final_txt["Derecho a descuento"].isna() | (df_final_txt["Derecho a descuento"].astype(str).str.strip() == "")
    df_final_txt.loc[mask, "Derecho a descuento"] = "X"
    
    
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


    if "Clasificación fiscal" in df_final_txt.columns and "Ident.impuest.mat." in df_final_txt.columns:
        df_final_txt["Clasificación fiscal"] = df_final_txt.apply(
            lambda row: row["Clasificación fiscal"]
            if pd.notna(row["Clasificación fiscal"]) and str(row["Clasificación fiscal"]).strip() != ""
            else (
                row["Ident.impuest.mat."]
                if pd.notna(row["Ident.impuest.mat."]) and str(row["Ident.impuest.mat."]).strip() != ""
                else "0"
            ),
            axis=1
        )
    else:
        print("⚠️ Las columnas requeridas no existen en el DataFrame.")


    # Guardar TXT
    df_final_txt.to_csv(out_path, sep="\t", index=False, header=False, encoding="utf-8-sig")
    return str(out_path)

#Tareas: Sacar Listado de MARA: MTART=Z120,Z130,Z140,Z150 Sacar Listado de MARC: MATNR=Listado MARA con el campo DISPO DISLS BESKZ=F FHORI=P0 RWPRO=NULL STRGR=40 """