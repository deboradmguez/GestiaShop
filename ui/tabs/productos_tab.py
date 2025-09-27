import customtkinter as ctk
from tkinter import ttk
from PIL import Image

# Esta constante ya no es tan necesaria, pero la podemos mantener si quieres
FUENTE_GENERAL = ("Segoe UI", 16)

class ProductosTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- MANEJO DE IMÁGENES CORREGIDO ---
        try:
            self.icono_agregar = ctk.CTkImage(Image.open(self.controller.ruta_recurso("icons/agregar.png")))
            self.icono_modificar = ctk.CTkImage(Image.open(self.controller.ruta_recurso("icons/lapiz.png")))
            self.icono_eliminar = ctk.CTkImage(Image.open(self.controller.ruta_recurso("icons/borrar.png")))
        except Exception as e:
            print(f"Error al cargar los iconos de productos: {e}")
            self.icono_agregar = self.icono_modificar = self.icono_eliminar = None

        self._crear_panel_de_controles()
        self._crear_tabla_de_inventario()

    def _crear_panel_de_controles(self):
        """Crea el panel superior con filtros, búsqueda y botones de acción."""
        frame_controles = ctk.CTkFrame(self)
        frame_controles.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_controles, text="Filtrar por:", font=("Segoe UI", 12)).pack(
            side="left", padx=(10, 5)
        )
        opciones_filtro = ["Todos los productos", "Productos con stock bajo"]
        self.combo_filtro_productos = ctk.CTkComboBox(
            frame_controles,
            values=opciones_filtro,
            command=self.controller.filtrar_productos_y_recargar
        )
        self.combo_filtro_productos.set(opciones_filtro[0])
        self.combo_filtro_productos.pack(side="left", padx=5)

        ctk.CTkLabel(frame_controles, text="Buscar:", font=FUENTE_GENERAL).pack(
            side="left", padx=(10, 5)
        )
        self.entry_buscar_producto = ctk.CTkEntry(frame_controles, font=FUENTE_GENERAL)
        self.entry_buscar_producto.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_buscar_producto.bind("<KeyRelease>", self.controller.filtrar_productos_y_recargar)
        self.entry_buscar_producto.bind("<Return>", self.controller.filtrar_productos_y_recargar)

        # --- Botones de acción CORREGIDOS ---
        self.btn_agregar_prod = ctk.CTkButton(
            frame_controles, image=self.icono_agregar, text="", width=32,
            command=self.controller.mostrar_ventana_agregar_producto,
            fg_color="#28a745", hover_color="#218838"  # Color "success"
        )
        self.btn_agregar_prod.pack(side="left", padx=5)

        self.btn_modificar_prod = ctk.CTkButton(
            frame_controles, image=self.icono_modificar, text="", width=32,
            command=self.controller.modificar_producto,
            fg_color="#ffc107", hover_color="#e0a800" # Color "warning"
        )
        self.btn_modificar_prod.pack(side="left", padx=5)

        self.btn_eliminar_prod = ctk.CTkButton(
            frame_controles, image=self.icono_eliminar, text="", width=32,
            command=self.controller.eliminar_producto,
            fg_color="#D32F2F", hover_color="#B71C1C" # Color "danger"
        )
        self.btn_eliminar_prod.pack(side="left", padx=5)

        self.btn_carga_rapida = ctk.CTkButton(
            frame_controles, text="Carga Rápida",
            command=self.controller.abrir_ventana_carga_rapida
        )
        self.btn_carga_rapida.pack(side="left", padx=10)

    def _crear_tabla_de_inventario(self):
        """Crea la tabla (Treeview) para mostrar el listado de productos."""
        tree_container = ctk.CTkFrame(self)
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0,10))
  
        self.tree_inventario = ttk.Treeview(
            tree_container, columns=("codigo", "nombre", "precio", "stock"), show="headings"
        )
        self.tree_inventario.pack(side="left", fill="both", expand=True)

        # Scrollbar de CustomTkinter
        scrollbar = ctk.CTkScrollbar(tree_container, command=self.tree_inventario.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_inventario.configure(yscrollcommand=scrollbar.set)
        
        self.tree_inventario.heading("codigo", text="Código")
        self.tree_inventario.heading("nombre", text="Nombre")
        self.tree_inventario.heading("precio", text="Precio")
        self.tree_inventario.heading("stock", text="Stock")
        self.tree_inventario.column("codigo", width=150, anchor="w")
        self.tree_inventario.column("nombre", width=400, anchor="w")
        self.tree_inventario.column("precio", width=100, anchor="e")
        self.tree_inventario.column("stock", width=100, anchor="e")
        
        self.tree_inventario.tag_configure("alerta_stock", background="#FFAA99", foreground="black")
        self.tree_inventario.tag_configure("mensaje_vacio", font=("Segoe UI", 11, "italic"), foreground="grey")

        self.tree_inventario.bind("<Double-1>", self.controller.editar_con_doble_click)