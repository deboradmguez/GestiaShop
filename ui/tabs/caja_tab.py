import customtkinter as ctk
from datetime import datetime

class CajaTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")  # Fondo transparente
        self.controller = controller
        self._crear_widgets()
        
    def _crear_widgets(self):
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Encabezado con mejor styling
        frame_encabezado = ctk.CTkFrame(frame_principal, corner_radius=10)
        frame_encabezado.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            frame_encabezado, 
            text="DETALLE DE CAJA", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=10)
        
        self.lbl_estado_caja = ctk.CTkLabel(
            frame_encabezado, 
            text="Cargando...", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_estado_caja.pack(side="right", padx=20, pady=10)

        # Frame de fecha con mejor integración
        frame_fecha = ctk.CTkFrame(frame_principal, corner_radius=8)
        frame_fecha.pack(pady=5)
        
        ctk.CTkLabel(
            frame_fecha, 
            text="Ver fecha:", 
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(10, 5), pady=10)
        
        self.cal_caja = ctk.CTkEntry(frame_fecha, placeholder_text="dd/mm/aaaa")
        self.cal_caja.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.cal_caja.pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            frame_fecha, 
            text="Cargar", 
            command=self.controller.recargar_vista_caja
        ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            frame_fecha, 
            text="Hoy", 
            command=self.controller.ir_a_hoy_caja
        ).pack(side="left", padx=5, pady=10)

        # Contenedor de datos con mejor styling
        frame_contenedor = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_contenedor.pack(fill="both", expand=True, pady=10)

        # Frame de Ventas con bordes redondeados
        frame_ventas = ctk.CTkFrame(frame_contenedor, corner_radius=10, border_width=2)
        frame_ventas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(
            frame_ventas, 
            text="RESUMEN DE VENTAS", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        # Frame de Caja con bordes redondeados
        frame_caja = ctk.CTkFrame(frame_contenedor, corner_radius=10, border_width=2)
        frame_caja.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(
            frame_caja, 
            text="INFORMACIÓN DE CAJA", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))

        # Labels de información mejorados
        self.lbl_ventas_efectivo = self._crear_fila_info(frame_ventas, "Ventas en Efectivo:", "$0.00")
        self.lbl_ventas_transferencia = self._crear_fila_info(frame_ventas, "Ventas en Transferencia:", "$0.00")
        
        # Separador más elegante
        separador = ctk.CTkFrame(frame_ventas, height=2, corner_radius=1)
        separador.pack(fill="x", pady=10, padx=20)
        
        self.lbl_ventas_total = self._crear_fila_info(frame_ventas, "TOTAL VENTAS:", "$0.00", bold=True)
        self.lbl_caja_fondo = self._crear_fila_info(frame_caja, "Fondo de Apertura:", "$0.00")
        self.lbl_caja_esperado = self._crear_fila_info(frame_caja, "Total Esperado:", "$0.00")

        # Frames dinámicos mejorados
        frame_dinamico = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_dinamico.pack(fill="x", pady=15)
        
        self.frame_cierre_abierto = ctk.CTkFrame(frame_dinamico, corner_radius=8)
        self.frame_cierre_abierto.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            self.frame_cierre_abierto, 
            text="Monto Contado:", 
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(15, 5), pady=15)
        
        self.entry_monto_final = ctk.CTkEntry(
            self.frame_cierre_abierto, 
            width=150, 
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=6
        )
        self.entry_monto_final.pack(side="left", padx=10, pady=15)
        
        self.btn_confirmar_corte = ctk.CTkButton(
            self.frame_cierre_abierto, 
            text="✅ Confirmar Corte", 
            fg_color="#D32F2F", 
            hover_color="#B71C1C",
            corner_radius=6
        )
        self.btn_confirmar_corte.pack(side="left", padx=(5, 15), pady=15)

        self.frame_cierre_finalizado = ctk.CTkFrame(frame_dinamico, corner_radius=8)
        self.lbl_caja_contado = self._crear_fila_info(self.frame_cierre_finalizado, "Monto contado:", "$0.00")
        self.lbl_caja_diferencia = self._crear_fila_info(self.frame_cierre_finalizado, "Diferencia:", "$0.00")
        
        # Botones de Acciones mejorados
        frame_acciones = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_acciones.pack(fill="x", pady=20)
        
        self.btn_reporte_caja = ctk.CTkButton(
            frame_acciones, 
            text="📊 Descargar PDF", 
            state="disabled", 
            command=self.controller.descargar_reporte_caja,
            corner_radius=8
        )
        self.btn_reporte_caja.pack(side="left", padx=(0, 10))
        
        self.btn_ajustar_caja = ctk.CTkButton(
            frame_acciones, 
            text="⚙️ Ajustar Cierre", 
            state="disabled", 
            fg_color="#f0ad4e", 
            text_color="black",
            corner_radius=8
        )
        self.btn_ajustar_caja.pack(side="left")
        self.entry_monto_final.bind("<Return>", lambda e: self.btn_confirmar_corte.invoke())

    def _crear_fila_info(self, parent, texto, valor_inicial, bold=False):
        """Función de ayuda para crear filas de etiquetas mejoradas."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5, padx=15)
        
        ctk.CTkLabel(
            frame, 
            text=texto, 
            anchor="w",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")
        
        font_weight = "bold" if bold else "normal"
        font_size = 13 if bold else 11
        
        lbl_valor = ctk.CTkLabel(
            frame, 
            text=valor_inicial, 
            font=ctk.CTkFont(size=font_size, weight=font_weight), 
            anchor="e"
        )
        lbl_valor.pack(side="right")
        return lbl_valor