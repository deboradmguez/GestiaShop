import sys, os
from datetime import datetime

# --- Constantes para formateo de fecha ---
DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def centrar_ventana(ventana_a_centrar, ventana_referencia):
    """Centra una ventana emergente en relación a una ventana de referencia."""
    ventana_a_centrar.update_idletasks()
    ancho = ventana_a_centrar.winfo_width()
    alto = ventana_a_centrar.winfo_height()
    x = (ventana_referencia.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_referencia.winfo_screenheight() // 2) - (alto // 2)
    ventana_a_centrar.geometry(f"+{x}+{y}")

def ruta_recurso(ruta_relativa):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

def formatear_fecha_es(dt: datetime):
    """Formatea un objeto datetime a un string en español."""
    dia_sem = DIAS_ES[dt.weekday()].capitalize()
    dia = dt.day
    mes = MESES_ES[dt.month - 1]
    año = dt.year
    return f"{dia_sem}, {dia} de {mes} de {año}"
