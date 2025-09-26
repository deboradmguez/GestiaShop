import tkinter as tk
from tkinter import ttk

# Es buena práctica definir constantes si se usan en varios lugares.
FUENTE_GENERAL = ("Segoe UI", 16)

class ProductosTab(ttk.Frame):
    """
    Clase que representa la pestaña de 'Productos' (gestión de inventario).
    """
    def __init__(self, parent, controller):
        """
        Constructor de la pestaña.
        - 'parent': El widget Notebook.
        - 'controller': La clase principal de la aplicación (App).
        """
        super().__init__(parent)
        self.controller = controller

        # Para que las imágenes no desaparezcan, las guardamos como atributos de la clase.
        # Asumimos que la función 'ruta_recurso' ahora es un método del controller.
        self.icono_agregar = tk.PhotoImage(file=self.controller.ruta_recurso("icons/agregar.png"))
        self.icono_modificar = tk.PhotoImage(file=self.controller.ruta_recurso("icons/lapiz.png"))
        self.icono_eliminar = tk.PhotoImage(file=self.controller.ruta_recurso("icons/borrar.png"))

        # Organizamos la creación de widgets en métodos para mayor claridad.
        self._crear_panel_de_controles()
        self._crear_tabla_de_inventario()

    def _crear_panel_de_controles(self):
        """Crea el panel superior con filtros, búsqueda y botones de acción."""
        frame_controles = ttk.Frame(self)
        frame_controles.pack(pady=5, fill="x")

        ttk.Label(frame_controles, text="Filtrar por:", font=("Segoe UI", 11)).pack(
            side="left", padx=(10, 5)
        )
        opciones_filtro = ["Todos los productos", "Productos con stock bajo"]
        self.combo_filtro_productos = ttk.Combobox(
            frame_controles, values=opciones_filtro, state="readonly", 
            font=("Segoe UI", 12), width=22
        )
        self.combo_filtro_productos.set(opciones_filtro[0])
        self.combo_filtro_productos.pack(side="left", padx=5)
        # Los 'binds' ahora llaman a métodos del controller.
        self.combo_filtro_productos.bind("<<ComboboxSelected>>", self.controller.filtrar_productos_y_recargar)

        ttk.Label(frame_controles, text="Buscar:", font=FUENTE_GENERAL).pack(
            side="left", padx=5
        )
        self.entry_buscar_producto = ttk.Entry(frame_controles, font=FUENTE_GENERAL)
        self.entry_buscar_producto.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_buscar_producto.bind("<KeyRelease>", self.controller.filtrar_productos_y_recargar)
        self.entry_buscar_producto.bind("<Return>", self.controller.filtrar_productos_y_recargar)

        # Botones de acción
        self.btn_agregar_prod = ttk.Button(
            frame_controles, image=self.icono_agregar,
            command=self.controller.mostrar_ventana_agregar_producto,
            style="success.TButton"
        )
        self.btn_agregar_prod.pack(side="left", padx=5)

        self.btn_modificar_prod = ttk.Button(
            frame_controles, image=self.icono_modificar,
            command=self.controller.modificar_producto,
            style="warning.TButton"
        )
        self.btn_modificar_prod.pack(side="left", padx=5)

        self.btn_eliminar_prod = ttk.Button(
            frame_controles, image=self.icono_eliminar,
            command=self.controller.eliminar_producto,
            style="danger.TButton"
        )
        self.btn_eliminar_prod.pack(side="left", padx=5)

        self.btn_carga_rapida = ttk.Button(
            frame_controles, text="Carga Rápida",
            command=self.controller.abrir_ventana_carga_rapida,
            style="primary.TButton"
        )
        self.btn_carga_rapida.pack(side="left", padx=5)

    def _crear_tabla_de_inventario(self):
        """Crea la tabla (Treeview) para mostrar el listado de productos."""
        self.tree_inventario = ttk.Treeview(
            self, columns=("codigo", "nombre", "precio", "stock"), show="headings", style="Custom.Treeview"
        )
        self.tree_inventario.heading("codigo", text="Código")
        self.tree_inventario.heading("nombre", text="Nombre")
        self.tree_inventario.heading("precio", text="Precio")
        self.tree_inventario.heading("stock", text="Stock")
        self.tree_inventario.column("codigo", width=150, anchor="w")
        self.tree_inventario.column("nombre", width=300, anchor="w")
        self.tree_inventario.column("precio", width=100, anchor="e")
        self.tree_inventario.column("stock", width=100, anchor="e")
        self.tree_inventario.pack(fill="both", expand=True)
        
        # Las configuraciones de estilo y tags se mantienen igual
        self.tree_inventario.tag_configure("alerta_stock", background="#FFAA99", foreground="black")
        self.tree_inventario.tag_configure("mensaje_vacio", font=("Segoe UI", 11, "italic"), foreground="grey")

        self.tree_inventario.bind("<Double-1>", self.controller.editar_con_doble_click)
    