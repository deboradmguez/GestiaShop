import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry

class HistorialTab(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller

        # Intentamos cargar el ícono, si falla, el botón no tendrá imagen.
        try:
            self.icono_descargar = tk.PhotoImage(file=self.controller.ruta_recurso("icons/descargar.png"))
        except tk.TclError:
            self.icono_descargar = None

        self._crear_panel_controles()
        self._crear_panel_resumen()
        self._crear_vista_historial()
        self._crear_panel_acciones()
        self._configurar_bindings_globales()

    def _crear_panel_controles(self):
        """Crea el panel superior para la selección de fecha."""
        frame_controles = ttk.Frame(self)
        frame_controles.pack(fill="x", pady=5)

        ttk.Label(frame_controles, text="Ver ventas del:", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.cal_fecha_historial = DateEntry(frame_controles, dateformat="%d/%m/%Y")
        self.cal_fecha_historial.pack(side="left", padx=5)
        
        btn_recargar = ttk.Button(
            frame_controles, text="Cargar Historial", style="info.TButton",
            # Llama al método delegado del controlador
            command=lambda: self.controller.recargar_historial_ventas()
        )
        btn_recargar.pack(side="left", padx=5)

        btn_hoy = ttk.Button(
            frame_controles, text="Hoy", style="secondary.TButton",
            # Llama a un método de utilidad del controlador
            command=self.controller.ir_a_hoy_historial
        )
        btn_hoy.pack(side="left", padx=5)

    def _crear_panel_resumen(self):
        """Crea las etiquetas para los totales del día."""
        frame_resumen = ttk.Frame(self)
        frame_resumen.pack(fill="x", pady=5)
        
        self.lbl_total_efectivo = ttk.Label(frame_resumen, text="Efectivo: $0.00", font=("Segoe UI", 12))
        self.lbl_total_efectivo.pack(side="left", padx=5)
        
        self.lbl_total_transferencia = ttk.Label(frame_resumen, text="Transferencia: $0.00", font=("Segoe UI", 12))
        self.lbl_total_transferencia.pack(side="left", padx=5)
        
        self.lbl_total_general = ttk.Label(frame_resumen, text="Total: $0.00", font=("Segoe UI", 12, "bold"))
        self.lbl_total_general.pack(side="right", padx=5)

    def _crear_vista_historial(self):
        """Crea la tabla (Treeview) para mostrar el historial."""
        self.tree_historial = ttk.Treeview(
            self,
            columns=("fecha", "hora", "desc", "cant", "p_unit", "p_efec", "p_trans", "total"),
            show="headings"
        )
        self.tree_historial.pack(fill="both", expand=True, pady=5)

        # Configuración de tags y columnas... (sin cambios)
        self.tree_historial.tag_configure("anulada", foreground="red")
        self.tree_historial.tag_configure("parent", font=("Segoe UI", 10, "bold"))
        self.tree_historial.tag_configure("child", font=("Segoe UI", 9))
        self.tree_historial.heading("fecha", text="Fecha"); self.tree_historial.column("fecha", width=80)
        self.tree_historial.heading("hora", text="Hora"); self.tree_historial.column("hora", width=60)
        self.tree_historial.heading("desc", text="Descripción"); self.tree_historial.column("desc", width=400)
        self.tree_historial.heading("cant", text="Cant."); self.tree_historial.column("cant", width=50, anchor="e")
        self.tree_historial.heading("p_unit", text="P. Unit."); self.tree_historial.column("p_unit", width=80, anchor="e")
        self.tree_historial.heading("p_efec", text="Efectivo"); self.tree_historial.column("p_efec", width=80, anchor="e")
        self.tree_historial.heading("p_trans", text="Transf."); self.tree_historial.column("p_trans", width=80, anchor="e")
        self.tree_historial.heading("total", text="Total"); self.tree_historial.column("total", width=80, anchor="e")

    def _crear_panel_acciones(self):
        """Crea los botones de acción en la parte inferior."""
        frame_acciones = ttk.Frame(self)
        frame_acciones.pack(fill="x", side="bottom", pady=5)
        
        self.btn_generar_pdf = ttk.Button(
            frame_acciones, text="Descargar PDF", image=self.icono_descargar, compound="left",
            style="success.TButton",
            # Llama al método delegado del controlador
            command=self.controller.descargar_reporte_historial
        )
        self.btn_generar_pdf.pack(side="left", padx=5, pady=5)

        self.btn_anular_venta = ttk.Button(
            frame_acciones, text="Anular Venta Seleccionada",
            style="danger.TButton", state="disabled",
            # Llama al método delegado del controlador
            command=self.controller.anular_venta_seleccionada
        )
        self.btn_anular_venta.pack(side="left", padx=5, pady=5)

    def _configurar_bindings_globales(self):
        """Configura eventos que necesitan interactuar con otros widgets."""
        # Se llama al controller para actualizar el estado del botón
        self.tree_historial.bind("<<TreeviewSelect>>", self.controller.actualizar_estado_boton_anular)
        # El controller se encarga de la lógica de deselección
        self.tree_historial.bind("<Button-1>", self.controller.deseleccionar_si_clic_vacio, add='+')
