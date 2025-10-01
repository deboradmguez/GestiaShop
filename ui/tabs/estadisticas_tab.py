import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.widgets.date_entry import DateEntry
class EstadisticasTab(ctk.CTkFrame):
    """
    Clase que representa la INTERFAZ de la pestaña de Estadísticas.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.canvas_grafico_widget = None

        self._crear_controles()
        self._crear_panel_resultados()
        
    def _crear_controles(self):
        """Crea el panel superior con selectores de fecha y botones."""
        frame_controles = ctk.CTkFrame(self)
        frame_controles.pack(fill="x", pady=5, padx=10)

        
        ctk.CTkLabel(frame_controles, text="Desde:", font=("Segoe UI", 11)).pack(side="left", padx=(0, 5))
        self.cal_desde = DateEntry(frame_controles)
        self.cal_desde.pack(side="left")
        self.cal_desde.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ctk.CTkLabel(frame_controles, text="Hasta:", font=("Segoe UI", 11)).pack(side="left", padx=(10, 5))
        self.cal_hasta = DateEntry(frame_controles)
        self.cal_hasta.pack(side="left")
        self.cal_hasta.insert(0, datetime.now().strftime("%d/%m/%Y"))

        btn_generar = ctk.CTkButton(
            frame_controles, text="📈 Generar Reporte",
            command=self.controller.generar_estadisticas
        )
        btn_generar.pack(side="left", padx=10)

        self.btn_pdf = ctk.CTkButton(
            frame_controles, text="📄 Descargar PDF", state="disabled",
            command=self.controller.descargar_reporte_estadisticas 
        )
        self.btn_pdf.pack(side="left", padx=5)

    def _crear_panel_resultados(self):
        """Crea el área principal que contendrá los resúmenes y el gráfico."""
        frame_resultados = ctk.CTkFrame(self, fg_color="transparent")
        frame_resultados.pack(fill="both", expand=True, pady=10, padx=10)
        frame_resultados.columnconfigure(1, weight=1)

        frame_resumen_datos = ctk.CTkFrame(frame_resultados)
        frame_resumen_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        frame_ganancias = ctk.CTkFrame(frame_resumen_datos, border_width=1)
        frame_ganancias.pack(fill="x", pady=5, padx=5, ipady=5)
        ctk.CTkLabel(frame_ganancias, text="Resumen de Ingresos", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))
        
        # Contenedor para los labels de ganancias
        frame_ganancias_inner = ctk.CTkFrame(frame_ganancias, fg_color="transparent")
        frame_ganancias_inner.pack(fill="x", padx=10)
        
        self.lbl_total_facturado = ctk.CTkLabel(frame_ganancias_inner, text="Facturación Total: $0.00", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_total_facturado.pack(anchor="w")
        self.lbl_total_efectivo = ctk.CTkLabel(frame_ganancias_inner, text="Total Efectivo: $0.00", font=("Segoe UI", 10))
        self.lbl_total_efectivo.pack(anchor="w")
        self.lbl_total_transferencia = ctk.CTkLabel(frame_ganancias_inner, text="Total Transferencia: $0.00", font=("Segoe UI", 10))
        self.lbl_total_transferencia.pack(anchor="w")

        frame_top_productos = ctk.CTkFrame(frame_resumen_datos, border_width=1)
        frame_top_productos.pack(fill="x", pady=10, padx=5)
        ctk.CTkLabel(frame_top_productos, text="Top 5 Productos Vendidos", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))


        self.tree_top_productos = ttk.Treeview(frame_top_productos, columns=("producto", "cantidad"), show="headings", height=5)
        self.tree_top_productos.heading("producto", text="Producto")
        self.tree_top_productos.heading("cantidad", text="Unidades")
        self.tree_top_productos.column("producto", width=300)
        self.tree_top_productos.column("cantidad", width=100, anchor="center")
        self.tree_top_productos.pack(fill="x", padx=10, pady=(0, 10))
        #configure_treeview_colors(self.tree_top_productos)

        # --- Gráfico ---
        self.frame_grafico = ctk.CTkFrame(frame_resultados, border_width=1)
        self.frame_grafico.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(self.frame_grafico, text="Distribución de Pagos", font=ctk.CTkFont(weight="bold")).pack(pady=(5,10))