import tkinter as tk
from ttkbootstrap import Window, ttk
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


class App(Window):
    
    def __init__(self, config, single_instance_lock=None):
        self.configuracion = config
        super().__init__(themename=self.configuracion.get("tema", "superhero"))
        self.single_instance_lock = single_instance_lock
        
        self.is_fullscreen = True
        
        style = ttk.Style()

        style.configure('.', font=('Segoe UI', 12)) 
        style.configure('TButton', font=('Segoe UI', 11))
        style.configure('TNotebook.Tab', font=('Segoe UI', 11))
        style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'))
        style.configure("Treeview", font=("Segoe UI", 12), rowheight=40)
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))
        self._configurar_ventana()
        self._configurar_locale()

        # --- Estado Central de la Aplicación ---
        self.carrito = {}
        self.total_venta = 0.0
        
        # --- Inicializar todos los controladores de lógica ---
        self.app_logic = AppLogic(self)
        self.ventas_logic = VentasLogic(self)
        self.productos_logic = ProductosLogic(self)
        self.inventario_logic = InventarioLogic(self)
        self.historial_logic = HistorialLogic(self)
        self.caja_logic = CajaLogic(self)
        self.estadisticas_logic = EstadisticasLogic(self)
        self.config_logic = ConfigLogic(self)
        
        # --- Construcción de la UI ---
        self._crear_header()
        self._crear_notebook()
        self._crear_footer()
        self._crear_widget_notificaciones()
        
        # --- Procesos de Inicio y Bindings ---
        self._iniciar_procesos_de_fondo()
        self._configurar_bindings_globales()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def _configurar_ventana(self):
        """Configura los atributos principales de la ventana."""
        self.title("GestiaShop - Sistema de Gestión")
        self.attributes("-fullscreen", self.is_fullscreen)
        self.iconphoto(True, tk.PhotoImage(file=ruta_recurso('icons/icono_app.png')))

    def _crear_header(self):
        """Crea el encabezado de la aplicación con nombre, fecha y hora."""
        frame_header = ttk.Frame(self, padding=(10, 6))
        frame_header.pack(fill="x", side="top")
        
        frame_izquierda = ttk.Frame(frame_header); frame_izquierda.pack(side="left", anchor="w")
        self.lbl_nombre_comercio = ttk.Label(frame_izquierda, font=("Georgia", 22, "bold"))
        self.lbl_nombre_comercio.pack(anchor="w")
        self.lbl_fecha = ttk.Label(frame_izquierda, font=("Segoe UI", 12)); self.lbl_fecha.pack(anchor="w")
        
        frame_derecha = ttk.Frame(frame_header); frame_derecha.pack(side="right", anchor="e", padx=10)
        self.lbl_hora = ttk.Label(frame_derecha, font=("Segoe UI", 40, "bold")); self.lbl_hora.pack(anchor="e")
        self.header_btn_abrir_caja = ttk.Button(frame_derecha, text="☀️ Abrir Caja", command=self.abrir_caja, style="success.TButton")

    def _crear_notebook(self):
        """Crea y llena el panel de pestañas."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.ventas_tab = VentasTab(self.notebook, self); self.notebook.add(self.ventas_tab, text="Ventas (F1)")
        self.productos_tab = ProductosTab(self.notebook, self); self.notebook.add(self.productos_tab, text="Productos (F2)")
        self.inventario_tab = InventarioTab(self.notebook, self); self.notebook.add(self.inventario_tab, text="Inventario (F3)")
        self.historial_tab = HistorialTab(self.notebook, self); self.notebook.add(self.historial_tab, text="Historial (F4)")
        self.caja_tab = CajaTab(self.notebook, self); self.notebook.add(self.caja_tab, text="Caja (F5)")
        self.estadisticas_tab = EstadisticasTab(self.notebook, self); self.notebook.add(self.estadisticas_tab, text="Estadísticas (F6)")
        self.configuracion_tab = ConfiguracionTab(self.notebook, self); self.notebook.add(self.configuracion_tab, text="Configuración (F7)")

    def _crear_footer(self):
        """Crea el pie de página con botones de ayuda y alertas."""
        self.btn_soporte = ttk.Button(self, text="⛑️ Ayuda", command=self.mostrar_soporte)
        self.btn_soporte.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")
        self.btn_alerta_stock = ttk.Button(self, text="⚠ Alertas") # La lógica de app_logic lo gestionará
    def _crear_widget_notificaciones(self):
        """Crea la etiqueta que se usará para todas las notificaciones."""
        self.lbl_notificacion = ttk.Label(self, text="", font=("Segoe UI", 12), padding=10)
    def _iniciar_procesos_de_fondo(self):
        """Inicia tareas recurrentes y la configuración inicial de la UI."""
        self.actualizar_titulo_app()
        self.actualizar_fecha_hora()
        self.app_logic.manejar_apertura_caja_inicial()
        self.app_logic.actualizar_alertas_stock()
        self.historial_logic.recargar_historial_ventas()
        self.productos_logic.filtrar_productos_y_recargar()
        self.caja_logic.recargar_vista_caja()
    def _configurar_locale(self):
        """Configura el idioma para fechas y formatos."""
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except: 
            try: locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
            except: print("Advertencia: No se pudo establecer el locale a español.")
    
    def _configurar_bindings_globales(self):
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        
        # Atajos para cambiar de pestaña
        self.bind("<F1>", lambda e: self.notebook.select(0))
        self.bind("<F2>", lambda e: self.notebook.select(1))
        self.bind("<F3>", lambda e: self.notebook.select(2))
        self.bind("<F4>", lambda e: self.notebook.select(3))
        self.bind("<F5>", lambda e: self.notebook.select(4))
        self.bind("<F6>", lambda e: self.notebook.select(5))
        self.bind("<F7>", lambda e: self.notebook.select(6))
        
        # Atajos para la pestaña de Ventas
        self.bind("<Control-f>", lambda e: self.mostrar_ventana_cobrar())
        self.bind("<Control-b>", lambda e: self.mostrar_ventana_busqueda())
        self.bind("<Control-a>", lambda e: self.agregar_producto_comun())
        self.bind("<Control-d>", lambda e: self.vaciar_carrito())

        # Nuevos bindings para pantalla completa
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.salir_de_fullscreen)

    def toggle_fullscreen(self, event=None):
        """Activa o desactiva el modo de pantalla completa."""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def salir_de_fullscreen(self, event=None):
        """Sale del modo de pantalla completa si está activo."""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)

    # --- MÉTODOS DE ACTUALIZACIÓN DE UI PRINCIPAL ---
    def actualizar_fecha_hora(self):
       
        ahora = datetime.now()
        self.lbl_hora.config(text=ahora.strftime("%H:%M"))
        # Llama directamente a la función importada desde helpers
        self.lbl_fecha.config(text=helpers.formatear_fecha_es(ahora)) 
        self.after(60000, self.actualizar_fecha_hora)
        
    def actualizar_titulo_app(self):
        """Actualiza el título de la ventana y el nombre del comercio."""
        nombre = self.configuracion.get("nombre_comercio", "GestiaShop")
        self.title(f"{nombre} - Sistema de Gestión")
        self.lbl_nombre_comercio.config(text=nombre)

    def _on_tab_change(self, event):
        """Se ejecuta cuando se cambia de pestaña para recargar vistas dinámicas."""
        tab_texto = self.notebook.tab(self.notebook.select(), "text")
        if "Configuración" in tab_texto:
            self.configuracion_tab.recargar_vista()

    # =====================================================================
    # --- MÉTODOS DELEGADOS (La App solo redirige la llamada al especialista)
    # =====================================================================
    def abrir_caja(self): self.app_logic.dialogo_abrir_caja()
    def cerrar_app(self): self.app_logic.cerrar_aplicacion_seguro()
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