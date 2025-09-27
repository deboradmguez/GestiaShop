import customtkinter as ctk
from tkinter import ttk

# Esta constante ya no es tan necesaria, pero podemos mantenerla
FUENTE_GENERAL = ("Segoe UI", 16)

class VentasTab(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self._crear_controles_superiores()
        self._crear_vista_carrito()
        self._crear_pie_de_pestana()

    def _crear_controles_superiores(self):
        frame_control_venta = ctk.CTkFrame(self, fg_color="transparent")
        frame_control_venta.pack(fill="x", side="top", padx=10, pady=10)

        frame_codigo = ctk.CTkFrame(frame_control_venta, fg_color="transparent")
        frame_codigo.pack(fill="x", pady=3)

        ctk.CTkLabel(frame_codigo, text="Código de Barras:", font=FUENTE_GENERAL).pack(side="left", padx=5)
        self.entry_codigo = ctk.CTkEntry(frame_codigo, font=("Segoe UI", 16))
        self.entry_codigo.pack(side="left", expand=True, fill="x", padx=5)
        self.entry_codigo.focus()
        self.entry_codigo.bind("<Return>", lambda event: self.controller.buscar_y_agregar_a_carrito())

        frame_botones_venta = ctk.CTkFrame(frame_control_venta, fg_color="transparent")
        frame_botones_venta.pack(fill="x", pady=(10, 0))

        self.btn_buscar_nombre = ctk.CTkButton(
            frame_botones_venta,
            text="🔎 Buscar por Nombre (Ctrl + B)",
            command=self.controller.mostrar_ventana_busqueda
        )
        self.btn_buscar_nombre.pack(side="left", padx=5)

        self.btn_prod_comun = ctk.CTkButton(
            frame_botones_venta,
            text="➕ Prod. Común (Ctrl + A)",
            command=self.controller.agregar_producto_comun,
            fg_color="#ffc107", hover_color="#e0a800" # Color "warning"
        )
        self.btn_prod_comun.pack(side="left", padx=5)

    def _crear_vista_carrito(self):
        """Crea la tabla (Treeview) para mostrar los productos del carrito."""
        tree_container = ctk.CTkFrame(self)
        tree_container.pack(fill="both", expand=True, pady=10, padx=10)
        
        # --- Estilo para el Treeview ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, rowheight=30)
        style.map("Treeview", background=[('selected', '#3470b8')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", font=("Segoe UI", 10, "bold"))
        
        self.tree_carrito = ttk.Treeview(
            tree_container,
            columns=("producto", "cantidad", "precio", "stock", "total"),
            show="headings",
            height=10
        )
        self.tree_carrito.pack(side="left", fill="both", expand=True)

        # --- Scrollbar de CustomTkinter ---
        scrollbar = ctk.CTkScrollbar(tree_container, command=self.tree_carrito.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_carrito.configure(yscrollcommand=scrollbar.set)

        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cantidad")
        self.tree_carrito.heading("precio", text="Precio")
        self.tree_carrito.heading("stock", text="Stock")
        self.tree_carrito.heading("total", text="Total")
        self.tree_carrito.column("producto", width=350, anchor="w")
        self.tree_carrito.column("cantidad", width=80, anchor="e")
        self.tree_carrito.column("precio", width=80, anchor="e")
        self.tree_carrito.column("stock", width=80, anchor="e")
        self.tree_carrito.column("total", width=80, anchor="e")
        
        self.tree_carrito.bind("<Double-1>", self.controller.modificar_cantidad_carrito)
        self.tree_carrito.bind("<Return>", self.controller.modificar_cantidad_carrito)
        self.tree_carrito.bind("<BackSpace>", lambda e: self.controller.quitar_producto_del_carrito())

    def _crear_pie_de_pestana(self):
        """Crea el área inferior con el total y los botones de finalizar venta."""
        frame_pie_ventas = ctk.CTkFrame(self)
        frame_pie_ventas.pack(fill="x", side="bottom", pady=10, padx=10)

        self.lbl_total = ctk.CTkLabel(
            frame_pie_ventas,
            text="Total: $0.00",
            font=("Arial Black", 28),
            fg_color="#1E8E3E",  # Un verde bonito
            text_color="white",
            corner_radius=8
        )
        self.lbl_total.pack(side="right", padx=(20, 10), ipady=5)

        self.btn_quitar = ctk.CTkButton(
            frame_pie_ventas, text="Quitar",
            command=self.controller.quitar_producto_del_carrito,
            state="disabled",
            fg_color="#D32F2F", hover_color="#B71C1C"
        )
        self.btn_quitar.pack(side="left", padx=(10, 5))

        self.btn_vaciar = ctk.CTkButton(
            frame_pie_ventas, text="Vaciar (Ctrl + D)",
            command=self.controller.vaciar_carrito,
            state="disabled"
        )
        self.btn_vaciar.pack(side="left", padx=5)

        self.btn_finalizar = ctk.CTkButton(
            frame_pie_ventas, text="Finalizar (Ctrl + F)",
            command=self.controller.mostrar_ventana_cobrar,
            state="disabled",
            fg_color="#28a745", hover_color="#218838"
        )
        self.btn_finalizar.pack(side="left", padx=5)

    def actualizar_vista(self, carrito_actualizado, total_actualizado):
        # Limpiamos la vista actual
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        # Llenamos con los nuevos datos
        for codigo, datos in carrito_actualizado.items():
            nombre = datos["nombre"]
            cantidad = datos["cantidad"]
            precio_unitario = datos["precio"]
            total_item = precio_unitario * cantidad
            stock_info = datos.get("stock", "N/A")
            
            stock_display = "-" if codigo.startswith("PROD_COMUN-") else str(stock_info)

            self.tree_carrito.insert(
                "", "end",
                values=(nombre, cantidad, f"${precio_unitario:,.2f}", stock_display, f"${total_item:,.2f}"),
            )

        # Actualizamos el label del total
        self.lbl_total.configure(text=f"Total: ${total_actualizado:,.2f}")
        self._actualizar_estado_botones(carrito_actualizado)
        
    def _actualizar_estado_botones(self, carrito):
        estado = "normal" if carrito else "disabled"
        
        # Usamos .configure() para cambiar el estado de los widgets ya creados
        self.btn_quitar.configure(state=estado)
        self.btn_vaciar.configure(state=estado)
        self.btn_finalizar.configure(state=estado)