import sys, os
from pathlib import Path
from datetime import datetime, date
import tkinter as tk


# --- Constantes para formateo de fecha ---
DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def centrar_ventana(ventana_a_centrar, ventana_referencia):
    """Centra una ventana emergente en relación a una ventana de referencia."""
    
    # --- CORRECCIÓN: Usamos un método más robusto para centrar ---

    def centrar():
        ventana_a_centrar.update_idletasks()
        ancho = ventana_a_centrar.winfo_width()
        alto = ventana_a_centrar.winfo_height()
        
        
        ref_x = ventana_referencia.winfo_x()
        ref_y = ventana_referencia.winfo_y()
        ref_ancho = ventana_referencia.winfo_width()
        ref_alto = ventana_referencia.winfo_height()

        x = ref_x + (ref_ancho // 2) - (ancho // 2)
        y = ref_y + (ref_alto // 2) - (alto // 2)
        
        ventana_a_centrar.geometry(f"+{x}+{y}")

    # Forzamos a la ventana a ser visible pero fuera de la pantalla
    ventana_a_centrar.geometry("+5000+5000") 
    ventana_a_centrar.deiconify() # Aseguramos que sea visible
    
    # Usamos after() para ejecutar el centrado justo después de que la ventana se haya dibujado
    ventana_a_centrar.after(10, centrar)
def ruta_recurso(ruta_relativa):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)
def obtener_ruta_guardado(nombre_carpeta):
    # La ruta base es la carpeta personal del usuario (ej: C:/Users/TuUsuario)
    ruta_base = Path.home() / "GestiaShop"
    
    ruta_final = ruta_base / nombre_carpeta
    
    ruta_final.mkdir(parents=True, exist_ok=True)
    
    return ruta_final


def formatear_fecha_es(dt: datetime):
    """Formatea un objeto datetime a un string en español."""
    dia_sem = DIAS_ES[dt.weekday()].capitalize()
    dia = dt.day
    mes = MESES_ES[dt.month - 1]
    año = dt.year
    return f"{dia_sem}, {dia} de {mes} de {año}"
        
def configurar_dialogo(dialogo, parent_app, widget_a_enfocar):
    dialogo.transient(parent_app)
    dialogo.grab_set()
    dialogo.resizable(False, False)
    
    centrar_ventana(dialogo, parent_app)
    
    dialogo.after(50, lambda: widget_a_enfocar.focus())