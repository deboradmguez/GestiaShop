import tkinter as tk
from datetime import date, datetime
from ..ui.utilities.dialogs import ConfirmacionDialog

# from ..database import database_manager as db
# from ..services import report_generator as report # Para generar PDF

class HistorialLogic:
    """
    Controlador especializado para la lógica de la pestaña de Historial de Ventas.
    """
    def __init__(self, app_controller):
        self.app = app_controller

    def recargar_historial_ventas(self):
        """
        Obtiene los datos del historial para la fecha seleccionada en la UI
        y actualiza la vista (tabla y totales).
        """
        fecha_str = self.app.historial_tab.cal_fecha_historial.entry.get()
        if not fecha_str:
            fecha_str = date.today().strftime("%d/%m/%Y")
        
        # --- Lógica de Base de Datos (simulada) ---
        # cierre_dia = db.obtener_cierre_caja_del_dia(fecha_db)
        # historial = db.obtener_historial_ventas_detallado(fecha_db)
        cierre_dia = [("Efectivo", 1500.0), ("Transferencia", 500.0)]
        historial = [
            ("tx1", "2025-09-24 10:30:00", "Producto A", 2, 150, 300, 0, 300, "Completada", "101"),
            ("tx2", "2025-09-24 11:15:00", "Producto B", 1, 200, 0, 200, 200, "Anulada", "102")
        ]
        
        # --- Actualización de la UI ---
        tab = self.app.historial_tab
        total_efectivo = sum(t for m, t in cierre_dia if m == "Efectivo")
        total_transferencia = sum(t for m, t in cierre_dia if m == "Transferencia")
        
        tab.lbl_total_efectivo.config(text=f"Efectivo: ${total_efectivo:,.2f}")
        tab.lbl_total_transferencia.config(text=f"Transferencia: ${total_transferencia:,.2f}")
        tab.lbl_total_general.config(text=f"Total: ${total_efectivo + total_transferencia:,.2f}")

        tab.tree_historial.delete(*tab.tree_historial.get_children())
        
        # Lógica para agrupar y mostrar los datos en la tabla (sin cambios)
        ventas_agrupadas = {}
        for id_t, fecha_h, nom, cant, prec, p_ef, p_tr, total_f, est, tick in historial:
            if id_t not in ventas_agrupadas:
                ventas_agrupadas[id_t] = {'fecha_hora': fecha_h, 'detalles': [], 'total_efectivo': p_ef, 'total_transferencia': p_tr, 'total_venta_completa': 0.0, 'estado': est, 'ticket_numero': tick}
            if total_f is not None:
                ventas_agrupadas[id_t]['detalles'].append((nom, cant, prec, total_f))
                ventas_agrupadas[id_t]['total_venta_completa'] += total_f
        
        for id_t, venta in ventas_agrupadas.items():
            dt = datetime.strptime(venta['fecha_hora'], "%Y-%m-%d %H:%M:%S")
            metodo = "Mixto" if venta['total_efectivo'] > 0 and venta['total_transferencia'] > 0 else "Efectivo" if venta['total_efectivo'] > 0 else "Transferencia"
            tags = ['parent']
            texto = f"Ticket #{venta['ticket_numero']} | Método: {metodo}"
            if venta['estado'] == 'Anulada':
                tags.append('anulada'); texto = f"[ANULADA] {texto}"
            
            tab.tree_historial.insert("", "end", iid=id_t, values=(dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M"), texto, "", "", f"${venta['total_efectivo']:.2f}", f"${venta['total_transferencia']:.2f}", f"${venta['total_venta_completa']:.2f}"), tags=tags)
            
            child_tags = ['child', 'anulada'] if venta['estado'] == 'Anulada' else ['child']
            for nom, cant, prec, total_f in venta['detalles']:
                tab.tree_historial.insert(id_t, "end", values=("", "", nom, cant, f"${prec or 0:.2f}", "", "", f"${total_f or 0:.2f}"), tags=child_tags)

    def anular_venta_seleccionada(self):
        """Procesa la anulación de la venta seleccionada en la tabla."""
        tab = self.app.historial_tab
        seleccion = tab.tree_historial.selection()
        if not seleccion: return

        item_seleccionado = seleccion[0]
        parent_id = tab.tree_historial.parent(item_seleccionado)
        id_transaccion = parent_id if parent_id else item_seleccionado
        
        # Lógica de confirmación y anulación... (simulada)
        dialogo = ConfirmacionDialog(
            parent=self.app, 
            title="Confirmar Acción", 
            message=f"¿Desea anular la venta con ID {id_transaccion}?"
        )
        
        respuesta = dialogo.show()
        if respuesta:
            print(f"Anulando venta {id_transaccion}...")
            # exito = db.anular_venta(id_transaccion)
            # if exito:
            self.app.notificar_exito("Venta anulada y stock restaurado.")
            self.recargar_historial_ventas()
            # self.app.productos_logic.filtrar_productos_y_recargar() # Notificar a otras lógicas

    def actualizar_estado_boton_anular(self, event=None):
        """Habilita o deshabilita el botón de anular según si hay una selección."""
        tab = self.app.historial_tab
        estado = "normal" if tab.tree_historial.selection() else "disabled"
        tab.btn_anular_venta.config(state=estado)
        
    def deseleccionar_si_clic_vacio(self, event):
        """Si se hace clic en un área vacía del Treeview, deselecciona el ítem."""
        region = self.app.historial_tab.tree_historial.identify_region(event.x, event.y)
        if region == "nothing":
            self.app.historial_tab.tree_historial.selection_set('')
            
    def ir_a_hoy_historial(self):
        """Pone la fecha de hoy en el calendario y recarga la vista."""
        hoy_str = date.today().strftime("%d/%m/%Y")
        cal = self.app.historial_tab.cal_fecha_historial
        cal.entry.delete(0, tk.END)
        cal.entry.insert(0, hoy_str)
        self.recargar_historial_ventas()

    def descargar_reporte_historial(self):
        """Genera y abre un reporte en PDF del historial del día seleccionado."""
        fecha_str = self.app.historial_tab.cal_fecha_historial.entry.get()
        print(f"Generando reporte para la fecha: {fecha_str}...")
        # report.reporte_cierre_caja(fecha_str)
        self.app.notificar_exito(f"Reporte PDF para {fecha_str} generado (simulación).")
