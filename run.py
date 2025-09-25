import sys
import tkinter as tk
from tkinter import messagebox

# --- Importaciones de la Aplicación ---
from ui.main_window import App
from database import database_manager as db_manager
from database.queries import inicializar_base_de_datos
from utilities.single_instance import SingleInstance
from logic.licencia_logic import LicenciaLogic

def mostrar_ventana_activacion():
    """
    Muestra una ventana emergente para que el usuario ingrese el código de activación.
    """
    # Creamos una instancia de la lógica de licencias para usar sus métodos
    licencia_logic = LicenciaLogic()
    
    # Creamos una ventana raíz temporal solo para este diálogo
    activacion_root = tk.Tk()
    activacion_root.title("Activación Requerida")
    activacion_root.withdraw() # La ocultamos para que solo se vea el diálogo

    # (Aquí iría la creación de una ventana de activación más bonita desde ui/windows/)
    # Por ahora, usamos un simple diálogo para ser prácticos
    from tkinter.simpledialog import askstring
    codigo = askstring("Activación", "Tu período de prueba ha finalizado.\nPor favor, ingresa tu código de activación:", parent=activacion_root)

    if codigo:
        exito, mensaje = licencia_logic.validar_codigo_activacion(codigo)
        messagebox.showinfo("Resultado de Activación", mensaje)
        if exito:
            # Si la activación fue exitosa, reiniciamos la aplicación
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    activacion_root.destroy()
    sys.exit() # Cerramos la aplicación si no se activa

def main():
    """
    Punto de entrada principal de la aplicación.
    """
    # 1. Verificar instancia única
    myapp = SingleInstance(name="GestiaShop-App-Lock")
    if myapp.already_running():
        messagebox.showwarning("Aplicación en ejecución", "GestiaShop ya se está ejecutando.")
        sys.exit()

    # --- 2. VERIFICACIÓN DE LICENCIA ---
    licencia_logic = LicenciaLogic()
    licencia_valida, _ = licencia_logic.verificar_licencia()
    
    if not licencia_valida:
        mostrar_ventana_activacion()
        return # Detenemos la ejecución aquí

    # --- Si la licencia es válida, continuamos con el arranque normal ---
    if not inicializar_base_de_datos():
        sys.exit()

    config = db_manager.cargar_configuracion_completa()
    if not config:
        messagebox.showerror("Error Crítico", "No se pudo cargar la configuración inicial.")
        sys.exit()
    
    app = App(config=config)
    app.mainloop()

if __name__ == "__main__":
    main()