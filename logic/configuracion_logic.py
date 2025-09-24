import tkinter as tk
from tkinter import messagebox
import sys
import os

# from ..database import config_manager_db as db  # Usaremos un manager de DB específico para config

class ConfigLogic:
    """
    Controlador especializado para la lógica de la pestaña de Configuración.
    """
    def __init__(self, app_controller):
        self.app = app_controller
        # Aquí cargarías la configuración inicial al arrancar la app
        # self.app.configuracion = db.cargar_configuracion()

    def get_configuracion(self):
        """Devuelve la configuración actual que tiene la App."""
        return self.app.configuracion

    def aplicar_y_guardar_config(self, nuevos_valores):
        """
        Guarda la nueva configuración y gestiona si se necesita un reinicio.
        """
        config_anterior = self.app.configuracion.copy()
        
        # --- Lógica de Base de Datos (simulada) ---
        # exito = db.guardar_configuracion_multiples(nuevos_valores)
        exito = True # Simulación

        if exito:
            # Actualizamos la configuración en la instancia de la App
            self.app.configuracion.update(nuevos_valores)
            
            # --- Lógica de Negocio ---
            # Comparamos si un valor clave (como el tema) ha cambiado
            if config_anterior.get("tema") != nuevos_valores.get("tema"):
                if messagebox.askyesno("Reinicio Necesario", "Para aplicar el nuevo tema, es necesario reiniciar la aplicación.\n¿Desea reiniciar ahora?", parent=self.app):
                    self._reiniciar_aplicacion()
                else:
                    messagebox.showinfo("Información", "El nuevo tema se aplicará la próxima vez que inicie el programa.", parent=self.app)
            else:
                messagebox.showinfo("Éxito", "Configuración guardada correctamente.", parent=self.app)
                # Si otros valores cambiaron, podríamos necesitar actualizar otras partes de la UI
                # self.app.actualizar_titulo_app()
                # self.app.actualizar_alertas_stock()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración en la base de datos.", parent=self.app)

    def restaurar_config_default(self):
        """Restaura la configuración a los valores por defecto."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea restaurar todos los ajustes a sus valores por defecto?", parent=self.app):
            # exito = db.restaurar_configuracion_default()
            exito = True # Simulación
            if exito:
                # self.app.configuracion = db.cargar_configuracion() # Recargamos
                messagebox.showinfo("Éxito", "La configuración ha sido restaurada.", parent=self.app)
                return True
            else:
                messagebox.showerror("Error", "No se pudo restaurar la configuración.", parent=self.app)
                return False
        return False

    def _reiniciar_aplicacion(self):
        """Cierra y vuelve a abrir la aplicación."""
        python = sys.executable
        os.execl(python, python, *sys.argv)