import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import locale

# --- Vistas (Pestañas) ---
from .tabs.ventas_tab import VentasTab
from .tabs.productos_tab import ProductosTab
from .tabs.inventario_tab import InventarioTab
from .tabs.historial_tab import HistorialTab
from .tabs.caja_tab import CajaTab
from .tabs.estadisticas_tab import EstadisticasTab
from .tabs.configuracion_tab import ConfiguracionTab

# --- Lógica (Controladores) ---
from logic.app_logic import AppLogic
from logic.ventas_logic import VentasLogic
from logic.productos_logic import ProductosLogic
from logic.inventario_logic import InventarioLogic
from logic.historial_logic import HistorialLogic
from logic.caja_logic import CajaLogic
from logic.estadisticas_logic import EstadisticasLogic
from logic.configuracion_logic import ConfigLogic

# --- Utilidades ---
from utilities import helpers
from utilities.helpers import ruta_recurso
from utilities.themes import apply_custom_theme

class App(ctk.CTk):
    def __init__(self, config, single_instance_lock=None):
        super().__init__()
        self.configuracion = config
        self.single_instance_lock = single_instance_lock
        ctk.set_appearance_mode(self.configuracion.get("tema", "dark"))
        ctk.set_default_color_theme("blue")
        apply_custom_theme(self)

        self.is_fullscreen = True
        
        self._configurar_ventana()
        self._configurar_locale()

        self.carrito = {}
        self.total_venta = 0.0
        self.app_logic = AppLogic(self)
        self.ventas_logic = VentasLogic(self)
        self.productos_logic = ProductosLogic(self)
        self.inventario_logic = InventarioLogic(self)
        self.historial_logic = HistorialLogic(self)
        self.caja_logic = CajaLogic(self)
        self.estadisticas_logic = EstadisticasLogic(self)
        self.config_logic = ConfigLogic(self)
        self._crear_header()
        self._crear_notebook()
        self._crear_footer()
        self._crear_widget_notificaciones()
        self._iniciar_procesos_de_fondo()
        self._configurar_bindings_globales()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def _configurar_ventana(self):
        """Configura los atributos principales de la ventana."""
        self.title("GestiaShop - Sistema de Gestión")
        self.attributes("-fullscreen", self.is_fullscreen)
        
        self.configure(fg_color=("gray95", "gray10"))
        
        try: 
            icon_image = ctk.CTkImage(Image.open(ruta_recurso('icons/icono_app.png')))
            self.iconbitmap(ruta_recurso('icons/icono_app.ico'))
        except Exception as e:
            print(f"No se pudo cargar el icono de la aplicación: {e}")

   

    

    def _crear_header(self):
        frame_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_header.pack(fill="x", side="top", padx=10, pady=(6, 0))
        
        frame_izquierda = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_izquierda.pack(side="left", anchor="w", padx=10)
        self.lbl_nombre_comercio = ctk.CTkLabel(frame_izquierda, text="", font=ctk.CTkFont(family="Georgia", size=22, weight="bold"))
        self.lbl_nombre_comercio.pack(anchor="w")
        self.lbl_fecha = ctk.CTkLabel(frame_izquierda, text="", font=("Segoe UI", 12))
        self.lbl_fecha.pack(anchor="w")
        
        frame_derecha = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_derecha.pack(side="right", anchor="e", padx=10)
        self.lbl_hora = ctk.CTkLabel(frame_derecha, text="", font=ctk.CTkFont(size=40, weight="bold"))
        self.lbl_hora.pack(anchor="e")
        self.header_btn_abrir_caja = ctk.CTkButton(frame_derecha, text="☀️ Abrir Caja", command=self.abrir_caja, fg_color="#28a745", hover_color="#218838")
        
    def _crear_notebook(self):
        self.notebook = ctk.CTkTabview(self, command=self._on_tab_change)
        self.notebook.pack(pady=(10, 5), padx=10, fill="both", expand=True)
       
        self.notebook.add("Ventas (F1)")
        self.notebook.add("Productos (F2)")
        self.notebook.add("Inventario (F3)")
        self.notebook.add("Historial (F4)")
        self.notebook.add("Caja (F5)")
        self.notebook.add("Estadísticas (F6)")
        self.notebook.add("Configuración (F7)")
        self.notebook.configure(fg_color="transparent")
    
        self.ventas_tab = VentasTab(self.notebook.tab("Ventas (F1)"), self)
        self.ventas_tab.pack(fill="both", expand=True)
        self.productos_tab = ProductosTab(self.notebook.tab("Productos (F2)"), self)
        self.productos_tab.pack(fill="both", expand=True)
        self.inventario_tab = InventarioTab(self.notebook.tab("Inventario (F3)"), self)
        self.inventario_tab.pack(fill="both", expand=True)
        self.historial_tab = HistorialTab(self.notebook.tab("Historial (F4)"), self)
        self.historial_tab.pack(fill="both", expand=True)
        self.caja_tab = CajaTab(self.notebook.tab("Caja (F5)"), self)
        self.caja_tab.pack(fill="both", expand=True)
        self.estadisticas_tab = EstadisticasTab(self.notebook.tab("Estadísticas (F6)"), self)
        self.estadisticas_tab.pack(fill="both", expand=True)
        self.configuracion_tab = ConfiguracionTab(self.notebook.tab("Configuración (F7)"), self)
        self.configuracion_tab.pack(fill="both", expand=True)


    def _crear_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=(5, 10))

        footer_frame.grid_columnconfigure(0, weight=0)
        footer_frame.grid_columnconfigure(1, weight=1) 
        footer_frame.grid_columnconfigure(2, weight=0)

        self.btn_soporte = ctk.CTkButton(footer_frame, text="⛑️ Ayuda", command=self.mostrar_soporte)
        self.btn_soporte.grid(row=0, column=0, sticky="w") 

        self.btn_alerta_stock = ctk.CTkButton(footer_frame, text="⚠ Alertas", command=self.app_logic.mostrar_alertas_de_stock)
        self.btn_alerta_stock.grid(row=0, column=2, sticky="e") 
        self.btn_alerta_stock.grid_remove()
    def _crear_widget_notificaciones(self):
        self.lbl_notificacion = ctk.CTkLabel(self, text="", font=("Segoe UI", 12))
    def _iniciar_procesos_de_fondo(self):
        self.actualizar_titulo_app()
        self.actualizar_fecha_hora()
        self.app_logic.manejar_apertura_caja_inicial()
        self.app_logic.actualizar_alertas_stock()
        self.historial_logic.recargar_historial_ventas()
        self.productos_logic.filtrar_productos_y_recargar()
        self.caja_logic.recargar_vista_caja()
        from utilities.themes import apply_dark_theme_to_all_treeviews
        # Excluir el Treeview de historial
        self.after(200, lambda: apply_dark_theme_to_all_treeviews(
            self, 
            exclude_widgets=[self.historial_tab.tree_historial]
        ))
        self.after(250, lambda: self.historial_tab.configurar_tags_treeview())
    def _configurar_locale(self):
        
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except: 
            try: locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
            except: print("Advertencia: No se pudo establecer el locale a español.")
    
    def _configurar_bindings_globales(self):

        self.bind("<F1>", lambda e: self.notebook.set("Ventas (F1)"))
        self.bind("<F2>", lambda e: self.notebook.set("Productos (F2)"))
        self.bind("<F3>", lambda e: self.notebook.set("Inventario (F3)"))
        self.bind("<F4>", lambda e: self.notebook.set("Historial (F4)"))
        self.bind("<F5>", lambda e: self.notebook.set("Caja (F5)"))
        self.bind("<F6>", lambda e: self.notebook.set("Estadísticas (F6)"))
        self.bind("<F7>", lambda e: self.notebook.set("Configuración (F7)"))
        
        self.bind("<Control-f>", lambda e: self.mostrar_ventana_cobrar())
        self.bind("<Control-b>", lambda e: self.mostrar_ventana_busqueda())
        self.bind("<Control-a>", lambda e: self.agregar_producto_comun())
        self.bind("<Control-d>", lambda e: self.vaciar_carrito())

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.salir_de_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def salir_de_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
    def mostrar_detalles_producto(self, codigo_producto):
        self.notebook.set("Productos (F2)") 
        self.productos_logic.buscar_y_seleccionar_producto(codigo_producto)
        
    # --- MÉTODOS DE ACTUALIZACIÓN DE UI PRINCIPAL ---
    def actualizar_fecha_hora(self):
       
        ahora = datetime.now()
        self.lbl_hora.configure(text=ahora.strftime("%H:%M"))
        self.lbl_fecha.configure(text=helpers.formatear_fecha_es(ahora)) 
        self.after(60000, self.actualizar_fecha_hora)
        
    def actualizar_titulo_app(self):
        """Actualiza el título de la ventana y el nombre del comercio."""
        nombre = self.configuracion.get("nombre_comercio", "GestiaShop")
        self.title(f"{nombre} - Sistema de Gestión")
        self.lbl_nombre_comercio.configure(text=nombre)

    def _on_tab_change(self):
        tab_seleccionada = self.notebook.get() 
        if "Configuración" in tab_seleccionada:
            self.configuracion_tab.recargar_vista()
    

    def abrir_caja(self): self.app_logic.dialogo_abrir_caja()
    def cerrar_app(self):
        if self.single_instance_lock:
            self.single_instance_lock.release()
        self.app_logic.cerrar_aplicacion_seguro()
    def mostrar_soporte(self): self.app_logic.mostrar_ventana_soporte()
    def ruta_recurso(self, path): return ruta_recurso(path)
    # -- Delegados de Ventas --
    def buscar_y_agregar_a_carrito(self): self.ventas_logic.buscar_y_agregar_a_carrito()
    def vaciar_carrito(self): self.ventas_logic.vaciar_carrito()
    def quitar_producto_del_carrito(self): self.ventas_logic.quitar_producto_del_carrito()
    def modificar_cantidad_carrito(self, e=None): self.ventas_logic.modificar_cantidad_carrito(e)
    def mostrar_ventana_busqueda(self): self.ventas_logic.mostrar_ventana_busqueda()
    def agregar_producto_desde_busqueda(self, c): self.ventas_logic.agregar_producto_desde_busqueda(c)
    def agregar_producto_comun(self): self.ventas_logic.agregar_producto_comun()
    def mostrar_ventana_cobrar(self): self.ventas_logic.mostrar_ventana_cobrar()
    def finalizar_venta(self, d): return self.ventas_logic.finalizar_venta(d)
 # -- Delegados de Productos --
    def realizar_busqueda_productos(self, t, w): self.productos_logic.realizar_busqueda_productos(t, w)
    def filtrar_productos_y_recargar(self, e=None): self.productos_logic.filtrar_productos_y_recargar(e)
    def mostrar_ventana_agregar_producto(self, c=""): self.productos_logic.mostrar_ventana_agregar_producto(c)
    def modificar_producto(self): self.productos_logic.modificar_producto()
    def eliminar_producto(self): self.productos_logic.eliminar_producto()
    def editar_con_doble_click(self, e): self.productos_logic.editar_con_doble_click(e)
    def abrir_ventana_carga_rapida(self): self.productos_logic.abrir_ventana_carga_rapida()
    # -- Delegados de Inventario --
    def buscar_producto_para_inventario(self, e=None): self.inventario_logic.buscar_producto_para_inventario(e)
    def guardar_cambios_inventario(self, e=None): self.inventario_logic.guardar_cambios_inventario(e)
        
    # -- Delegados de Historial --
    def recargar_historial_ventas(self): self.historial_logic.recargar_historial_ventas()
    def anular_venta_seleccionada(self): self.historial_logic.anular_venta_seleccionada()
    def actualizar_estado_boton_anular(self, e=None): self.historial_logic.actualizar_estado_boton_anular(e)
    def deseleccionar_si_clic_vacio(self, e): self.historial_logic.deseleccionar_si_clic_vacio(e)
    def ir_a_hoy_historial(self): self.historial_logic.ir_a_hoy_historial()
    def descargar_reporte_historial(self): self.historial_logic.descargar_reporte_historial()
        
    # -- Delegados de Caja --
    def recargar_vista_caja(self): self.caja_logic.recargar_vista_caja()
    def procesar_cierre_caja(self, f, t): self.caja_logic.procesar_cierre_caja(f, t)
    def ajustar_cierre_de_caja(self, f): self.caja_logic.ajustar_cierre_de_caja(f)
    def ir_a_hoy_caja(self): self.caja_logic.ir_a_hoy_caja()
    def descargar_reporte_caja(self): self.caja_logic.descargar_reporte_caja()
    
    # -- Delegados de Estadísticas --
    def generar_estadisticas(self): self.estadisticas_logic.generar_estadisticas()
    def descargar_reporte_estadisticas(self): self.estadisticas_logic.descargar_reporte_estadisticas()
        
    # -- Delegados de Configuración --
    def get_configuracion(self): return self.config_logic.get_configuracion()
    def aplicar_y_guardar_config(self, v): self.config_logic.aplicar_y_guardar_config(v)
    def restaurar_config_default(self): return self.config_logic.restaurar_config_default()

    # -- Delegados de App --
    def notificar_exito(self, texto):
        self.app_logic.notificar_exito(texto)
        
    def notificar_alerta(self, texto):
        self.app_logic.notificar_alerta(texto)
        
    def notificar_error(self, texto):
        self.app_logic.notificar_error(texto)