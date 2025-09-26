import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EstadisticasTab(ttk.Frame):
    """
    Clase que representa la INTERFAZ de la pestaña de Estadísticas.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        # Referencia para el widget del gráfico, se manejará desde el controlador
        self.canvas_grafico_widget = None

        self._crear_controles()
        self._crear_panel_resultados()

    def _crear_controles(self):
        """Crea el panel superior con selectores de fecha y botones."""
        frame_controles = ttk.Frame(self)
        frame_controles.pack(fill="x", pady=5)

        ttk.Label(frame_controles, text="Desde:", font=("Segoe UI", 11)).pack(side="left", padx=(0, 5))
        self.cal_desde = DateEntry(frame_controles, dateformat="%d/%m/%Y", width=12)
        self.cal_desde.pack(side="left")

        ttk.Label(frame_controles, text="Hasta:", font=("Segoe UI", 11)).pack(side="left", padx=(10, 5))
        self.cal_hasta = DateEntry(frame_controles, dateformat="%d/%m/%Y", width=12)
        self.cal_hasta.pack(side="left")

        btn_generar = ttk.Button(
            frame_controles, text="📈 Generar Reporte", style="primary.TButton",
            command=self.controller.generar_estadisticas # Llama al controlador
        )
        btn_generar.pack(side="left", padx=10)

        self.btn_pdf = ttk.Button(
            frame_controles, text="📄 Descargar PDF", style="info.TButton", state="disabled",
            command=self.controller.descargar_reporte_estadisticas # Llama al controlador
        )
        self.btn_pdf.pack(side="left", padx=5)

    def _crear_panel_resultados(self):
        """Crea el área principal que contendrá los resúmenes y el gráfico."""
        frame_resultados = ttk.Frame(self)
        frame_resultados.pack(fill="both", expand=True, pady=10)
        frame_resultados.columnconfigure(1, weight=1)

        frame_resumen_datos = ttk.Frame(frame_resultados)
        frame_resumen_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        frame_ganancias = ttk.LabelFrame(frame_resumen_datos, text="Resumen de Ingresos", padding=10)
        frame_ganancias.pack(fill="x", pady=5)
        self.lbl_total_facturado = ttk.Label(frame_ganancias, text="Facturación Total: $0.00", font=("Segoe UI", 12, "bold"))
        self.lbl_total_facturado.pack(anchor="w")
        self.lbl_total_efectivo = ttk.Label(frame_ganancias, text="Total Efectivo: $0.00", font=("Segoe UI", 10))
        self.lbl_total_efectivo.pack(anchor="w")
        self.lbl_total_transferencia = ttk.Label(frame_ganancias, text="Total Transferencia: $0.00", font=("Segoe UI", 10))
        self.lbl_total_transferencia.pack(anchor="w")

        frame_top_productos = ttk.LabelFrame(frame_resumen_datos, text="Top 5 Productos Vendidos", padding=10)
        frame_top_productos.pack(fill="x", pady=10)
        self.tree_top_productos = ttk.Treeview(frame_top_productos, columns=("producto", "cantidad"), show="headings", height=5)
        self.tree_top_productos.heading("producto", text="Producto")
        self.tree_top_productos.heading("cantidad", text="Unidades")
        self.tree_top_productos.column("producto", width=300)
        self.tree_top_productos.column("cantidad", width=100, anchor="center")
        self.tree_top_productos.pack(fill="x")

        self.frame_grafico = ttk.LabelFrame(frame_resultados, text="Distribución de Pagos", padding=10)
        self.frame_grafico.grid(row=0, column=1, sticky="nsew")
