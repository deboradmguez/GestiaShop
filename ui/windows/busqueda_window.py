import customtkinter as ctk
from tkinter import ttk
from utilities import helpers
from utilities.themes import configure_treeview_colors

class BusquedaWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("Buscar Productos")
        self.transient(parent)
        self.attributes('-topmost', True)
        self.grab_set()

        self._crear_widgets()
        self._configurar_bindings()
        
        helpers.centrar_ventana(self, parent)

    def _crear_widgets(self):
        frame_busqueda = ctk.CTkFrame(self)
        frame_busqueda.pack(fill="both", expand=True, padx=10, pady=10)

        frame_control = ctk.CTkFrame(frame_busqueda, fg_color="transparent")
        frame_control.pack(pady=10, fill="x")

        ctk.CTkLabel(frame_control, text="Nombre del Producto:", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.entry_busqueda = ctk.CTkEntry(frame_control, font=("Segoe UI", 12))
        self.entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_busqueda.focus_set()

        # --- Treeview y Scrollbar ---
        tree_container = ctk.CTkFrame(frame_busqueda)
        tree_container.pack(fill="both", expand=True)
        
        self.tree_busqueda = ttk.Treeview(tree_container, columns=("nombre", "precio", "stock"), show="headings")
        self.tree_busqueda.pack(side="left", fill="both", expand=True)
        configure_treeview_colors(self.tree_busqueda)
        scrollbar = ctk.CTkScrollbar(tree_container, command=self.tree_busqueda.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_busqueda.configure(yscrollcommand=scrollbar.set)
        
        self.tree_busqueda.heading("nombre", text="Nombre")
        self.tree_busqueda.heading("precio", text="Precio")
        self.tree_busqueda.heading("stock", text="Stock")
        self.tree_busqueda.column("nombre", width=400, anchor="w")
        self.tree_busqueda.column("precio", width=100, anchor="e")
        self.tree_busqueda.column("stock", width=100, anchor="e")

        self.btn_agregar = ctk.CTkButton(frame_busqueda, text="Agregar a Carrito", fg_color="#28a745", hover_color="#218838")
        self.btn_agregar.pack(pady=10)

    def _configurar_bindings(self):
        self.entry_busqueda.bind("<KeyRelease>", self._on_realizar_busqueda)
        self.btn_agregar.configure(command=self._on_agregar_seleccion)
        self.tree_busqueda.bind("<Double-1>", lambda e: self._on_agregar_seleccion())
        self.bind("<Escape>", lambda e: self.destroy())
    
    # --- Métodos que comunican con el controlador ---

    def _on_realizar_busqueda(self, event=None):
        termino = self.entry_busqueda.get()
        # Le pasa el término y el widget que debe actualizar
        self.controller.realizar_busqueda_productos(termino, self.tree_busqueda)

    def _on_agregar_seleccion(self):
        item_seleccionado = self.tree_busqueda.focus()
        if not item_seleccionado:
            return
        
        codigo_barras = self.tree_busqueda.item(item_seleccionado, "tags")[0]
        # Le pasa el código y se autodestruye
        self.controller.agregar_producto_desde_busqueda(codigo_barras)
        self.destroy()