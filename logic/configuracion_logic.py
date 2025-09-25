import sys, os
from utilities.dialogs import ConfirmacionDialog
from database import database_manager as db_manager

CONFIG_DEFAULT = {
    "nombre_comercio": "GestiaShop",
    "tema": "superhero",
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
        
        exito = db_manager.guardar_configuracion(nuevos_valores)

        if exito:
            self.app.configuracion.update(nuevos_valores)
            
            # Actualizamos la UI inmediatamente donde sea necesario
            self.app.actualizar_titulo_app()
            self.app.app_logic.actualizar_alertas_stock()

            if config_anterior.get("tema") != nuevos_valores.get("tema"):
                dialogo = ConfirmacionDialog(
                    parent=self.app,
                    title="Reinicio Necesario",
                    message="Para aplicar el nuevo tema, es necesario reiniciar la aplicación.\n¿Desea reiniciar ahora?"
                )
                if dialogo.show():
                    self._reiniciar_aplicacion()
                else:
                    self.app.notificar_alerta("El nuevo tema se aplicará la próxima vez que inicie el programa.")
            else:
                self.app.notificar_exito("Configuración guardada correctamente.")
        else:
            self.app.notificar_error("No se pudo guardar la configuración.")

    def restaurar_config_default(self):
        dialogo = ConfirmacionDialog(
            parent=self.app,
            title="Confirmar Restauración",
            message="¿Está seguro de que desea restaurar todos los ajustes a sus valores por defecto?"
        )
        
        if dialogo.show():
            exito = db_manager.restaurar_configuracion()
            if exito:
                # Recargamos la configuración en la app
                self.app.configuracion = db_manager.cargar_configuracion_completa()
                self.app.notificar_exito("La configuración ha sido restaurada.")
                # Le pedimos a la pestaña que se redibuje con los nuevos valores
                self.app.configuracion_tab.recargar_vista()
                return True
            else:
                self.app.notificar_error("No se pudo restaurar la configuración.")
                return False
        return False

    def _reiniciar_aplicacion(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)