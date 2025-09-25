import tkinter as tk
from tkinter import Toplevel
import webbrowser
from ttkbootstrap import ttk
from datetime import date
from ..ui.utilities import notifications
from ..ui.utilities.dialogs import ConfirmacionDialog, PinDialog
from ..database import database_manager as db_manager

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

        hoy_db = date.today().strftime("%Y-%m-%d")
        estado, usuario = db_manager.consultar_estado_caja(hoy_db) 

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
        dialogo = Toplevel(self.app)
        dialogo.title("Apertura de Caja")
        dialogo.transient(self.app)
        dialogo.grab_set()
        dialogo.resizable(False, False)

        frame = ttk.Frame(dialogo, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="¿Quién abre la caja hoy?").pack()
        entry_usuario = ttk.Entry(frame, width=30)
        entry_usuario.pack(pady=5)
        entry_usuario.focus()

        ttk.Label(frame, text="¿Con cuánto fondo inicial?").pack()
        entry_fondo = ttk.Entry(frame, width=30)
        entry_fondo.pack(pady=5)

        def confirmar_apertura():
            usuario = entry_usuario.get().strip()
            fondo_str = entry_fondo.get().strip()

            if not all([usuario, fondo_str]):
                self.app.notificar_error("Ambos campos son obligatorios.")
                return
            
            try:
                fondo = float(fondo_str)
                hoy_db = date.today().strftime("%Y-%m-%d")
                
                exito = db_manager.registrar_apertura_caja(hoy_db, fondo, usuario)

                if exito:
                    self.app.modo_venta_activo = True
                    self.app.usuario_actual = usuario
                    self.app.header_btn_abrir_caja.pack_forget()
                    self._actualizar_estado_controles_venta()
                    self.app.caja_logic.recargar_vista_caja() # Avisa a la pestaña de caja que recargue
                    self.app.notificar_exito(f"Caja abierta por {usuario}.")
                    dialogo.destroy()
                else:
                    self.app.notificar_error("No se pudo registrar la apertura de caja.")

            except (ValueError, TypeError):
                self.app.notificar_error("El fondo inicial debe ser un número válido.")

        btn_confirmar = ttk.Button(frame, text="Confirmar y Empezar", command=confirmar_apertura)
        btn_confirmar.pack(pady=10)
        
        entry_fondo.bind("<Return>", lambda e: btn_confirmar.invoke())
        dialogo.bind("<Escape>", lambda e: dialogo.destroy())
    def solicitar_pin_admin(self):
        
        pin_guardado = self.app.configuracion.get("pin_admin", "0000") 

        # 2. Crea y muestra el diálogo de PIN
        dialogo_pin = PinDialog(self.app, pin_guardado)
        
        # 3. Devuelve el resultado
        return dialogo_pin.show()

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
        
        productos = db_manager.obtener_lista_productos_a_reponer()
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