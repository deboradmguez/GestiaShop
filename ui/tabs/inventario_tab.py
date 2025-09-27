import customtkinter as ctk

class InventarioTab(ctk.CTkFrame):
    """
    Clase que representa la interfaz de la pestaña 'Inventario'.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Creamos la interfaz
        self._crear_widgets()
        self._configurar_bindings()

    def _crear_widgets(self):
        """Crea y posiciona todos los widgets de esta pestaña."""
        ctk.CTkLabel(self, text="Escanear Código de Barras", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20)

        self.entry_codigo_inv = ctk.CTkEntry(self, font=("Segoe UI", 16))
        self.entry_codigo_inv.pack(padx=20, pady=5, fill="x")
        self.entry_codigo_inv.focus()

        # Frame para los datos del producto
        frame_datos = ctk.CTkFrame(self) 
        frame_datos.pack(fill="x", pady=10, padx=20)
        frame_datos.columnconfigure(1, weight=1)

        self.entries = {}
        campos = {
            "Nombre del Producto:": "nombre_edit",
            "Precio:": "precio_edit",
            "Stock Actual:": "lbl_stock_actual",
            "Agregar Stock:": "stock_agregar"
        }

        for i, (texto, clave) in enumerate(campos.items()):
            ctk.CTkLabel(frame_datos, text=texto).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if clave == "lbl_stock_actual":
                widget = ctk.CTkLabel(frame_datos, text="0", font=ctk.CTkFont(size=11, weight="bold"))
            else:
                # El width en CTkEntry es en píxeles, 40 era muy pequeño
                widget = ctk.CTkEntry(frame_datos)
            
            widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[clave] = widget
        
        # Botón de confirmación (corregido)
        self.btn_confirmar_cambios = ctk.CTkButton(
            self, text="✅ Guardar Cambios", state="disabled",
            fg_color="#28a745", hover_color="#218838" # Color "success"
        )
        self.btn_confirmar_cambios.pack(pady=10)

    def _configurar_bindings(self):
        """Configura todos los atajos de teclado y comandos."""
        self.entry_codigo_inv.bind("<Return>", self.controller.buscar_producto_para_inventario)
        # Usamos .configure() que es el método estándar en CustomTkinter
        self.btn_confirmar_cambios.configure(command=self.controller.guardar_cambios_inventario)

        # Navegación entre campos con Enter
        self.entries["nombre_edit"].bind("<Return>", lambda e: self.entries["precio_edit"].focus_set())
        self.entries["precio_edit"].bind("<Return>", lambda e: self.entries["stock_agregar"].focus_set())
        self.entries["stock_agregar"].bind("<Return>", self.controller.guardar_cambios_inventario)