import tkinter as tk
from datetime import date

# from ..database import database_manager as db

class CajaLogic:
    """
    Controlador especializado para la lógica de la pestaña de Caja.
    """
    def __init__(self, app_controller):
        self.app = app_controller

    def recargar_vista_caja(self):
        """
        Obtiene los datos de la caja para la fecha seleccionada en la UI
        y actualiza la vista, mostrando los widgets correspondientes.
        """
        fecha_str = self.app.caja_tab.cal_caja.entry.get()
        # ... (Lógica completa para obtener datos y actualizar cada widget de la UI) ...
        # Esta es una simulación simple
        print(f"Recargando vista de caja para la fecha: {fecha_str}")
        
        # Simulación de datos obtenidos de la DB
        cierre_dia = [("Efectivo", 1234.50), ("Transferencia", 678.90)]
        caja_hoy = (2000.0, None, None) # (fondo_inicial, monto_final, diferencia) -> Caja Abierta
        # caja_hoy = (2000.0, 3250.0, 15.50) # -> Caja Cerrada
        # caja_hoy = None # -> Sin Registro

        tab = self.app.caja_tab
        tab.frame_cierre_abierto.pack_forget()
        tab.frame_cierre_finalizado.pack_forget()

        if not caja_hoy:
            tab.lbl_estado_caja.config(text="SIN REGISTRO", foreground="grey")
            # ... (limpiar todos los labels) ...
            tab.btn_reporte_caja.config(state="disabled")
            tab.btn_ajustar_caja.config(state="disabled")
            return

        fondo_inicial, monto_final, diferencia = caja_hoy
        total_efectivo = sum(t for m, t in cierre_dia if m == "Efectivo")
        total_transferencia = sum(t for m, t in cierre_dia if m == "Transferencia")
        total_esperado = fondo_inicial + total_efectivo

        # Llenar labels
        tab.lbl_ventas_efectivo.config(text=f"${total_efectivo:,.2f}")
        tab.lbl_ventas_transferencia.config(text=f"${total_transferencia:,.2f}")
        tab.lbl_ventas_total.config(text=f"${total_efectivo + total_transferencia:,.2f}")
        tab.lbl_caja_fondo.config(text=f"${fondo_inicial:,.2f}")
        tab.lbl_caja_esperado.config(text=f"${total_esperado:,.2f}")
        
        tab.btn_reporte_caja.config(state="normal", command=lambda: self.descargar_reporte_caja(fecha_str))
        tab.btn_ajustar_caja.config(state="normal", command=lambda: self.ajustar_cierre_de_caja(fecha_str))

        if monto_final is None: # Caja abierta
            tab.lbl_estado_caja.config(text="🔓 CAJA ABIERTA", foreground="#d9534f")
            tab.frame_cierre_abierto.pack(pady=10)
            tab.entry_monto_final.delete(0, 'end')
            tab.btn_confirmar_corte.config(command=lambda: self.procesar_cierre_caja(fecha_str, total_esperado))
        else: # Caja cerrada
            tab.lbl_estado_caja.config(text="🔒 CAJA CERRADA", foreground="#28a745")
            tab.frame_cierre_finalizado.pack(pady=10)
            tab.lbl_caja_contado.config(text=f"${monto_final:,.2f}")
            tab.lbl_caja_diferencia.config(text=f"${diferencia:,.2f}")

    def procesar_cierre_caja(self, fecha_str, total_esperado):
        """Procesa la lógica para cerrar la caja del día."""
        monto_str = self.app.caja_tab.entry_monto_final.get()
        # ... (Validaciones, cálculos, llamada a la DB) ...
        print(f"Procesando cierre para {fecha_str} con monto {monto_str}")
        self.app.notificar_exito("Cierre de caja procesado (simulación).")
        self.recargar_vista_caja()

    def ajustar_cierre_de_caja(self, fecha_str):
        """Maneja el flujo para ajustar un cierre, incluyendo pedir PIN."""
        # ... (Lógica para mostrar pop-up de PIN y luego el de ajuste) ...
        print(f"Ajustando cierre para la fecha: {fecha_str}")

    def ir_a_hoy_caja(self):
        """Pone la fecha actual en el calendario y recarga la vista."""
        hoy_str = date.today().strftime("%d/%m/%Y")
        cal = self.app.caja_tab.cal_caja
        cal.entry.delete(0, tk.END)
        cal.entry.insert(0, hoy_str)
        self.recargar_vista_caja()
        
    def descargar_reporte_caja(self, fecha_str):
        """Llama al servicio de generación de reportes."""
        print(f"Descargando reporte para la fecha: {fecha_str}")
