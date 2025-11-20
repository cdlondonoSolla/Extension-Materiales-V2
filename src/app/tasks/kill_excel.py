import subprocess

def kill_excel():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "EXCEL.EXE"], check=False)
    except Exception as e:
        print(f"Error cerrando Excel: {e}")