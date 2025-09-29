import customtkinter as ctk 
from tkinter import Toplevel
from datetime import date, datetime
from database import database_manager as db_manager
from services import report_generator 
from utilities import helpers
from utilities.dialogs import ConfirmacionDialog


class CajaLogic:
    """
    Controlador especializado para la lógica de la pestaña de Caja.
    """
    def __init__(self, app_controller):
        self.app = app_controller
        
    def procesar_cierre_caja(self, fecha_db, total_esperado):
        monto_final_str = self.app.caja_tab.entry_monto_final.get().strip()
        if not monto_final_str:
            self.app.notificar_alerta("Debe ingresar un monto para el cierre.")
            return

        dialogo = ConfirmacionDialog(
            parent=self.app,
            title="Confirmar Cierre de Caja",
            message=f"¿Está seguro de que desea cerrar la caja con un monto final de ${monto_final_str}?"
        )
        if not dialogo.show():
            self.app.notificar_alerta("Cierre de caja cancelado.")
            return

        try:
            monto_final = float(monto_final_str)
            diferencia = monto_final - total_esperado

            exito = db_manager.registrar_cierre_caja(fecha_db, monto_final, diferencia)

            if exito:
                self.app.notificar_exito("Caja cerrada correctamente.")
                self.recargar_vista_caja()
            else:
                self.app.notificar_error("No se pudo registrar el cierre de caja.")

        except (ValueError, TypeError):
            self.app.notificar_error("El monto ingresado no es un número válido.")
                
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
            tab.lbl_estado_caja.configure(text="SIN REGISTRO", text_color="grey")
            # Limpiamos todos los labels
            tab.lbl_ventas_efectivo.configure(text="$0.00")
            tab.lbl_ventas_transferencia.configure(text="$0.00")
            tab.lbl_ventas_total.configure(text="$0.00")
            tab.lbl_caja_fondo.configure(text="$0.00")
            tab.lbl_caja_esperado.configure(text="$0.00")
            tab.btn_reporte_caja.configure(state="disabled")
            tab.btn_ajustar_caja.configure(state="disabled")
            return

        # Si hay datos de caja, los procesamos
        fondo_inicial = datos_caja.get("fondo_inicial", 0.0)
        total_esperado = fondo_inicial + total_efectivo

        # Llenamos los labels de información
        tab.lbl_ventas_efectivo.configure(text=f"${total_efectivo:,.2f}")
        tab.lbl_ventas_transferencia.configure(text=f"${total_transferencia:,.2f}")
        tab.lbl_ventas_total.configure(text=f"${total_efectivo + total_transferencia:,.2f}")
        tab.lbl_caja_fondo.configure(text=f"${fondo_inicial:,.2f}")
        tab.lbl_caja_esperado.configure(text=f"${total_esperado:,.2f}")
        
        tab.btn_ajustar_caja.configure(command=lambda: self.ajustar_cierre_de_caja(fecha_ui))
        tab.btn_reporte_caja.configure(state="normal")
        tab.btn_ajustar_caja.configure(state="normal")

        if estado_caja == 'abierta':
            tab.lbl_estado_caja.configure(text="🔓 CAJA ABIERTA", text_color="#d9534f")
            tab.frame_cierre_abierto.pack(pady=10)
            tab.entry_monto_final.delete(0, 'end')
            # Conectamos el botón de confirmar con la lógica de cierre (que haremos después)
            tab.btn_confirmar_corte.configure(command=lambda: self.procesar_cierre_caja(fecha_db, total_esperado))
        
        elif estado_caja == 'cerrada':
            monto_final = datos_caja.get("contado_final", 0.0)
            diferencia = datos_caja.get("diferencia", 0.0)
            tab.lbl_estado_caja.configure(text="🔒 CAJA CERRADA", text_color="#28a745")
            tab.frame_cierre_finalizado.pack(pady=10)
            tab.lbl_caja_contado.configure(text=f"${monto_final:,.2f}")
            tab.lbl_caja_diferencia.configure(text=f"${diferencia:,.2f}")

    def ajustar_cierre_de_caja(self, fecha_ui):
        if not self.app.app_logic.solicitar_pin_admin():
            self.app.notificar_alerta("Operación cancelada o PIN incorrecto.")
            return

        # --- CORRECCIÓN DE TOPLEVEL Y WIDGETS ---
        dialogo_ajuste = ctk.CTkToplevel(self.app)
        dialogo_ajuste.title("Corregir Cierre de Caja")

        frame = ctk.CTkFrame(dialogo_ajuste)
        frame.pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=f"Nuevo monto final para el día {fecha_ui}:").pack(pady=5)
        entry_monto = ctk.CTkEntry(frame, width=200, font=("Segoe UI", 12))
        entry_monto.pack(pady=5)
        


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
        
        btn_confirmar = ctk.CTkButton(frame, text="Confirmar Ajuste", command=confirmar_ajuste)
        btn_confirmar.pack(pady=10)
        helpers.configurar_dialogo(dialogo_ajuste, self.app, entry_monto
        )
        entry_monto.bind("<Return>", lambda e: btn_confirmar.invoke())
        dialogo_ajuste.bind("<Escape>", lambda e: dialogo_ajuste.destroy())

    def ir_a_hoy_caja(self):
        """Pone la fecha actual en el calendario de la caja y recarga la vista."""
        helpers.ir_a_hoy_y_recargar(
            self.app.caja_tab.cal_caja,      
            self.recargar_vista_caja        
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
