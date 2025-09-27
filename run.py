import sys,os
import customtkinter as ctk
from tkinter import messagebox
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)
from ui.main_window import App
from database import database_manager as db_manager
from database.queries import inicializar_base_de_datos
from utilities.single_instance import SingleInstance
from logic.licencia_logic import LicenciaLogic

def mostrar_ventana_activacion():
    licencia_logic = LicenciaLogic()
    activacion_root = ctk.CTk()
    activacion_root.title("Activación Requerida")
    activacion_root.withdraw()
    from tkinter.simpledialog import askstring
    codigo = askstring("Activación", "Tu período de prueba ha finalizado.\nPor favor, ingresa tu código de activación:", parent=activacion_root)
    if codigo:
        exito, mensaje = licencia_logic.validar_codigo_activacion(codigo)
        messagebox.showinfo("Resultado de Activación", mensaje)
        if exito:
            python = sys.executable
            os.execl(python, python, *sys.argv)
    activacion_root.destroy()
    sys.exit()

def main():
    
    myapp = SingleInstance(name="GestiaShop-App-Lock")
    if myapp.already_running():
        messagebox.showwarning("Aplicación en ejecución", "GestiaShop ya se está ejecutando.")
        sys.exit()
    licencia_logic = LicenciaLogic()
    licencia_valida, _ = licencia_logic.verificar_licencia()
    if not licencia_valida:
        mostrar_ventana_activacion()
        return
    if not inicializar_base_de_datos():
        sys.exit()
    config = db_manager.cargar_configuracion_completa()
    if not config:
        messagebox.showerror("Error Crítico", "No se pudo cargar la configuración inicial.")
        sys.exit()
    app = App(config=config, single_instance_lock=myapp)
    app.mainloop()

if __name__ == "__main__":
    main()