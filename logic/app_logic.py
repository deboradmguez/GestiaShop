import customtkinter as ctk
import webbrowser, tkinter as tk
from PIL import Image
from datetime import date
from utilities import notifications, helpers
from utilities.dialogs import ConfirmacionDialog, PinDialog
from database import database_manager as db_manager

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
        dialogo = ctk.CTkToplevel(self.app)
        dialogo.title("Apertura de Caja")

        frame = ctk.CTkFrame(dialogo)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="¿Quién abre la caja hoy?").pack(anchor="w", padx=5)
        entry_usuario = ctk.CTkEntry(frame)
        entry_usuario.pack(fill="x", padx=5, pady=(0, 10))

        ctk.CTkLabel(frame, text="¿Con cuánto fondo inicial?").pack(anchor="w", padx=5)
        entry_fondo = ctk.CTkEntry(frame)
        entry_fondo.pack(fill="x", padx=5, pady=(0, 10))

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

        btn_confirmar = ctk.CTkButton(frame, text="Confirmar y Empezar", command=confirmar_apertura)
        btn_confirmar.pack(pady=10)
        helpers.configurar_dialogo(dialogo, self.app, entry_usuario)

        entry_usuario.bind("<Return>", lambda e: entry_fondo.focus())
        entry_fondo.bind("<Return>", lambda e: btn_confirmar.invoke())
        dialogo.bind("<Escape>", lambda e: dialogo.destroy())
        
    def solicitar_pin_admin(self):
        pin_guardado = self.app.configuracion.get("pin_admin", "0000") 
        dialogo_pin = PinDialog(self.app, pin_guardado)
        return dialogo_pin.show()

    def _actualizar_estado_controles_venta(self):
        """Activa o desactiva los controles de la pestaña de ventas."""
        estado_venta = "normal" if self.app.modo_venta_activo else "disabled"
        tab = self.app.ventas_tab
        
        if hasattr(tab, 'entry_codigo'):
            # Estos controles sí dependen de si la caja está abierta
            tab.entry_codigo.configure(state=estado_venta)
            tab.btn_prod_comun.configure(state=estado_venta)
            tab.btn_buscar_nombre.configure(state="normal")
    
    def cerrar_aplicacion_seguro(self):
        """Verifica el estado de la caja antes de cerrar."""
        hoy_db = date.today().strftime("%Y-%m-%d")
        caja_abierta, _ = db_manager.consultar_estado_caja(hoy_db) # Lógica de DB real
        if caja_abierta and self.app.modo_venta_activo:
            
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
        ventana_soporte = ctk.CTkToplevel(self.app)
        ventana_soporte.title("Soporte Técnico")
        ventana_soporte.transient(self.app)
        ventana_soporte.grab_set()
        ventana_soporte.resizable(False, False)

       
        frame_principal = ctk.CTkFrame(ventana_soporte)
        frame_principal.pack(fill="both", expand=True, padx=15, pady=15)
        
        frame_texto = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_texto.pack(side="left", fill="both", expand=True, padx=(0, 15))
        frame_qr = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_qr.pack(side="right")
        
        ctk.CTkLabel(frame_texto, text="Soporte Técnico", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(frame_texto, text="Para consultas o problemas, puedes:", font=("Segoe UI", 10)).pack(anchor="w")

        lbl_email = ctk.CTkLabel(frame_texto, text="Enviar un correo electrónico", font=ctk.CTkFont(size=10, underline=True), text_color="#6495ED", cursor="hand2")
        lbl_email.pack(anchor="w", pady=5)
        lbl_email.bind("<Button-1>", lambda e: webbrowser.open("mailto:sistema.app.dominguez@gmail.com"))

        ctk.CTkLabel(frame_texto, text="o escanear el código para chatear por WhatsApp.", font=("Segoe UI", 10)).pack(anchor="w")
        ctk.CTkLabel(frame_texto, text="\nVersión del Software: 1.0.0", font=ctk.CTkFont(size=9, slant="italic")).pack(anchor="w", pady=(10, 0))

        try:
            qr_path = self.app.ruta_recurso("icons/whatsapp_qr.png")
            imagen_original = Image.open(qr_path)
            qr_image = ctk.CTkImage(light_image=imagen_original, dark_image=imagen_original, size=(150, 150)) 
            
            lbl_qr = ctk.CTkLabel(frame_qr, image=qr_image, text="")
            lbl_qr.pack()
        except Exception as e:
            ctk.CTkLabel(frame_qr, text="Error al cargar QR").pack()
            print(f"Error al cargar imagen QR: {e}")
        
        helpers.centrar_ventana(ventana_soporte, self.app)
        ventana_soporte.bind("<Escape>", lambda e: ventana_soporte.destroy())
    def mostrar_alertas_de_stock(self):
        """Navega a la pestaña de productos y filtra por stock bajo."""
        self.app.notebook.set("Productos (F2)")
        
        self.app.productos_tab.combo_filtro_productos.set("Productos con stock bajo")
        
        self.app.productos_logic.filtrar_productos_y_recargar()

    def actualizar_alertas_stock(self):
        productos = db_manager.obtener_lista_productos_a_reponer()
        conteo = len(productos)

        if conteo > 0 and hasattr(self.app, 'btn_alerta_stock'):
            self.app.btn_alerta_stock.configure(
                text=f"⚠ {conteo} Alerta{'s' if conteo > 1 else ''}",
                fg_color="#D32F2F", hover_color="#B71C1C" # Color "danger"
            )
            self.app.btn_alerta_stock.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        elif hasattr(self.app, 'btn_alerta_stock'):
            self.app.btn_alerta_stock.place_forget()
        
    #notificaciones
    
    def notificar_exito(self, texto):
        notifications.mostrar_mensaje_exito(self.app.lbl_notificacion, texto)

    def notificar_alerta(self, texto):
        notifications.mostrar_mensaje_alerta(self.app.lbl_notificacion, texto)

    def notificar_error(self, texto):
        notifications.mostrar_mensaje_error(self.app.lbl_notificacion, texto)