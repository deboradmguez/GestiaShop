import tkinter as tk
from ttkbootstrap import ttk
from tkinter import Toplevel
from datetime import date, datetime
from database import database_manager as db_manager
from services import report_generator 
from utilities import helpers

class CajaLogic:
    """
    Controlador especializado para la lógica de la pestaña de Caja.
    """
    def __init__(self, app_controller):
        self.app = app_controller
    def recargar_vista_caja(self):
        
        fecha_ui = self.app.caja_tab.cal_caja.entry.get()
        try:
            fecha_db = datetime.strptime(fecha_ui, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            fecha_db = date.today().strftime("%Y-%m-%d")

        estado_caja, datos_caja = db_manager.consultar_estado_caja(fecha_db)
        resumen_ventas = db_manager.obtener_resumen_ventas_del_dia(fecha_db)

        total_efectivo = sum(t for m, t in resumen_ventas if m == "Efectivo")
        total_transferencia = sum(t for m, t in resumen_ventas if m == "Transferencia")
        
        tab = self.app.caja_tab
        tab.frame_cierre_abierto.pack_forget()
        tab.frame_cierre_finalizado.pack_forget()

        if estado_caja == 'inexistente' or estado_caja == 'error':
            tab.lbl_estado_caja.config(text="SIN REGISTRO", foreground="grey")
            # Limpiamos todos los labels
            tab.lbl_ventas_efectivo.config(text="$0.00")
            tab.lbl_ventas_transferencia.config(text="$0.00")
            tab.lbl_ventas_total.config(text="$0.00")
            tab.lbl_caja_fondo.config(text="$0.00")
            tab.lbl_caja_esperado.config(text="$0.00")
            tab.btn_reporte_caja.config(state="disabled")
            tab.btn_ajustar_caja.config(state="disabled")
            return

        # Si hay datos de caja, los procesamos
        fondo_inicial = datos_caja.get("fondo_inicial", 0.0)
        total_esperado = fondo_inicial + total_efectivo

        # Llenamos los labels de información
        tab.lbl_ventas_efectivo.config(text=f"${total_efectivo:,.2f}")
        tab.lbl_ventas_transferencia.config(text=f"${total_transferencia:,.2f}")
        tab.lbl_ventas_total.config(text=f"${total_efectivo + total_transferencia:,.2f}")
        tab.lbl_caja_fondo.config(text=f"${fondo_inicial:,.2f}")
        tab.lbl_caja_esperado.config(text=f"${total_esperado:,.2f}")
        
        tab.btn_reporte_caja.config(state="normal")
        tab.btn_ajustar_caja.config(state="normal")

        if estado_caja == 'abierta':
            tab.lbl_estado_caja.config(text="🔓 CAJA ABIERTA", foreground="#d9534f")
            tab.frame_cierre_abierto.pack(pady=10)
            tab.entry_monto_final.delete(0, 'end')
            # Conectamos el botón de confirmar con la lógica de cierre (que haremos después)
            tab.btn_confirmar_corte.config(command=lambda: self.procesar_cierre_caja(fecha_db, total_esperado))
        
        elif estado_caja == 'cerrada':
            monto_final = datos_caja.get("contado_final", 0.0)
            diferencia = datos_caja.get("diferencia", 0.0)
            tab.lbl_estado_caja.config(text="🔒 CAJA CERRADA", foreground="#28a745")
            tab.frame_cierre_finalizado.pack(pady=10)
            tab.lbl_caja_contado.config(text=f"${monto_final:,.2f}")
            tab.lbl_caja_diferencia.config(text=f"${diferencia:,.2f}")

    def procesar_cierre_caja(self, fecha_db, total_esperado):
        monto_str = self.app.caja_tab.entry_monto_final.get()
        
        try:
            if not monto_str:
                self.app.notificar_alerta("Debe ingresar el monto contado.")
                return
            
            monto_final = float(monto_str.replace(',', '.'))
            diferencia = monto_final - total_esperado

            # 2. Llamamos al database_manager para guardar los datos
            exito = db_manager.registrar_cierre_caja(fecha_db, monto_final, diferencia)

            if exito:
                self.app.notificar_exito("Corte de caja registrado con éxito.")
                # 3. Recargamos la vista para que se actualice a "Caja Cerrada"
                self.recargar_vista_caja()
            else:
                self.app.notificar_error("No se pudo guardar el cierre de caja.")

        except (ValueError, TypeError):
            self.app.notificar_error("El monto ingresado no es un número válido.")

    def ajustar_cierre_de_caja(self, fecha_ui):
        
        if not self.app.app_logic.solicitar_pin_admin():
            self.app.notificar_alerta("Operación cancelada o PIN incorrecto.")
            return

        dialogo_ajuste = Toplevel(self.app)
        dialogo_ajuste.title("Corregir Cierre de Caja")
        dialogo_ajuste.transient(self.app)
        dialogo_ajuste.grab_set()

        frame = ttk.Frame(dialogo_ajuste, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Nuevo monto final para el día {fecha_ui}:").pack(pady=5)
        entry_monto = ttk.Entry(frame, width=20, font=("Segoe UI", 12))
        entry_monto.pack(pady=5)
        entry_monto.focus()

        def confirmar_ajuste():
            try:
                monto_corregido = float(entry_monto.get().strip())
                fecha_db = datetime.strptime(fecha_ui, "%d/%m/%Y").strftime("%Y-%m-%d")

                # Recalculamos la diferencia
                resumen_ventas = db_manager.obtener_resumen_ventas_del_dia(fecha_db)
                total_efectivo = sum(t for m, t in resumen_ventas if m == "Efectivo")
                
                _, datos_caja = db_manager.consultar_estado_caja(fecha_db)
                fondo_inicial = datos_caja.get("fondo_inicial", 0.0)
                
                total_esperado = fondo_inicial + total_efectivo
                diferencia_corregida = monto_corregido - total_esperado
                
                # Guardamos los cambios en la base de datos
                exito = db_manager.registrar_ajuste_caja(fecha_db, monto_corregido, diferencia_corregida)

                if exito:
                    self.app.notificar_exito("Cierre de caja ajustado correctamente.")
                    dialogo_ajuste.destroy()
                    self.recargar_vista_caja()
                else:
                    self.app.notificar_error("No se pudo ajustar el cierre de caja.")

            except (ValueError, TypeError):
                self.app.notificar_error("El monto ingresado no es un número válido.")
        
        btn_confirmar = ttk.Button(frame, text="Confirmar Ajuste", command=confirmar_ajuste)
        btn_confirmar.pack(pady=10)
        entry_monto.bind("<Return>", lambda e: btn_confirmar.invoke())
        dialogo_ajuste.bind("<Escape>", lambda e: dialogo_ajuste.destroy())

    def ir_a_hoy_caja(self):
        """Pone la fecha actual en el calendario de la caja y recarga la vista."""
        helpers.ir_a_hoy_y_recargar(
            self.app.caja_tab.cal_caja,      # Le pasamos el calendario de la caja
            self.recargar_vista_caja        # Le pasamos la función de recarga de la caja
        )
        
    def descargar_reporte_caja(self):
        fecha_ui = self.app.caja_tab.cal_caja.entry.get()
        try:
            fecha_db = datetime.strptime(fecha_ui, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            self.app.notificar_error("Fecha inválida para generar el reporte.")
            return

        # 1. Recolectamos todos los datos necesarios desde el db_manager
        _, datos_cierre = db_manager.consultar_estado_caja(fecha_db)
        if not datos_cierre:
            self.app.notificar_alerta("No hay datos de caja para esta fecha.")
            return

        resumen_ventas = db_manager.obtener_resumen_ventas_del_dia(fecha_db)
        historial_ventas = db_manager.obtener_historial_por_fecha(fecha_db)
        
        # 2. Llamamos al servicio para que genere el PDF
        exito, error_msg = report_generator.generar_reporte_cierre_caja(
            datos_cierre, historial_ventas, resumen_ventas, fecha_ui
        )

        if exito:
            self.app.notificar_exito("Reporte PDF generado correctamente.")
        else:
            self.app.notificar_error(f"No se pudo generar el reporte: {error_msg}")
