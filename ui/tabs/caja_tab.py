import customtkinter as ctk
from ttkbootstrap.widgets import DateEntry

class CajaTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea la estructura estática de la pestaña. Se ejecuta una sola vez."""
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True)

        # Encabezado
        frame_encabezado = ctk.CTkFrame(frame_principal)
        frame_encabezado.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(frame_encabezado, text="DETALLE DE CAJA", font=("Segoe UI", 18, "bold")).pack(side="left")
        self.lbl_estado_caja = ctk.CTkLabel(frame_encabezado, text="Cargando...", font=("Segoe UI", 12, "bold"))
        self.lbl_estado_caja.pack(side="right")

        # Selector de Fecha
        frame_fecha = ctk.CTkFrame(frame_principal)
        frame_fecha.pack(pady=5)
        ctk.CTkLabel(frame_fecha, text="Ver fecha:", font=("Segoe UI", 11)).pack(side="left")
        self.cal_caja = DateEntry(frame_fecha, bootstyle="info", dateformat="%d/%m/%Y")
        self.cal_caja.pack(side="left", padx=5)
        ctk.CTkButton(frame_fecha, text="Cargar", command=self.controller.recargar_vista_caja).pack(side="left", padx=5)
        ctk.CTkButton(frame_fecha, text="Hoy", style="secondary.TButton", command=self.controller.ir_a_hoy_caja).pack(side="left", padx=5)

        # Contenedor de datos
        frame_contenedor = ctk.CTkFrame(frame_principal)
        frame_contenedor.pack(fill="both", expand=True, pady=10)
        frame_ventas = ctk.CTkFrame(frame_contenedor, text="RESUMEN DE VENTAS", padding=15)
        frame_ventas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        frame_caja = ctk.CTkFrame(frame_contenedor, text="INFORMACIÓN DE CAJA", padding=15)
        frame_caja.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Labels de información (se llenarán desde el controlador)
        self.lbl_ventas_efectivo = self._crear_fila_info(frame_ventas, "Ventas en Efectivo:", "$0.00")
        self.lbl_ventas_transferencia = self._crear_fila_info(frame_ventas, "Ventas en Transferencia:", "$0.00")
        ttk.Separator(frame_ventas, orient="horizontal").pack(fill="x", pady=5)
        self.lbl_ventas_total = self._crear_fila_info(frame_ventas, "TOTAL VENTAS:", "$0.00", bold=True)
        self.lbl_caja_fondo = self._crear_fila_info(frame_caja, "Fondo de Apertura:", "$0.00")
        self.lbl_caja_esperado = self._crear_fila_info(frame_caja, "Total Esperado:", "$0.00")

        # --- Frames dinámicos (el controlador decidirá cuál mostrar) ---
        frame_dinamico = ctk.CTkFrame(frame_principal)
        frame_dinamico.pack(fill="x", pady=15)
        
        # Frame para CAJA ABIERTA
        self.frame_cierre_abierto = ctk.CTkFrame(frame_dinamico)
        ctk.CTkLabel(self.frame_cierre_abierto, text="Monto Contado:", font=("Segoe UI", 11)).pack(side="left")
        self.entry_monto_final = ctk.CTkEntry(self.frame_cierre_abierto, width=15, font=("Segoe UI", 12, "bold"))
        self.entry_monto_final.pack(side="left", padx=10)
        self.btn_confirmar_corte = ctk.CTkButton(self.frame_cierre_abierto, text="✅ Confirmar Corte", style="danger.TButton")
        self.btn_confirmar_corte.pack(side="left")

        # Frame para CAJA CERRADA
        self.frame_cierre_finalizado = ctk.CTkFrame(frame_dinamico)
        self.lbl_caja_contado = self._crear_fila_info(self.frame_cierre_finalizado, "Monto contado:", "$0.00")
        self.lbl_caja_diferencia = self._crear_fila_info(self.frame_cierre_finalizado, "Diferencia:", "$0.00")
        
        # Botones de Acciones (siempre visibles)
        frame_acciones = ctk.CTkFrame(frame_principal)
        frame_acciones.pack(fill="x", pady=20)
        self.btn_reporte_caja = ctk.CTkButton(frame_acciones, text="📊 Descargar PDF", style="info.TButton", state="disabled", command=self.controller.descargar_reporte_caja)
        self.btn_reporte_caja.pack(side="left")
        self.btn_ajustar_caja = ctk.CTkButton(frame_acciones, text="⚙️ Ajustar Cierre", style="warning.TButton", state="disabled")
        self.btn_ajustar_caja.pack(side="left", padx=10)

    def _crear_fila_info(self, parent, texto, valor_inicial, bold=False):
        """Función de ayuda para crear filas de etiquetas."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=3)
        ctk.CTkLabel(frame, text=texto, width=25, anchor="w").pack(side="left")
        font = ("Segoe UI", 12, "bold") if bold else ("Segoe UI", 11)
        lbl_valor = ctk.CTkLabel(frame, text=valor_inicial, font=font, anchor="e")
        lbl_valor.pack(side="right")
        return lbl_valor
