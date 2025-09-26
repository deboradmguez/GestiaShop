import customtkinter as ctk


class InventarioTab(ctk.CTkFrame):
    """
    Clase que representa la interfaz de la pestaña 'Inventario'.
    No contiene lógica de negocio, solo la definición de los widgets.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller

        # Creamos la interfaz
        self._crear_widgets()
        self._configurar_bindings()

    def _crear_widgets(self):
        """Crea y posiciona todos los widgets de esta pestaña."""
        ctk.CTkLabel(self, text="Escanear Código de Barras", font=("Segoe UI", 16)).pack(pady=(10, 5))

        self.entry_codigo_inv = ctk.CTkEntry(self, font=("Segoe UI", 16))
        self.entry_codigo_inv.pack(padx=20, pady=5, fill="x")
        self.entry_codigo_inv.focus()

        # Frame para los datos del producto
        frame_datos = ctk.CTkFrame(self, padding=10)
        frame_datos.pack(fill="x", pady=10)
        frame_datos.columnconfigure(1, weight=1) # Permite que los Entry se expandan

        # Guardamos los widgets en un diccionario para fácil acceso desde el controlador
        self.entries = {}
        campos = {
            "Nombre del Producto:": "nombre_edit",
            "Precio:": "precio_edit",
            "Stock Actual:": "lbl_stock_actual", # Este es un Label
            "Agregar Stock:": "stock_agregar"
        }

        for i, (texto, clave) in enumerate(campos.items()):
            ctk.CTkLabel(frame_datos, text=texto).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if clave == "lbl_stock_actual":
                widget = ctk.CTkLabel(frame_datos, text="0", font=("Segoe UI", 11, "bold"))
            else:
                widget = ctk.CTkEntry(frame_datos, width=40)
            
            widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[clave] = widget
        
        # Botón de confirmación
        self.btn_confirmar_cambios = ctk.CTkButton(
            self, text="✅ Guardar Cambios", style="success.TButton", state="disabled"
        )
        self.btn_confirmar_cambios.pack(pady=10)

    def _configurar_bindings(self):
        """Configura todos los atajos de teclado y comandos."""
        # Los eventos ahora llaman a los métodos delegados del controlador
        self.entry_codigo_inv.bind("<Return>", self.controller.buscar_producto_para_inventario)
        self.btn_confirmar_cambios.config(command=self.controller.guardar_cambios_inventario)

        # Navegación entre campos con Enter
        self.entries["nombre_edit"].bind("<Return>", lambda e: self.entries["precio_edit"].focus_set())
        self.entries["precio_edit"].bind("<Return>", lambda e: self.entries["stock_agregar"].focus_set())
        self.entries["stock_agregar"].bind("<Return>", self.controller.guardar_cambios_inventario)