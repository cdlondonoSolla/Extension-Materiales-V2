from src.app.config import load_config
from src.app.utils.paths import resource_path, logs_dir

def main():
    cfg = load_config()
    print("Configuración cargada de config/config.json\n")

    plantilla = resource_path(cfg["excel"]["template_relative"]) 
    print(f"plantilla: {plantilla}")

    paths_cfg = cfg.get("paths", {})
    scripts_dir = paths_cfg.get("scripts", "scripts")
    tmp_xlsx_rel = paths_cfg.get("tmp_xlsx", "data/tmp/tmp.xlsx")
    vbs_clip_name = paths_cfg.get("vbs_clip", "LeerExcel_CopiarPortapapeles.vbs")
    vbs_tmp_name = paths_cfg.get("vbs_tmp", "script_tmp.vbs")
    vbs_cargue_name = paths_cfg.get("vbs_cargue", "cargue_sap.vbs")

    print(f"tmp_xlsx (rel): {tmp_xlsx_rel}")
    print(f"tmp_xlsx (abs): {resource_path(tmp_xlsx_rel)}")
    print(f"scripts dir: {scripts_dir}")
    print(f"vbs_clip: {resource_path(f'{scripts_dir}/{vbs_clip_name}')}")
    print(f"vbs_tmp: {resource_path(f'{scripts_dir}/{vbs_tmp_name}')}")
    print(f"vbs_cargue: {resource_path(f'{scripts_dir}/{vbs_cargue_name}')}")
    print(f"logs dir: {logs_dir()}")

if __name__ == '__main__':
    main()
