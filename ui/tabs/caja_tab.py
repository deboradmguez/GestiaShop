import customtkinter as ctk
from tkinter import ttk 
from ttkbootstrap.widgets import DateEntry 

class CajaTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) 
        self.controller = controller
        self._crear_widgets()

    def _crear_widgets(self):
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Encabezado
        frame_encabezado = ctk.CTkFrame(frame_principal)
        frame_encabezado.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(frame_encabezado, text="DETALLE DE CAJA", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=10)
        self.lbl_estado_caja = ctk.CTkLabel(frame_encabezado, text="Cargando...", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_estado_caja.pack(side="right", padx=10)

        frame_fecha = ctk.CTkFrame(frame_principal)
        frame_fecha.pack(pady=5)
        ctk.CTkLabel(frame_fecha, text="Ver fecha:", font=("Segoe UI", 11)).pack(side="left")
        self.cal_caja = DateEntry(frame_fecha, bootstyle="info", dateformat="%d/%m/%Y") # Se añadirá al final
        self.cal_caja.pack(side="left", padx=5)
        ctk.CTkButton(frame_fecha, text="Cargar", command=self.controller.recargar_vista_caja).pack(side="left", padx=5)
        ctk.CTkButton(frame_fecha, text="Hoy", command=self.controller.ir_a_hoy_caja).pack(side="left", padx=5)

        # Contenedor de datos
        frame_contenedor = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_contenedor.pack(fill="both", expand=True, pady=10)

        # --- Frame de Ventas (Simulando LabelFrame) ---
        frame_ventas = ctk.CTkFrame(frame_contenedor, border_width=1)
        frame_ventas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(frame_ventas, text="RESUMEN DE VENTAS", font=ctk.CTkFont(weight="bold")).pack(pady=(5,10))
        
        # --- Frame de Caja (Simulando LabelFrame) ---
        frame_caja = ctk.CTkFrame(frame_contenedor, border_width=1)
        frame_caja.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(frame_caja, text="INFORMACIÓN DE CAJA", font=ctk.CTkFont(weight="bold")).pack(pady=(5,10))

        # Labels de información (se llenarán desde el controlador)
        self.lbl_ventas_efectivo = self._crear_fila_info(frame_ventas, "Ventas en Efectivo:", "$0.00")
        self.lbl_ventas_transferencia = self._crear_fila_info(frame_ventas, "Ventas en Transferencia:", "$0.00")
        
        # Separador moderno
        ctk.CTkFrame(frame_ventas, height=1, fg_color="gray50").pack(fill="x", pady=5, padx=10)
        
        self.lbl_ventas_total = self._crear_fila_info(frame_ventas, "TOTAL VENTAS:", "$0.00", bold=True)
        self.lbl_caja_fondo = self._crear_fila_info(frame_caja, "Fondo de Apertura:", "$0.00")
        self.lbl_caja_esperado = self._crear_fila_info(frame_caja, "Total Esperado:", "$0.00")

        # --- Frames dinámicos ---
        frame_dinamico = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_dinamico.pack(fill="x", pady=15)
        
        self.frame_cierre_abierto = ctk.CTkFrame(frame_dinamico, fg_color="transparent")
        ctk.CTkLabel(self.frame_cierre_abierto, text="Monto Contado:", font=("Segoe UI", 11)).pack(side="left")
        self.entry_monto_final = ctk.CTkEntry(self.frame_cierre_abierto, width=150, font=ctk.CTkFont(size=12, weight="bold"))
        self.entry_monto_final.pack(side="left", padx=10)
        self.btn_confirmar_corte = ctk.CTkButton(self.frame_cierre_abierto, text="✅ Confirmar Corte", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_confirmar_corte.pack(side="left")

        self.frame_cierre_finalizado = ctk.CTkFrame(frame_dinamico, fg_color="transparent")
        self.lbl_caja_contado = self._crear_fila_info(self.frame_cierre_finalizado, "Monto contado:", "$0.00")
        self.lbl_caja_diferencia = self._crear_fila_info(self.frame_cierre_finalizado, "Diferencia:", "$0.00")
        
        # Botones de Acciones
        frame_acciones = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_acciones.pack(fill="x", pady=20)
        self.btn_reporte_caja = ctk.CTkButton(frame_acciones, text="📊 Descargar PDF", state="disabled", command=self.controller.descargar_reporte_caja)
        self.btn_reporte_caja.pack(side="left")
        self.btn_ajustar_caja = ctk.CTkButton(frame_acciones, text="⚙️ Ajustar Cierre", state="disabled", fg_color="#f0ad4e", text_color="black")
        self.btn_ajustar_caja.pack(side="left", padx=10)

    def _crear_fila_info(self, parent, texto, valor_inicial, bold=False):
        """Función de ayuda para crear filas de etiquetas."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=3, padx=10)
        
        ctk.CTkLabel(frame, text=texto, anchor="w").pack(side="left")
        
        font_weight = "bold" if bold else "normal"
        lbl_valor = ctk.CTkLabel(frame, text=valor_inicial, font=ctk.CTkFont(family="Segoe UI", size=12, weight=font_weight), anchor="e")
        lbl_valor.pack(side="right")
        return lbl_valor