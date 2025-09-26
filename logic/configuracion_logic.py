import sys, os
from utilities.dialogs import ConfirmacionDialog
from database import database_manager as db_manager
import time

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
        
        tema_cambiado = config_anterior.get("tema") != nuevos_valores.get("tema")

        if tema_cambiado:
            # 2. Si el tema cambió, el diálogo es específico y advierte del reinicio
            dialogo = ConfirmacionDialog(
                parent=self.app,
                title="Confirmar y Reiniciar",
                message="Ha cambiado el tema. Para aplicar este cambio, la aplicación se reiniciará.\n¿Desea guardar y reiniciar ahora?"
            )
            if dialogo.show():
                # Si el usuario acepta, guardamos y reiniciamos
                if db_manager.guardar_configuracion(nuevos_valores):
                    self._reiniciar_aplicacion()
                else:
                    self.app.notificar_error("No se pudo guardar la configuración.")
            else:
                # Si cancela, no hacemos nada y notificamos
                self.app.notificar_alerta("Cambios no guardados.")
        else:
            # 3. Si el tema no cambió, es un guardado normal
            dialogo = ConfirmacionDialog(
                parent=self.app,
                title="Confirmar Cambios",
                message="¿Está seguro de que desea guardar los nuevos ajustes?"
            )
            if dialogo.show():
                if db_manager.guardar_configuracion(nuevos_valores):
                    self.app.configuracion.update(nuevos_valores)
                    self.app.actualizar_titulo_app()
                    self.app.app_logic.actualizar_alertas_stock()
                    self.app.notificar_exito("Configuración guardada correctamente.")
                else:
                    self.app.notificar_error("No se pudo guardar la configuración.")
            else:
                self.app.notificar_alerta("Cambios no guardados.")


    def restaurar_config_default(self):
        dialogo = ConfirmacionDialog(
            parent=self.app,
            title="Confirmar Restauración",
            message="¿Está seguro de que desea restaurar todos los ajustes a sus valores por defecto?"
        )
        
        if dialogo.show():
            tema_anterior = self.app.configuracion.get("tema")
            exito = db_manager.restaurar_configuracion()
            
            if exito:
                self.app.configuracion = db_manager.cargar_configuracion_completa()
                self.app.notificar_exito("La configuración ha sido restaurada.")
                self.app.configuracion_tab.recargar_vista()
                
                # Si el tema cambió, solo notificamos
                if tema_anterior != self.app.configuracion.get("tema"):
                    self.app.notificar_alerta("El tema por defecto se aplicará en el próximo reinicio.")
                return True
            else:
                self.app.notificar_error("No se pudo restaurar la configuración.")
                return False
        return False

    def _reiniciar_aplicacion(self):
        if self.app.single_instance_lock:
            self.app.single_instance_lock.release()
            time.sleep(0.1)
        
        python = sys.executable
        os.execl(python, python, *sys.argv)