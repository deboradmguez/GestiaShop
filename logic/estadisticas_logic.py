from ttkbootstrap import ttk
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from ..database import database_manager as db
# from ..services import report_generator

class EstadisticasLogic:
    """
    Controlador especializado para la lógica de la pestaña de Estadísticas.
    """
    def __init__(self, app_controller):
        self.app = app_controller
        # Guardamos el estado de los últimos datos generados para el PDF
        self.ultimos_datos_generados = None

    def generar_estadisticas(self):
        """
        Valida fechas, obtiene los datos y actualiza toda la UI de la pestaña.
        """
        tab = self.app.estadisticas_tab
        fecha_inicio_str = tab.cal_desde.entry.get()
        fecha_fin_str = tab.cal_hasta.entry.get()

        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
            if fecha_inicio > fecha_fin:
                self.app.notificar_error("La fecha 'Desde' no puede ser posterior a la fecha 'Hasta'.")
                return
        except ValueError:
            self.app.notificar_error("Error de Formato", "Por favor, ingrese fechas válidas.")
            return

        # --- Lógica de Base de Datos (simulada) ---
        # resumen = db.obtener_resumen_ventas_periodo(fecha_inicio, fecha_fin)
        # top_productos = db.obtener_top_productos_periodo(fecha_inicio, fecha_fin)
        resumen = {'total': 18500.75, 'efectivo': 12300.25, 'transferencia': 6200.50}
        top_productos = [("Producto A", 50), ("Producto C", 35), ("Producto B", 22)]

        # Guardamos los datos para poder usarlos en la descarga del PDF
        self.ultimos_datos_generados = (fecha_inicio_str, fecha_fin_str, resumen, top_productos)
        
        # --- Actualización de la UI ---
        tab.lbl_total_facturado.config(text=f"Facturación Total: ${resumen['total']:,.2f}")
        tab.lbl_total_efectivo.config(text=f"Total Efectivo: ${resumen['efectivo']:,.2f}")
        tab.lbl_total_transferencia.config(text=f"Total Transferencia: ${resumen['transferencia']:,.2f}")
        
        tab.tree_top_productos.delete(*tab.tree_top_productos.get_children())
        for producto, cantidad in top_productos:
            tab.tree_top_productos.insert("", "end", values=(producto, f"{cantidad} unidades"))
            
        self._actualizar_grafico_torta(resumen)
        tab.btn_pdf.config(state="normal")

    def _actualizar_grafico_torta(self, datos_resumen):
        """Dibuja o actualiza el gráfico de torta en el canvas de la pestaña."""
        tab = self.app.estadisticas_tab
        # Si ya existe un gráfico, lo destruimos para crear uno nuevo
        if tab.canvas_grafico_widget:
            tab.canvas_grafico_widget.destroy()

        labels = ['Efectivo', 'Transferencia']
        sizes = [datos_resumen.get('efectivo', 0), datos_resumen.get('transferencia', 0)]
        
        # Si no hay datos, mostramos un mensaje en lugar del gráfico
        if all(s == 0 for s in sizes):
            ttk.Label(tab.frame_grafico, text="No hay datos para mostrar.").pack(expand=True)
            return

        fig = Figure(figsize=(4, 4), dpi=100, facecolor='#303030')
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#28a745', '#007bff'],
               textprops={'color': 'white', 'fontsize': 10})
        ax.axis('equal')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=tab.frame_grafico)
        canvas.draw()
        widget_grafico = canvas.get_tk_widget()
        widget_grafico.pack(fill="both", expand=True)
        tab.canvas_grafico_widget = widget_grafico # Guardamos la referencia

    def descargar_reporte_estadisticas(self):
        """Genera y guarda un PDF con los últimos datos generados."""
        if not self.ultimos_datos_generados:
            self.app.notificar_error("Primero debe generar un reporte.")
            return
            
        # Desempaquetamos los datos guardados
        fecha_inicio, fecha_fin, resumen, top_productos = self.ultimos_datos_generados
        
        print(f"Generando reporte PDF desde {fecha_inicio} hasta {fecha_fin}...")
        # report_generator.generar_reporte_estadisticas_pdf(fecha_inicio, fecha_fin, resumen, top_productos)
        self.app.notificar_exito("Reporte de estadísticas generado (simulación).")
