import tkinter as tk
from tkinter import Toplevel
from ttkbootstrap import ttk
from datetime import date
from ..ui.utilities import notifications
from ..ui.utilities.dialogs import ConfirmacionDialog
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
            self.app.notificar_exito(f"Caja abierta por {usuario_nuevo}.")

    def _actualizar_estado_controles_venta(self):
        """Activa o desactiva los controles de la pestaña de ventas."""
        estado = "normal" if self.app.modo_venta_activo else "disabled"
        tab = self.app.ventas_tab
        # Esto asegura que los widgets existan antes de intentar configurarlos
        if hasattr(tab, 'entry_codigo'):
            tab.entry_codigo.config(state=estado)
            tab.btn_buscar_nombre.config(state=estado)
            tab.btn_prod_comun.config(state=estado)
    
    def cerrar_aplicacion_seguro(self):
        """Verifica el estado de la caja antes de cerrar."""
        # caja_abierta = db.verificar_caja_abierta() # Lógica de DB real
        caja_abierta_simulacion = True # Simulación
        if caja_abierta_simulacion and self.app.modo_venta_activo:
            
            dialogo = ConfirmacionDialog(
                parent=self.app,
                title="Confirmar Cierre",
                message="La caja del día aún está abierta.\n¿Desea cerrar de todos modos?"
            )
            
            respuesta = dialogo.show()
            if respuesta:
                self.app.destroy()
        else:
            self.app.destroy()
    
    def mostrar_ventana_soporte(self):
        """Muestra la ventana emergente de Soporte Técnico."""
        ventana_soporte = Toplevel(self.app)
        ventana_soporte.title("Soporte Técnico")
        ventana_soporte.transient(self.app)
        ventana_soporte.grab_set()
        ventana_soporte.resizable(False, False)

        frame_principal = ttk.Frame(ventana_soporte, padding=15)
        frame_principal.pack(fill="both", expand=True)
        frame_texto = ttk.Frame(frame_principal)
        frame_texto.pack(side="left", fill="both", expand=True, padx=(0, 15))
        frame_qr = ttk.Frame(frame_principal)
        frame_qr.pack(side="right")
        
        ttk.Label(frame_texto, text="Soporte Técnico", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(frame_texto, text="Para consultas o problemas, puedes:", font=("Segoe UI", 10)).pack(anchor="w")

        lbl_email = ttk.Label(frame_texto, text="Enviar un correo electrónico", font=("Segoe UI", 10, "underline"), foreground="#6495ED", cursor="hand2")
        lbl_email.pack(anchor="w", pady=5)
        lbl_email.bind("<Button-1>", lambda e: webbrowser.open("mailto:sistema.app.dominguez@gmail.com"))

        ttk.Label(frame_texto, text="o escanear el código para chatear por WhatsApp.", font=("Segoe UI", 10)).pack(anchor="w")
        ttk.Label(frame_texto, text="\nVersión del Software: 1.0.0", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(10, 0))

        try:
            # Asumiendo que ruta_recurso ahora es un método del controlador App
            qr_path = self.app.ruta_recurso("icons/whatsapp_qr.png")
            qr_image_original = tk.PhotoImage(file=qr_path)
            qr_image = qr_image_original.subsample(3, 3)
            lbl_qr = ttk.Label(frame_qr, image=qr_image)
            lbl_qr.image = qr_image 
            lbl_qr.pack()
        except tk.TclError:
            ttk.Label(frame_qr, text="Error al cargar QR").pack()
        
        # Aquí necesitaríamos una función de utilidad para centrar, la crearemos después
        # utils.centrar_ventana(ventana_soporte, self.app)

    def actualizar_alertas_stock(self):
        """Actualiza el botón de alertas de stock en la UI principal."""
        # Esta función obtendría los productos con stock bajo de la DB
        # productos = db.obtener_productos_a_reponer()
        productos = [("123", "Producto A", 2)] # Simulación
        conteo = len(productos)

        if conteo > 0 and hasattr(self.app, 'btn_alerta_stock'):
            self.app.btn_alerta_stock.config(text=f"⚠ {conteo} Alerta{'s' if conteo > 1 else ''}", style="danger.TButton")
            self.app.btn_alerta_stock.place(relx=1.0, rely=0, x=-5, y=-5, anchor="ne")
        elif hasattr(self.app, 'btn_alerta_stock'):
            self.app.btn_alerta_stock.place_forget()
    
    #notificaciones
    
    def notificar_exito(self, texto):
        notifications.mostrar_mensaje_exito(self.app.lbl_notificacion, texto)

    def notificar_alerta(self, texto):
        notifications.mostrar_mensaje_alerta(self.app.lbl_notificacion, texto)

    def notificar_error(self, texto):
        notifications.mostrar_mensaje_error(self.app.lbl_notificacion, texto)