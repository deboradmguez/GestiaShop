import tkinter as tk
from tkinter import Toplevel, ttk, messagebox

# from ..database import database_manager as db

class ProductosLogic:
    """
    Controlador especializado para toda la lógica de la pestaña de Productos.
    """
    def __init__(self, app_controller):
        self.app = app_controller # Referencia a la App principal para acceder a las vistas y al estado

    # --- LÓGICA DE VISUALIZACIÓN Y FILTROS ---

    def filtrar_productos_y_recargar(self, event=None):
        """
        Obtiene los filtros de la UI, busca en la DB y actualiza la tabla de productos.
        """
        filtro_seleccionado = self.app.productos_tab.combo_filtro_productos.get()
        texto_busqueda = self.app.productos_tab.entry_buscar_producto.get().strip()
        tipo_filtro_db = 'bajo' if filtro_seleccionado == "Productos con stock bajo" else 'todos'

        # productos_encontrados = db.buscar_productos_filtrados(tipo_filtro_db, texto_busqueda)
        productos_encontrados = [("123", "Producto A", 150.0, 20, 5), ("456", "Producto B", 250.0, 3, 5)] # Simulación

        tree = self.app.productos_tab.tree_inventario
        tree.delete(*tree.get_children())

        if not productos_encontrados and texto_busqueda:
            tree.insert("", "end", values=("", "No se encontraron productos...", "", ""), tags=('mensaje_vacio',))
        else:
            for prod in productos_encontrados:
                codigo, nombre, precio, stock, umbral = prod
                tag = 'alerta_stock' if stock <= umbral else ''
                tree.insert("", "end", values=(codigo, nombre, f"${precio:,.2f}", stock), tags=(tag,))

    # --- LÓGICA DE GESTIÓN DE PRODUCTOS (ABM) ---

    def mostrar_ventana_agregar_producto(self, codigo_previo=""):
        """Muestra la ventana emergente para agregar un nuevo producto."""
        ventana_agregar = Toplevel(self.app)
        ventana_agregar.title("Agregar Nuevo Producto")
        ventana_agregar.transient(self.app)
        ventana_agregar.grab_set()
        
        frame_agregar = ttk.Frame(ventana_agregar, padding=20)
        frame_agregar.pack()

        entries = {}
        campos = ["Código de Barras", "Nombre del Producto", "Precio", "Stock Inicial"]
        for campo in campos:
            ttk.Label(frame_agregar, text=campo).pack(anchor="w")
            entry = ttk.Entry(frame_agregar, width=35, font=("Segoe UI", 11))
            entry.pack(fill="x", padx=5, pady=(0, 10))
            entries[campo] = entry

        entries["Código de Barras"].insert(0, codigo_previo)
        entries["Código de Barras"].focus_set()

        umbral_global = self.app.configuracion.get("umbral_alerta_stock", 5)
        ttk.Label(frame_agregar, text=f"Umbral de alerta por defecto: {umbral_global}", font=("Segoe UI", 9, "italic")).pack(pady=5)

        btn_guardar = ttk.Button(frame_agregar, text="Guardar Producto", style="success.TButton", command=lambda: self._guardar_nuevo_producto(entries, ventana_agregar))
        btn_guardar.pack(pady=10)

        entries["Código de Barras"].bind("<Return>", lambda e: entries["Nombre del Producto"].focus_set())
        entries["Nombre del Producto"].bind("<Return>", lambda e: entries["Precio"].focus_set())
        entries["Precio"].bind("<Return>", lambda e: entries["Stock Inicial"].focus_set())
        entries["Stock Inicial"].bind("<Return>", lambda e: btn_guardar.invoke())
        ventana_agregar.bind("<Escape>", lambda e: ventana_agregar.destroy())

    def _guardar_nuevo_producto(self, entries, ventana):
        """Valida y guarda los datos del nuevo producto."""
        try:
            codigo = entries["Código de Barras"].get().strip()
            nombre = entries["Nombre del Producto"].get().strip()
            precio = float(entries["Precio"].get())
            stock = int(entries["Stock Inicial"].get())

            if not all([codigo, nombre]):
                messagebox.showerror("Error", "El código y el nombre son obligatorios.", parent=ventana)
                return

            # umbral_global = self.app.configuracion.get("umbral_alerta_stock", 5)
            # exito = db.agregar_producto(codigo, nombre, precio, stock, umbral_global)
            # if exito:
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.", parent=self.app)
            ventana.destroy()
            self.filtrar_productos_y_recargar()
            # else: 
            #     messagebox.showerror("Error de Base de Datos", "No se pudo agregar el producto.", parent=ventana)
        except (ValueError, TypeError):
            messagebox.showerror("Error de Formato", "El precio y el stock deben ser números válidos.", parent=ventana)

    def modificar_producto(self):
        """Muestra la ventana emergente para modificar un producto."""
        item_seleccionado = self.app.productos_tab.tree_inventario.selection()
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto para modificar.", parent=self.app)
            return
        
        codigo_a_modificar = self.app.productos_tab.tree_inventario.item(item_seleccionado, "values")[0]
        
        # producto_db = db.buscar_producto(codigo_a_modificar)
        producto_db = ("123", "Producto A", 150.0, 20, 5) # Simulación
        if not producto_db: 
            messagebox.showerror("Error", "Producto no encontrado en la base de datos.", parent=self.app)
            return

        codigo_barras, nombre, precio, stock, _ = producto_db

        ventana_modificar = Toplevel(self.app)
        ventana_modificar.title(f"Modificar Producto: {codigo_barras}")
        ventana_modificar.transient(self.app)
        ventana_modificar.grab_set()

        frame_modificar = ttk.Frame(ventana_modificar, padding=20)
        frame_modificar.pack(expand=True)

        entries = {}
        campos = {"Nombre": nombre, "Precio": f"{precio:.2f}", "Stock": stock}
        for campo, valor in campos.items():
            ttk.Label(frame_modificar, text=f"{campo}:").pack(anchor="w", padx=5)
            entry = ttk.Entry(frame_modificar, width=35, font=("Segoe UI", 11))
            entry.insert(0, valor)
            entry.pack(fill="x", padx=5, pady=(0, 10))
            entries[campo] = entry

        btn_guardar = ttk.Button(
            frame_modificar,
            text="Guardar Cambios",
            style="success.TButton",
            command=lambda: self._guardar_modificaciones_producto(
                codigo_barras, entries, ventana_modificar
            )
        )
        btn_guardar.pack(pady=10)
        entries["Stock"].bind("<Return>", lambda e: btn_guardar.invoke())

    def _guardar_modificaciones_producto(self, codigo, entries, ventana):
        """Valida y guarda las modificaciones de un producto."""
        try:
            nuevo_nombre = entries["Nombre"].get().strip()
            nuevo_precio = float(entries["Precio"].get())
            nuevo_stock = int(entries["Stock"].get())

            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre del producto no puede estar vacío.", parent=ventana)
                return

            # exito = db.actualizar_producto(codigo, nuevo_nombre, nuevo_precio, nuevo_stock)
            # if exito:
            messagebox.showinfo("Éxito", f"Producto '{nuevo_nombre}' modificado.", parent=self.app)
            ventana.destroy()
            self.filtrar_productos_y_recargar()
            # else:
            #     messagebox.showerror("Error", "No se pudo actualizar el producto.", parent=ventana)
        except (ValueError, TypeError):
            messagebox.showerror("Error de Formato", "El precio y el stock deben ser números válidos.", parent=ventana)

    def eliminar_producto(self):
        """Elimina el producto seleccionado previa confirmación."""
        item_seleccionado = self.app.productos_tab.tree_inventario.selection()
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto para eliminar.", parent=self.app)
            return

        values = self.app.productos_tab.tree_inventario.item(item_seleccionado, "values")
        codigo, nombre = values[0], values[1]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que querés eliminar '{nombre}'?", parent=self.app):
            # exito = db.eliminar_producto(codigo)
            # if exito:
            messagebox.showinfo("Éxito", f"Producto '{nombre}' eliminado correctamente.", parent=self.app)
            self.filtrar_productos_y_recargar()
            # else: 
            #     messagebox.showerror("Error", "No se pudo eliminar el producto.", parent=self.app)

    def editar_con_doble_click(self, event):
        """Manejador para el evento de doble clic que inicia la modificación."""
        self.modificar_producto()

    # --- LÓGICA DE CARGA RÁPIDA ---

    def abrir_ventana_carga_rapida(self):
        """Muestra la ventana emergente para la carga rápida de múltiples productos."""
        ventana_carga = Toplevel(self.app)
        ventana_carga.title("Carga Rápida de Inventario")
        ventana_carga.transient(self.app)
        ventana_carga.grab_set()
        ventana_carga.resizable(False, False)

        productos_a_guardar = []

        frame_principal = ttk.Frame(ventana_carga, padding=20)
        frame_principal.pack(fill="both", expand=True)

        campos_entries = {
            "Código de Barras": ttk.Entry(frame_principal, font=("Segoe UI", 11)),
            "Nombre": ttk.Entry(frame_principal, font=("Segoe UI", 11)),
            "Precio": ttk.Entry(frame_principal, font=("Segoe UI", 11)),
            "Stock Inicial": ttk.Entry(frame_principal, font=("Segoe UI", 11)),
        }
        for i, (texto, entry) in enumerate(campos_entries.items()):
            ttk.Label(frame_principal, text=texto, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=2)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
        
        campos_entries["Código de Barras"].focus_set()
        lbl_contador = ttk.Label(frame_principal, text="Productos en lista: 0", font=("Segoe UI", 10, "italic"))
        lbl_contador.grid(row=len(campos_entries), column=0, columnspan=2, pady=10)

        def agregar_y_siguiente(event=None):
            codigo = campos_entries["Código de Barras"].get().strip()
            nombre = campos_entries["Nombre"].get().strip()
            precio_str = campos_entries["Precio"].get().strip()
            stock_str = campos_entries["Stock Inicial"].get().strip()

            if not all([codigo, nombre, precio_str, stock_str]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=ventana_carga)
                return
            try:
                precio = float(precio_str)
                stock = int(stock_str)
                productos_a_guardar.append((codigo, nombre, precio, stock))
                
                for entry in campos_entries.values():
                    entry.delete(0, 'end')
                
                lbl_contador.config(text=f"Productos en lista: {len(productos_a_guardar)}")
                campos_entries["Código de Barras"].focus_set()
            except ValueError:
                messagebox.showerror("Error de Formato", "El precio y el stock deben ser números válidos.", parent=ventana_carga)

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.grid(row=len(campos_entries) + 1, column=0, columnspan=2, pady=20)
        
        btn_agregar = ttk.Button(frame_botones, text="Agregar y Siguiente (Enter)", command=agregar_y_siguiente)
        btn_agregar.pack(side="left", padx=10)

        btn_finalizar = ttk.Button(frame_botones, text="Finalizar y Guardar Todo", style="success.TButton", command=lambda: self._finalizar_y_guardar_carga_rapida(productos_a_guardar, ventana_carga))
        btn_finalizar.pack(side="left", padx=10)

        campos_entries["Stock Inicial"].bind("<Return>", agregar_y_siguiente)
        ventana_carga.bind("<Escape>", lambda e: ventana_carga.destroy())

    def _finalizar_y_guardar_carga_rapida(self, productos, ventana):
        """Guarda la lista de productos de la carga rápida en la base de datos."""
        if not productos:
            messagebox.showwarning("Atención", "No hay productos en la lista para guardar.", parent=ventana)
            return

        if not messagebox.askyesno("Confirmar Guardado", f"¿Desea guardar {len(productos)} productos en la base de datos?", parent=ventana):
            return

        # agregados, errores = db.agregar_productos_en_lote(productos)
        agregados, errores = len(productos), [] # Simulación
        
        mensaje_final = f"Se guardaron {agregados} productos con éxito."
        if errores:
            messagebox.showwarning("Proceso con Errores", f"{mensaje_final}\n\nNo se pudieron agregar {len(errores)} productos.", parent=ventana)
        else:
            messagebox.showinfo("Éxito", mensaje_final, parent=self.app)
        
        ventana.destroy()
        self.filtrar_productos_y_recargar()

