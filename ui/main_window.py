import tkinter as tk
from ttkbootstrap import Window, ttk

# --- Vistas (Pestañas) ---
from .tabs.ventas_tab import VentasTab
from .tabs.productos_tab import ProductosTab
from .tabs.inventario_tab import InventarioTab
from .tabs.historial_tab import HistorialTab
from .tabs.caja_tab import CajaTab
from .tabs.estadisticas_tab import EstadisticasTab
from .tabs.configuracion_tab import ConfiguracionTab


# --- Lógica (Controladores Especializados) ---
from ..logic.ventas_logic import VentasLogic
from ..logic.productos_logic import ProductosLogic
from ..logic.inventario_logic import InventarioLogic
from ..logic.historial_logic import HistorialLogic
from ..logic.caja_logic import CajaLogic
from ..logic.estadisticas_logic import EstadisticasLogic
from ..logic.configuracion_logic import ConfigLogic


class App(Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Gestión de Ventas e Inventario")
        
        self.carrito = {}
        self.total_venta = 0.0
        self.configuracion = {"umbral_alerta_stock": 5}
        
        # --- Controladores de Lógica Especializados ---
        self.ventas_logic = VentasLogic(self)
        self.productos_logic = ProductosLogic(self)
        self.inventario_logic = InventarioLogic(self)
        self.historial_logic = HistorialLogic(self)
        self.caja_logic = CajaLogic(self)
        self.estadisticas_logic = EstadisticasLogic(self)
        self.config_logic = ConfigLogic(self)
        
        self._crear_widgets()

    def _crear_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, fill="both", expand=True)

        self.ventas_tab = VentasTab(notebook, controller=self)
        notebook.add(self.ventas_tab, text="VENTAS (F1)")
        
        self.productos_tab = ProductosTab(notebook, controller=self)
        notebook.add(self.productos_tab, text="PRODUCTOS (F2)")
        
        self.inventario_tab = InventarioTab(notebook, controller=self)
        notebook.add(self.inventario_tab, text="INVENTARIO (F3)")

        self.historial_tab = HistorialTab(notebook, controller=self)
        notebook.add(self.historial_tab, text="HISTORIAL (F4)")

        self.caja_tab = CajaTab(notebook, controller=self)
        notebook.add(self.caja_tab, text="CAJA (F5)")

        self.estadisticas_tab = EstadisticasTab(notebook, controller=self)
        notebook.add(self.estadisticas_tab, text="ESTADÍSTICAS (F6)")
        
        self.configuracion_tab = ConfiguracionTab(notebook, controller=self)
        notebook.add(self.configuracion_tab, text="CONFIGURACIÓN (F7)")

    # =====================================================================
    # --- MÉTODOS DELEGADOS ---
    # La clase App ya no contiene la lógica detallada. Su trabajo es
    # simplemente pasar la solicitud al controlador especialista correcto.
    # =====================================================================

    # -- Delegados de Ventas --
    
    def buscar_y_agregar_a_carrito(self):
        self.ventas_logic.buscar_y_agregar_a_carrito()

    def vaciar_carrito(self):
        self.ventas_logic.vaciar_carrito()

    def quitar_producto_del_carrito(self):
        self.ventas_logic.quitar_producto_del_carrito()

    def modificar_cantidad_carrito(self, event=None):
        self.ventas_logic.modificar_cantidad_carrito(event)

    def mostrar_ventana_busqueda(self):
        # Nota: La ventana de búsqueda es creada por la lógica de ventas, 
        # pero como necesita llamar a métodos de la App, le pasamos 'self'.
        self.ventas_logic.mostrar_ventana_busqueda()

    def agregar_producto_desde_busqueda(self, codigo_barras):
        self.ventas_logic.agregar_producto_desde_busqueda(codigo_barras)

    def agregar_producto_comun(self):
        self.ventas_logic.agregar_producto_comun()

    def mostrar_ventana_cobrar(self):
        self.ventas_logic.mostrar_ventana_cobrar()
    
    def finalizar_venta(self, payment_data):
        # Este método necesita devolver un valor, así que lo retornamos.
        return self.ventas_logic.finalizar_venta(payment_data)

    # -- Delegados de Productos --

    def filtrar_productos_y_recargar(self, event=None):
        self.productos_logic.filtrar_productos_y_recargar(event)

    def mostrar_ventana_agregar_producto(self, codigo_previo=""):
        self.productos_logic.mostrar_ventana_agregar_producto(codigo_previo)

    def modificar_producto(self):
        self.productos_logic.modificar_producto()

    def eliminar_producto(self):
        self.productos_logic.eliminar_producto()

    def editar_con_doble_click(self, event):
        self.productos_logic.editar_con_doble_click(event)

    def abrir_ventana_carga_rapida(self):
        self.productos_logic.abrir_ventana_carga_rapida()
        
    # inventario
       
    def buscar_producto_para_inventario(self, event=None):
        self.inventario_logic.buscar_producto_para_inventario(event)
        
    def guardar_cambios_inventario(self, event=None):
        self.inventario_logic.guardar_cambios_inventario(event)
        
    # --- Historial ---
    def recargar_historial_ventas(self):
        self.historial_logic.recargar_historial_ventas()
        
    def anular_venta_seleccionada(self):
        self.historial_logic.anular_venta_seleccionada()
        
    def actualizar_estado_boton_anular(self, event=None):
        self.historial_logic.actualizar_estado_boton_anular(event)
        
    def deseleccionar_si_clic_vacio(self, event):
        self.historial_logic.deseleccionar_si_clic_vacio(event)
        
    def ir_a_hoy_historial(self):
        self.historial_logic.ir_a_hoy_historial()
        
    def descargar_reporte_historial(self):
        self.historial_logic.descargar_reporte_historial()
        
        
    #caja
    def recargar_vista_caja(self):
        self.caja_logic.recargar_vista_caja()
    
    def procesar_cierre_caja(self, fecha_str, total_esperado):
        self.caja_logic.procesar_cierre_caja(fecha_str, total_esperado)
    
    def ajustar_cierre_de_caja(self, fecha_str):
        self.caja_logic.ajustar_cierre_de_caja(fecha_str)
    
    def ir_a_hoy_caja(self):
        self.caja_logic.ir_a_hoy_caja()
        
    def descargar_reporte_caja(self, fecha_str):
        self.caja_logic.descargar_reporte_caja(fecha_str)
    
    #estadisticas
    
    def generar_estadisticas(self):
        self.estadisticas_logic.generar_estadisticas()

    def descargar_reporte_estadisticas(self):
        self.estadisticas_logic.descargar_reporte_estadisticas
        
    #configuraciones
    
    def get_configuracion(self):
        return self.config_logic.get_configuracion()
        
    def aplicar_y_guardar_config(self, nuevos_valores):
        self.config_logic.aplicar_y_guardar_config(nuevos_valores)
        
    def restaurar_config_default(self):
        return self.config_logic.restaurar_config_default()
     
       
    
    
    #utilidades
        
    def ruta_recurso(self, ruta_relativa):
        # Esta es una función de utilidad que puede vivir en la App principal
        # o en un archivo de utilidades separado. Por ahora, aquí está bien.
        # import os, sys
        # try:
        #     ruta_base = sys._MEIPASS
        # except Exception:
        #     ruta_base = os.path.abspath(".")
        # return os.path.join(ruta_base, ruta_relativa)
        return ruta_relativa # Simulación para desarrollo

