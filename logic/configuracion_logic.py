import sys, os
from CTkMessagebox import CTkMessagebox # <-- 1. Importamos la nueva biblioteca
from utilities.themes import update_theme_dynamically 
from database import database_manager as db_manager
import time

CONFIG_DEFAULT = {
    "nombre_comercio": "GestiaShop",
    "tema": "dark",
    "mostrar_alertas_stock": True,
    "umbral_alerta_stock": 5,
    "pin_admin": "7114"
}

class ConfigLogic:
    def __init__(self, app_controller):
        self.app = app_controller
        self.app.configuracion = db_manager.cargar_configuracion_completa()

    def get_configuracion(self):
        return self.app.configuracion

    def aplicar_y_guardar_config(self, nuevos_valores):
        config_anterior = self.app.configuracion.copy()

        if not db_manager.guardar_configuracion(nuevos_valores):
            self.app.notificar_error("No se pudo guardar la configuración.")
            return

        self.app.configuracion.update(nuevos_valores)
        
        tema_cambiado = config_anterior.get("tema") != nuevos_valores.get("tema")

        if tema_cambiado:
            update_theme_dynamically(self.app, nuevos_valores.get("tema"))
            self.app.after(150, self.app.configuracion_tab.recargar_vista)
            self.app.notificar_exito("Tema actualizado correctamente.")
        else:
            self.app.notificar_exito("Configuración guardada correctamente.")

        self.app.actualizar_titulo_app()
        self.app.app_logic.actualizar_alertas_stock()
        
        self.app.productos_logic.filtrar_productos_y_recargar()


    def restaurar_config_default(self):
        # --- INICIO DE LA MODIFICACIÓN ---
        dialogo = CTkMessagebox(
            title="Confirmar Restauración",
            message="¿Está seguro de que desea restaurar todos los ajustes a sus valores por defecto?",
            icon="question",
            option_1="No",
            option_2="Sí",
            sound=True
        )
        
        if dialogo.get() != "Sí":
            self.app.notificar_alerta("Restauración cancelada.")
            return False
        # --- FIN DE LA MODIFICACIÓN ---

        tema_anterior = self.app.configuracion.get("tema")
        exito = db_manager.restaurar_configuracion()
        
        if exito:
            self.app.configuracion = db_manager.cargar_configuracion_completa()
            
            self.app.notificar_exito("La configuración ha sido restaurada.")
            
            tema_nuevo = self.app.configuracion.get("tema")
            if tema_anterior != tema_nuevo:
                update_theme_dynamically(self.app, tema_nuevo)
            
            self.app.configuracion_tab.recargar_vista()
            self.app.actualizar_titulo_app()
            self.app.app_logic.actualizar_alertas_stock()
            self.app.productos_logic.filtrar_productos_y_recargar()
            
            return True
        else:
            self.app.notificar_error("No se pudo restaurar la configuración.")
            return False


    def _reiniciar_aplicacion(self):
        if self.app.single_instance_lock:
            self.app.single_instance_lock.release()
            time.sleep(0.1)
        
        python = sys.executable
        os.execl(python, python, *sys.argv)