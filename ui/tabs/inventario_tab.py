import customtkinter as ctk

class InventarioTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self._crear_widgets()
        self._configurar_bindings()
        self.after(300, lambda: self.entry_codigo_inv.focus_set())
        
    def _crear_widgets(self):

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 
        self.grid_columnconfigure(2, weight=1) 

        frame_principal = ctk.CTkFrame(self)
        frame_principal.grid(row=0, column=1, pady=20, padx=20, sticky="n")

        
        ctk.CTkLabel(frame_principal, text="Escanear Código de Barras", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20)

        self.entry_codigo_inv = ctk.CTkEntry(frame_principal, font=("Segoe UI", 16), width=350)
        self.entry_codigo_inv.pack(padx=20, pady=5)

        
        frame_datos = ctk.CTkFrame(frame_principal) 
        frame_datos.pack(pady=10, padx=20)
       

        self.entries = {}
        campos = {
            "Nombre del Producto:": "nombre_edit",
            "Precio:": "precio_edit",
            "Stock Actual:": "lbl_stock_actual",
            "Agregar Stock:": "stock_agregar"
        }

        for i, (texto, clave) in enumerate(campos.items()):
            ctk.CTkLabel(frame_datos, text=texto).grid(row=i, column=0, sticky="w", padx=10, pady=8)
            if clave == "lbl_stock_actual":
                widget = ctk.CTkLabel(frame_datos, text="0", font=ctk.CTkFont(size=11, weight="bold"))
            else:
                widget = ctk.CTkEntry(frame_datos, width=250)
            
            widget.grid(row=i, column=1, padx=10, pady=8) # Sin sticky
            self.entries[clave] = widget
        
        self.btn_confirmar_cambios = ctk.CTkButton(
            frame_principal, text="✅ Guardar Cambios", state="disabled",
            fg_color="#28a745", hover_color="#218838"
        )
        self.btn_confirmar_cambios.pack(pady=20)


    def _configurar_bindings(self):
        """Configura todos los atajos de teclado y comandos."""
        self.entry_codigo_inv.bind("<Return>", self.controller.buscar_producto_para_inventario)
        self.btn_confirmar_cambios.configure(command=self.controller.guardar_cambios_inventario)
        self.entries["nombre_edit"].bind("<Return>", lambda e: self.entries["precio_edit"].focus_set())
        self.entries["precio_edit"].bind("<Return>", lambda e: self.entries["stock_agregar"].focus_set())
        self.entries["stock_agregar"].bind("<Return>", self.controller.guardar_cambios_inventario)