# src/app/main.py
import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import sys

from src.app.config import load_config
from src.app.logging_setup import setup_logging
from src.app.io.txt_writer import generate_txt
from src.app.tasks.kill_excel import kill_excel
from src.app.tasks.cleanup import cleanup_tmp
from src.app.utils.paths import resource_path, logs_dir


def create_execution_folder() -> Path:
    """
    Crea una carpeta dentro de logs/ con timestamp (YYYYMMDD_HHMMSS)
    y la devuelve. Garantiza que existe.
    """
    base = logs_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = base / ts
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def run_pipeline() -> int:
    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    log = logging.getLogger(__name__)

    try:
        # 0) Crear carpeta de ejecución con timestamp
        exec_folder = create_execution_folder()
        log.info(f"Carpeta de ejecución: {exec_folder}")

        # 1) Logs de rutas esperadas (diagnóstico)
        plantilla_path = resource_path(cfg["excel"]["template_relative"])
        tmp_xlsx_path = resource_path("data/tmp/tmp.xlsx")
        log.info(f"Plantilla esperada en: {plantilla_path}")
        log.info(f"tmp.xlsx esperado en: {tmp_xlsx_path}")

        # 2) Ejecutar VBS: copiar datos al portapapeles desde la plantilla
        vbs_clip = resource_path("scripts/LeerExcel_CopiarPortapapeles.vbs")
        subprocess.run(["cscript", "//nologo", str(vbs_clip)], check=True)
        log.info("Datos copiados al portapapeles desde la plantilla.")

        # 3) Ejecutar VBS: generar tmp.xlsx consultando en SAP
        vbs_tmp = resource_path("scripts/script_tmp.vbs")
        subprocess.run(["cscript", "//nologo", str(vbs_tmp)], check=True)
        log.info("Archivo tmp.xlsx generado desde SAP.")

        # 4) Generar el archivo TXT (intenta con y sin exec_folder)
        txt_path_str: str | None = None
        try:
            # Versión nueva: generate_txt(cfg, exec_folder)
            txt_path_str = generate_txt(cfg, exec_folder)  # type: ignore[arg-type]
            log.info(f"Archivo TXT generado (con exec_folder) en: {txt_path_str}")
        except TypeError:
            # Versión anterior: generate_txt(cfg) que escribe en logs/
            log.info("generate_txt(cfg, exec_folder) no soportado; usando generate_txt(cfg) y moviendo archivo...")
            txt_path_str = generate_txt(cfg)  # type: ignore[call-arg]
            log.info(f"Archivo TXT generado (sin exec_folder) en: {txt_path_str}")

        # 6) Cerrar Excel (prevención de bloqueos)
        kill_excel()
        log.info("Instancias de Excel cerradas.")

        # 5) Ejecutar VBS: cargue en SAP usando el TXT generado
        vbs_cargue = resource_path("scripts/cargue_sap.vbs")
        subprocess.run(["cscript", "//nologo", str(vbs_cargue)], check=True)
        log.info("Archivo TXT cargado en SAP.")

        # Mover a carpeta de ejecución si se generó en logs/
        try:
            if txt_path_str:
                src_txt = Path(txt_path_str)
                if src_txt.exists():
                    dest_txt = exec_folder / src_txt.name
                    shutil.move(str(src_txt), str(dest_txt))
                    txt_path_str = str(dest_txt)
                    log.info(f"TXT movido a carpeta de ejecución: {dest_txt}")
        except Exception as move_err:
            log.warning(f"No se pudo mover el TXT a la carpeta de ejecución: {move_err}")

        # Mover también otros outputs conocidos (si existen) a la carpeta de ejecución
        # Por ejemplo: log de no encontrados
        no_encontrados_csv = logs_dir() / "log_materiales_no_encontrados.csv"
        if no_encontrados_csv.exists():
            shutil.move(str(no_encontrados_csv), str(exec_folder / no_encontrados_csv.name))
            log.info(f"Log de no encontrados movido a: {exec_folder / no_encontrados_csv.name}")
            
        log_bapi = logs_dir() / "LOG_BAPI.TXT"
        if log_bapi.exists():
            shutil.move(str(log_bapi), str(exec_folder / log_bapi.name))
            log.info(f"Log de no encontrados movido a: {exec_folder / log_bapi.name}")
            
        log_clase = logs_dir() / "LOG_CLASE.TXT"
        if log_clase.exists():
            shutil.move(str(log_clase), str(exec_folder / log_clase.name))
            log.info(f"Log de no encontrados movido a: {exec_folder / log_clase.name}")
            
        log_mat = logs_dir() / "LOG_MAT.TXT"
        if log_mat.exists():
            shutil.move(str(log_mat), str(exec_folder / log_mat.name))
            log.info(f"Log de no encontrados movido a: {exec_folder / log_mat.name}")
            
        log_error = logs_dir() / "LOG_ERROR.TXT"
        if log_error.exists():
            shutil.move(str(log_error), str(exec_folder / log_error.name))
            log.info(f"Log de no encontrados movido a: {exec_folder / log_error.name}")
        # 7) Limpiar temporales
        cleanup_tmp()
        log.info("Archivos temporales eliminados.")

        # 8) Copiar el log principal a la carpeta de ejecución (snapshot)
        app_log_file = logs_dir() / "app.log"
        if app_log_file.exists():
            try:
                shutil.copy(app_log_file, exec_folder / "app.log")
                log.info(f"Log principal copiado a carpeta de ejecución: {exec_folder / 'app.log'}")
            except Exception as copy_err:
                log.warning(f"No se pudo copiar app.log a la carpeta de ejecución: {copy_err}")

        log.info("Proceso finalizado correctamente.")
        return 0

    except subprocess.CalledProcessError as e:
        log.error(f"Error ejecutando script VBS: {e}")
        return 10
    except Exception as e:
        log.exception(f"Error general: {e}")
        return 99


if __name__ == "__main__":
    sys.exit(run_pipeline())