from datetime import date, datetime
from CTkMessagebox import CTkMessagebox
from database import database_manager as db_manager
from services import report_generator

class HistorialLogic:
    def __init__(self, app_controller):
        self.app = app_controller

    def recargar_historial_ventas(self):
        fecha_ui = self.app.historial_tab.cal_fecha_historial.get()
        
        try:
            fecha_db = datetime.strptime(fecha_ui, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            fecha_db = date.today().strftime("%Y-%m-%d")

        resumen_dia = db_manager.obtener_resumen_ventas_del_dia(fecha_db)
        historial = db_manager.obtener_historial_por_fecha(fecha_db)
        
        total_efectivo = sum(t for m, t in resumen_dia if m == "Efectivo")
        total_transferencia = sum(t for m, t in resumen_dia if m == "Transferencia")
        
        tab = self.app.historial_tab
        tab.lbl_total_efectivo.configure(text=f"Efectivo: ${total_efectivo:,.2f}")
        tab.lbl_total_transferencia.configure(text=f"Transferencia: ${total_transferencia:,.2f}")
        tab.lbl_total_general.configure(text=f"Total: ${total_efectivo + total_transferencia:,.2f}")

        tab.tree_historial.delete(*tab.tree_historial.get_children())
        
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
            if 'anulada' in tags:
                print(f"DEBUG: Item {id_t} insertado con tags: {tags}")
                print(f"DEBUG: Configuración actual del tag 'anulada': {tab.tree_historial.tag_configure('anulada')}")

    def anular_venta_seleccionada(self):
        tab = self.app.historial_tab
        seleccion = tab.tree_historial.selection()
        if not seleccion:
            self.app.notificar_alerta("Por favor, seleccione una venta para anular.")
            return

        item_seleccionado = seleccion[0]
        parent_id = tab.tree_historial.parent(item_seleccionado)
        id_transaccion = parent_id if parent_id else item_seleccionado
        
        item_actual = tab.tree_historial.item(id_transaccion)
        if 'anulada' in item_actual['tags']:
            self.app.notificar_alerta("Esta venta ya ha sido anulada.")
            return

        dialogo_confirmacion = CTkMessagebox(
            title="Confirmar Anulación", 
            message="¿Desea anular la venta seleccionada?\n\nEsta acción devolverá los productos al stock.",
            icon="warning",
            option_1="Cancelar",
            option_2="Anular Venta",
            sound=True,
            button_color="#D32F2F",
            button_hover_color="#B71C1C"
        )
        
        if dialogo_confirmacion.get() != "Anular Venta":
            self.app.notificar_alerta("Anulación cancelada.")
            return

        resultado_pin = self.app.app_logic.solicitar_pin_admin()

        if resultado_pin is False:
            self.app.notificar_error("PIN incorrecto. Anulación no autorizada.")
            return
        
        if resultado_pin is None:
            self.app.notificar_alerta("Anulación cancelada.")
            return

        exito = db_manager.anular_venta_existente(id_transaccion)
        
        if exito:
            self.app.notificar_exito("Venta anulada y stock restaurado correctamente.")
            self.recargar_historial_ventas()
            self.app.productos_logic.filtrar_productos_y_recargar()
            self.app.caja_logic.recargar_vista_caja()
            self.app.app_logic.actualizar_alertas_stock()
        else:
            self.app.notificar_error("No se pudo anular la venta en la base de datos.")


    def actualizar_estado_boton_anular(self, event=None):
        """Habilita o deshabilita el botón de anular según si hay una selección."""
        tab = self.app.historial_tab
        estado = "normal" if tab.tree_historial.selection() else "disabled"
        tab.btn_anular_venta.configure(state=estado)
        
    def deseleccionar_si_clic_vacio(self, event):
        """Si se hace clic en un área vacía del Treeview, deselecciona el ítem."""
        region = self.app.historial_tab.tree_historial.identify_region(event.x, event.y)
        if region == "nothing":
            self.app.historial_tab.tree_historial.selection_set('')
            
    def ir_a_hoy_historial(self):
        hoy_str = date.today().strftime("%d/%m/%Y")
        self.app.historial_tab.cal_fecha_historial.set(hoy_str) # Usamos .set()
        self.recargar_historial_ventas()

    def descargar_reporte_historial(self):
        fecha_ui = self.app.historial_tab.cal_fecha_historial.get()
        try:
            fecha_db = datetime.strptime(fecha_ui, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            self.app.notificar_error("Fecha inválida para generar el reporte.")
            return

        _, datos_cierre = db_manager.consultar_estado_caja(fecha_db)
        if not datos_cierre:
            self.app.notificar_alerta("No hay datos de caja para generar un reporte de esta fecha.")
            return

        resumen_ventas = db_manager.obtener_resumen_ventas_del_dia(fecha_db)
        historial_ventas = db_manager.obtener_historial_por_fecha(fecha_db)
        
        exito, error_msg = report_generator.generar_reporte_cierre_caja(
            datos_cierre, historial_ventas, resumen_ventas, fecha_ui
        )

        if exito:
            self.app.notificar_exito("Reporte PDF generado correctamente.")
        else:
            self.app.notificar_error(f"No se pudo generar el reporte: {error_msg}")