import customtkinter as ctk
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import database_manager as db_manager
from services import report_generator

class EstadisticasLogic:
    
    def __init__(self, app_controller):
        self.app = app_controller
        self.ultimos_datos_generados = None

    def generar_estadisticas(self):
        tab = self.app.estadisticas_tab
        fecha_inicio_str = tab.cal_desde.get()
        fecha_fin_str = tab.cal_hasta.get()

        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
            fecha_fin_obj = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
            if fecha_inicio_obj > fecha_fin_obj:
                self.app.notificar_error("La fecha 'Desde' no puede ser posterior a la fecha 'Hasta'.")
                return

            fecha_inicio_db = fecha_inicio_obj.strftime("%Y-%m-%d")
            fecha_fin_db = fecha_fin_obj.strftime("%Y-%m-%d")

        except ValueError:
            self.app.notificar_error("Por favor, ingrese fechas válidas.")
            return

        resumen = db_manager.obtener_resumen_ventas_periodo(fecha_inicio_db, fecha_fin_db)
        top_productos = db_manager.obtener_top_productos_periodo(fecha_inicio_db, fecha_fin_db)

        self.ultimos_datos_generados = (fecha_inicio_str, fecha_fin_str, resumen, top_productos)
        
        tab.lbl_total_facturado.configure(text=f"Facturación Total: ${resumen['total']:,.2f}")
        tab.lbl_total_efectivo.configure(text=f"Total Efectivo: ${resumen['efectivo']:,.2f}")
        tab.lbl_total_transferencia.configure(text=f"Total Transferencia: ${resumen['transferencia']:,.2f}")
        
        tab.tree_top_productos.delete(*tab.tree_top_productos.get_children())
        for producto, cantidad in top_productos:
            tab.tree_top_productos.insert("", "end", values=(producto, f"{cantidad} unidades"))
            
        self._actualizar_grafico_torta(resumen)
        tab.btn_pdf.configure(state="normal")

    def _actualizar_grafico_torta(self, datos_resumen):
        """Dibuja o actualiza el gráfico de torta en el canvas de la pestaña."""
        tab = self.app.estadisticas_tab
        
        for widget in tab.frame_grafico.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Distribución" in widget.cget("text"):
                continue
            widget.destroy()

        labels = ['Efectivo', 'Transferencia']
        sizes = [datos_resumen.get('efectivo', 0), datos_resumen.get('transferencia', 0)]
        
        if all(s == 0 for s in sizes):
            ctk.CTkLabel(tab.frame_grafico, text="No hay datos para mostrar.").pack(expand=True)
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
        tab.canvas_grafico_widget = widget_grafico

    def descargar_reporte_estadisticas(self):
        if not self.ultimos_datos_generados:
            self.app.notificar_alerta("Primero debe generar un reporte en pantalla.")
            return
            
        fecha_inicio, fecha_fin, resumen, top_productos = self.ultimos_datos_generados
        
        exito, error_msg = report_generator.generar_reporte_estadisticas(
            fecha_inicio, fecha_fin, resumen, top_productos
        )

        if exito:
            self.app.notificar_exito("Reporte de estadísticas generado.")
        else:
            self.app.notificar_error(f"No se pudo generar el reporte: {error_msg}")