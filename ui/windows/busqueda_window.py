import customtkinter as ctk
from tkinter import ttk
from utilities import helpers
#from utilities.themes import configure_treeview_colors

class BusquedaWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, modo_venta_activo):
        super().__init__(parent)
        self.controller = controller
        self.modo_venta_activo = modo_venta_activo

        self.title("Buscar Productos")
        self.attributes('-topmost', True)
        self._crear_widgets()
        self._configurar_bindings()
        
        helpers.configurar_dialogo(self, parent, self.entry_busqueda)

    def _crear_widgets(self):
        frame_busqueda = ctk.CTkFrame(self)
        frame_busqueda.pack(fill="both", expand=True, padx=10, pady=10)

        frame_control = ctk.CTkFrame(frame_busqueda, fg_color="transparent")
        frame_control.pack(pady=10, fill="x")

        ctk.CTkLabel(frame_control, text="Nombre del Producto:", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.entry_busqueda = ctk.CTkEntry(frame_control, font=("Segoe UI", 12))
        self.entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)
        
        tree_container = ctk.CTkFrame(frame_busqueda)
        tree_container.pack(fill="both", expand=True)
        
        self.tree_busqueda = ttk.Treeview(tree_container, columns=("nombre", "precio", "stock"), show="headings")
        self.tree_busqueda.pack(side="left", fill="both", expand=True)
        #configure_treeview_colors(self.tree_busqueda)
        scrollbar = ctk.CTkScrollbar(tree_container, command=self.tree_busqueda.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_busqueda.configure(yscrollcommand=scrollbar.set)
        
        self.tree_busqueda.heading("nombre", text="Nombre")
        self.tree_busqueda.heading("precio", text="Precio")
        self.tree_busqueda.heading("stock", text="Stock")
        self.tree_busqueda.column("nombre", width=400, anchor="w")
        self.tree_busqueda.column("precio", width=100, anchor="e")
        self.tree_busqueda.column("stock", width=100, anchor="e")

        frame_botones = ctk.CTkFrame(frame_busqueda, fg_color="transparent")
        frame_botones.pack(pady=10)
        
        estado_boton_agregar = "normal" if self.modo_venta_activo else "disabled"
        self.btn_agregar = ctk.CTkButton(frame_botones, text="Agregar a Carrito", fg_color="#28a745", hover_color="#218838", state=estado_boton_agregar)
        self.btn_agregar.pack(side="left", padx=5)
        
        self.btn_detalles = ctk.CTkButton(frame_botones, text="Ver Detalles", command=self._on_ver_detalles)
        self.btn_detalles.pack(side="left", padx=5)


    def _configurar_bindings(self):
        self.entry_busqueda.bind("<KeyRelease>", self._on_realizar_busqueda)
        self.btn_agregar.configure(command=self._on_agregar_seleccion)
        self.tree_busqueda.bind("<Double-1>", self._on_double_click)
        self.bind("<Escape>", lambda e: self.destroy())
    
    def _on_realizar_busqueda(self, event=None):
        termino = self.entry_busqueda.get()
        self.controller.realizar_busqueda_productos(termino, self.tree_busqueda)

    def _on_double_click(self, event=None):
        if self.modo_venta_activo:
            self._on_agregar_seleccion()
        else:
            self._on_ver_detalles()

    def _on_ver_detalles(self):
        item_seleccionado = self.tree_busqueda.focus()
        if not item_seleccionado:
            return
        
        codigo_barras = self.tree_busqueda.item(item_seleccionado, "tags")[0]
        self.controller.mostrar_detalles_producto(codigo_barras)
        self.destroy()

    def _on_agregar_seleccion(self):
        if not self.modo_venta_activo:
            return

        item_seleccionado = self.tree_busqueda.focus()
        if not item_seleccionado:
            return
        
        codigo_barras = self.tree_busqueda.item(item_seleccionado, "tags")[0]
        self.controller.agregar_producto_desde_busqueda(codigo_barras)
        self.destroy()