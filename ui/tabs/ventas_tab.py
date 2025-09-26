import tkinter as tk
from tkinter import ttk

# Definimos una constante para la fuente, para no repetirla.
FUENTE_GENERAL = ("Segoe UI", 16)

class VentasTab(ttk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        # Llamamos a métodos privados para organizar la creación de la interfaz.
        self._crear_controles_superiores()
        self._crear_vista_carrito()
        self._crear_pie_de_pestana()

    def _crear_controles_superiores(self):
        """Crea el área de ingreso de código y los botones de acción."""
        frame_control_venta = ttk.Frame(self, padding=10)
        frame_control_venta.pack(fill="x", side="top")

        # Campo para escanear el código
        frame_codigo = ttk.Frame(frame_control_venta)
        frame_codigo.pack(fill="x", pady=3)

        ttk.Label(frame_codigo, text="Código de Barras:", font=FUENTE_GENERAL).pack(
            side="left", padx=5
        )
        # Los widgets ahora son atributos de la clase (self.entry_codigo)
        self.entry_codigo = ttk.Entry(frame_codigo, font=("Segoe UI", 12), width=25)
        self.entry_codigo.pack(side="left", expand=True, fill="x", padx=5)
        self.entry_codigo.focus()
        # Los comandos ahora llaman a métodos del 'controller'
        self.entry_codigo.bind("<Return>", lambda event: self.controller.buscar_y_agregar_a_carrito())

        # Botones de acceso rápido
        frame_botones_venta = ttk.Frame(frame_control_venta)
        frame_botones_venta.pack(fill="x", pady=(10, 0))

        self.btn_buscar_nombre = ttk.Button(
            frame_botones_venta,
            text="🔎 Buscar por Nombre (Ctrl + B)",
            command=self.controller.mostrar_ventana_busqueda, # Llama al método en el controller
            style="secondary.TButton",
        )
        self.btn_buscar_nombre.pack(side="left", padx=5, ipadx=5)

        self.btn_prod_comun = ttk.Button(
            frame_botones_venta,
            text="➕ Prod. Común (Ctrl + A)",
            command=self.controller.agregar_producto_comun, # Llama al método en el controller
            style="warning.TButton",
        )
        self.btn_prod_comun.pack(side="left", padx=5, ipadx=5)

    def _crear_vista_carrito(self):
        """Crea la tabla (Treeview) para mostrar los productos del carrito."""
        frame_carrito = ttk.Frame(self)
        frame_carrito.pack(fill="both", expand=True, pady=10)
        
        tree_frame = ttk.Frame(frame_carrito)
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree_carrito = ttk.Treeview(
            tree_frame,
            columns=("producto", "cantidad", "precio", "stock", "total"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=10
        )
        scrollbar.config(command=self.tree_carrito.yview)

        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cantidad")
        self.tree_carrito.column("producto", width=350, anchor="w")
        self.tree_carrito.column("cantidad", width=80, anchor="e")
        self.tree_carrito.column("precio", width=80, anchor="e")
        self.tree_carrito.column("stock", width=80, anchor="e")
        self.tree_carrito.column("total", width=80, anchor="e")
        self.tree_carrito.pack(fill="both", expand=True)
        
        self.tree_carrito.bind("<Double-1>", self.controller.modificar_cantidad_carrito)
        self.tree_carrito.bind("<Return>", self.controller.modificar_cantidad_carrito)
        self.tree_carrito.bind("<BackSpace>", lambda e: self.controller.quitar_producto_del_carrito())

    def _crear_pie_de_pestana(self):
        """Crea el área inferior con el total y los botones de finalizar venta."""
        frame_pie_ventas = ttk.Frame(self)
        frame_pie_ventas.pack(fill="x", side="bottom", pady=(10, 0))

        self.lbl_total = ttk.Label(
            frame_pie_ventas,
            text="Total: $0.00",
            font=("Arial Black", 28),
            bootstyle="inverse-success",
            padding=10,
        )
        self.lbl_total.pack(side="right", padx=(20, 10))

        self.btn_quitar = ttk.Button(
            frame_pie_ventas, text="Quitar",
            command=self.controller.quitar_producto_del_carrito,
            style="danger.TButton", state="disabled",
        )
        self.btn_quitar.pack(side="left", padx=(10, 5))

        self.btn_vaciar = ttk.Button(
            frame_pie_ventas, text="Vaciar (Ctrl + D)",
            command=self.controller.vaciar_carrito,
            style="secondary.TButton", state="disabled",
        )
        self.btn_vaciar.pack(side="left", padx=5)

        self.btn_finalizar = ttk.Button(
            frame_pie_ventas, text="Finalizar (Ctrl + F)",
            command=self.controller.mostrar_ventana_cobrar,
            style="success.TButton", state="disabled",
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
        self.lbl_total.config(text=f"Total: ${total_actualizado:,.2f}")
        self._actualizar_estado_botones(carrito_actualizado)
        
    def _actualizar_estado_botones(self, carrito):
        """Habilita o deshabilita los botones según si el carrito tiene items."""
        estado = "normal" if carrito else "disabled"
        
        self.btn_quitar.config(state=estado)
        self.btn_vaciar.config(state=estado)
        self.btn_finalizar.config(state=estado)
        
    