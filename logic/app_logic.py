import tkinter as tk
from tkinter import messagebox, Toplevel
from ttkbootstrap import ttk
from datetime import date

# from ..database import database_manager as db

class AppLogic:
    """
    Controlador para la lógica global de la aplicación que no pertenece
    a una pestaña específica.
    """
    def __init__(self, app_controller):
        self.app = app_controller
        self.app.modo_venta_activo = False
        self.app.usuario_actual = "Modo Consulta"

    def manejar_apertura_caja_inicial(self):
        """
        Verifica el estado de la caja al iniciar y configura la UI.
        """
        # estado, usuario = db.consultar_estado_caja_hoy() # Lógica de DB
        estado, usuario = "inexistente", None # Simulación

        if estado == 'abierta':
            self.app.modo_venta_activo = True
            self.app.usuario_actual = usuario
            self.app.header_btn_abrir_caja.pack_forget()
        elif estado == 'cerrada':
            self.app.modo_venta_activo = False
            self.app.usuario_actual = "Caja Cerrada"
            self.app.header_btn_abrir_caja.pack_forget()
        else: # 'inexistente'
            self.app.modo_venta_activo = False
            self.app.usuario_actual = "Modo Consulta"
            self.app.header_btn_abrir_caja.pack(side="right", padx=10, pady=5)
        
        self._actualizar_estado_controles_venta()

    def dialogo_abrir_caja(self):
        """
        Muestra el pop-up para abrir la caja y actualiza el estado de la app.
        """
        # Aquí iría la lógica del Toplevel para pedir usuario y fondo inicial.
        # Al confirmar, se guardaría en la DB y se actualizaría el estado.
        # usuario_nuevo = ... (obtenido del pop-up)
        usuario_nuevo = "Admin" # Simulación

        if usuario_nuevo:
            self.app.modo_venta_activo = True
            self.app.usuario_actual = usuario_nuevo
            self.app.header_btn_abrir_caja.pack_forget()
            self._actualizar_estado_controles_venta()
            self.app.caja_logic.recargar_vista_caja() # Avisa a la pestaña de caja que recargue
            messagebox.showinfo("Éxito", f"Caja abierta por {usuario_nuevo}.")

    def _actualizar_estado_controles_venta(self):
        """Activa o desactiva los controles de venta."""
        estado = "normal" if self.app.modo_venta_activo else "disabled"
        # Actualizaría los botones de la pestaña de ventas a través del controlador
        # self.app.ventas_tab.set_controls_state(estado)
        print(f"Controles de venta puestos en estado: {estado}")
    
    def cerrar_aplicacion_seguro(self):
        """Verifica la caja antes de cerrar."""
        caja_abierta = False # db.verificar_caja_abierta() # Lógica de DB
        if caja_abierta:
            if messagebox.askyesno("Confirmar Cierre", "La caja del día está abierta. ¿Desea cerrar de todos modos?"):
                self.app.destroy()
        else:
            self.app.destroy()
