# ui/windows/busqueda_window.py

import tkinter as tk
from tkinter import ttk
from utilities import helpers
class BusquedaWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        """
        Constructor de la ventana de búsqueda.
        - 'parent' es la ventana principal de la app.
        - 'controller' es la instancia de la clase App, nuestro cerebro.
        """
        super().__init__(parent)
        self.controller = controller

        self.title("Buscar Productos")
        self.transient(parent)
        self.attributes('-topmost', True)
        self.grab_set()

        # Llamamos a un método para crear los widgets internos
        self._crear_widgets()
        self._configurar_bindings()
        
        helpers.centrar_ventana(self, parent)

    def _crear_widgets(self):
        """Crea y posiciona todos los widgets de esta ventana."""
        frame_busqueda = ttk.Frame(self, padding=10)
        frame_busqueda.pack(fill="both", expand=True)

        frame_control = ttk.Frame(frame_busqueda)
        frame_control.pack(pady=10)

        ttk.Label(frame_control, text="Nombre del Producto:", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.entry_busqueda = ttk.Entry(frame_control, width=40, font=("Segoe UI", 12))
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.focus_set()

        self.tree_busqueda = ttk.Treeview(
            frame_busqueda, columns=("nombre", "precio", "stock"), show="headings"
        )
        # ... (configuración de headings y columns sin cambios) ...
        self.tree_busqueda.heading("nombre", text="Nombre")
        self.tree_busqueda.heading("precio", text="Precio")
        self.tree_busqueda.heading("stock", text="Stock")
        self.tree_busqueda.column("nombre", width=300, anchor="w")
        self.tree_busqueda.column("precio", width=100, anchor="e")
        self.tree_busqueda.column("stock", width=100, anchor="e")
        self.tree_busqueda.pack(fill="both", expand=True)

        self.btn_agregar = ttk.Button(
            frame_busqueda, text="Agregar a Carrito", style="success.TButton"
        )
        self.btn_agregar.pack(pady=10)

    def _configurar_bindings(self):
        """Configura todos los eventos de los widgets."""
        # Al escribir, la ventana le pide al controlador que realice la búsqueda
        self.entry_busqueda.bind("<KeyRelease>", self._on_realizar_busqueda)

        self.btn_agregar.config(command=self._on_agregar_seleccion)
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