import customtkinter as ctk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry
from PIL import Image
import tkinter as tk

class HistorialTab(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent) # Se elimina el argumento 'padding'
        self.controller = controller

        # --- MANEJO DE IMÁGENES CORREGIDO ---
        try:
            ruta_icono = self.controller.ruta_recurso("icons/descargar.png")
            self.icono_descargar = ctk.CTkImage(Image.open(ruta_icono))
        except Exception as e:
            print(f"Error al cargar icono de descarga: {e}")
            self.icono_descargar = None

        self._crear_panel_controles()
        self._crear_panel_resumen()
        self._crear_vista_historial()
        self._crear_panel_acciones()
        self._configurar_bindings_globales()

    def _crear_panel_controles(self):
        """Crea el panel superior para la selección de fecha."""
        frame_controles = ctk.CTkFrame(self)
        frame_controles.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(frame_controles, text="Ver ventas del:", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.cal_fecha_historial = DateEntry(frame_controles, dateformat="%d/%m/%Y")
        self.cal_fecha_historial.pack(side="left", padx=5)
        
        btn_recargar = ctk.CTkButton(
            frame_controles, text="Cargar Historial",
            command=lambda: self.controller.recargar_historial_ventas()
        )
        btn_recargar.pack(side="left", padx=5)

        btn_hoy = ctk.CTkButton(
            frame_controles, text="Hoy",
            command=self.controller.ir_a_hoy_historial
        )
        btn_hoy.pack(side="left", padx=5)

    def _crear_panel_resumen(self):
        """Crea las etiquetas para los totales del día."""
        frame_resumen = ctk.CTkFrame(self)
        frame_resumen.pack(fill="x", pady=5, padx=10)
        
        self.lbl_total_efectivo = ctk.CTkLabel(frame_resumen, text="Efectivo: $0.00", font=("Segoe UI", 12))
        self.lbl_total_efectivo.pack(side="left", padx=10)
        
        self.lbl_total_transferencia = ctk.CTkLabel(frame_resumen, text="Transferencia: $0.00", font=("Segoe UI", 12))
        self.lbl_total_transferencia.pack(side="left", padx=10)
        
        self.lbl_total_general = ctk.CTkLabel(frame_resumen, text="Total: $0.00", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_total_general.pack(side="right", padx=10)

    def _crear_vista_historial(self):
        """Crea la tabla (Treeview) para mostrar el historial."""
        tree_container = ctk.CTkFrame(self)
        tree_container.pack(fill="both", expand=True, pady=5, padx=10)

        # --- Estilizado del Treeview para que combine con el tema ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#3470b8')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0)

        self.tree_historial = ttk.Treeview(
            tree_container,
            columns=("fecha", "hora", "desc", "cant", "p_unit", "p_efec", "p_trans", "total"),
            show="headings"
        )
        self.tree_historial.pack(side="left", fill="both", expand=True)

        # --- Scrollbar de CustomTkinter ---
        scrollbar = ctk.CTkScrollbar(tree_container, command=self.tree_historial.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_historial.configure(yscrollcommand=scrollbar.set)

        self.tree_historial.tag_configure("anulada", foreground="#ff5555")
        self.tree_historial.tag_configure("parent", font=("Segoe UI", 10, "bold"))
        self.tree_historial.tag_configure("child", font=("Segoe UI", 9))
        self.tree_historial.heading("fecha", text="Fecha"); self.tree_historial.column("fecha", width=80)
        self.tree_historial.heading("hora", text="Hora"); self.tree_historial.column("hora", width=60)
        self.tree_historial.heading("desc", text="Descripción"); self.tree_historial.column("desc", width=300)
        self.tree_historial.heading("cant", text="Cant."); self.tree_historial.column("cant", width=50, anchor="e")
        self.tree_historial.heading("p_unit", text="P. Unit."); self.tree_historial.column("p_unit", width=80, anchor="e")
        self.tree_historial.heading("p_efec", text="Efectivo"); self.tree_historial.column("p_efec", width=80, anchor="e")
        self.tree_historial.heading("p_trans", text="Transf."); self.tree_historial.column("p_trans", width=80, anchor="e")
        self.tree_historial.heading("total", text="Total"); self.tree_historial.column("total", width=80, anchor="e")


    def _crear_panel_acciones(self):
        """Crea los botones de acción en la parte inferior."""
        frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        frame_acciones.pack(fill="x", side="bottom", pady=10, padx=10)
        
        self.btn_generar_pdf = ctk.CTkButton(
            frame_acciones, text="Descargar PDF", image=self.icono_descargar,
            command=self.controller.descargar_reporte_historial,
            fg_color="#28a745", hover_color="#218838" # Color "success"
        )
        self.btn_generar_pdf.pack(side="left", padx=5)

        self.btn_anular_venta = ctk.CTkButton(
            frame_acciones, text="Anular Venta Seleccionada",
            state="disabled",
            command=self.controller.anular_venta_seleccionada,
            fg_color="#D32F2F", hover_color="#B71C1C" # Color "danger"
        )
        self.btn_anular_venta.pack(side="left", padx=5)

    def _configurar_bindings_globales(self):
        """Configura eventos que necesitan interactuar con otros widgets."""
        self.tree_historial.bind("<<TreeviewSelect>>", self.controller.actualizar_estado_boton_anular)
        self.tree_historial.bind("<Button-1>", self.controller.deseleccionar_si_clic_vacio, add='+')