from CTkMessagebox import CTkMessagebox 
from database import database_manager as db_manager
from utilities import helpers
import customtkinter as ctk

class ProductosLogic:
    """
    Controlador especializado para toda la lógica de la pestaña de Productos.
    """
    def __init__(self, app_controller):
        self.app = app_controller 

    # --- LÓGICA DE VISUALIZACIÓN Y FILTROS ---

    def filtrar_productos_y_recargar(self, event=None):
        """
        Obtiene los filtros de la UI, busca en la DB y actualiza la tabla de productos.
        """
        filtro_seleccionado = self.app.productos_tab.combo_filtro_productos.get()
        texto_busqueda = self.app.productos_tab.entry_buscar_producto.get().strip()
        tipo_filtro_db = 'bajo' if filtro_seleccionado == "Productos con stock bajo" else 'todos'

        productos_encontrados = db_manager.obtener_productos_filtrados(tipo_filtro_db, texto_busqueda)

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
        ventana_agregar = ctk.CTkToplevel(self.app)
        ventana_agregar.title("Agregar Nuevo Producto")
        
        frame_agregar = ctk.CTkFrame(ventana_agregar)
        frame_agregar.pack(padx=20, pady=20)

        entries = {}
        campos = ["Código de Barras", "Nombre del Producto", "Precio", "Stock Inicial"]
        for campo in campos:
            ctk.CTkLabel(frame_agregar, text=campo).pack(anchor="w")
            entry = ctk.CTkEntry(frame_agregar, width=35, font=("Segoe UI", 11))
            entry.pack(fill="x", padx=5, pady=(0, 10))
            entries[campo] = entry

        entries["Código de Barras"].insert(0, codigo_previo)
       

        umbral_global = self.app.configuracion.get("umbral_alerta_stock", 5)
        ctk.CTkLabel(frame_agregar, text=f"Umbral de alerta por defecto: {umbral_global}", font=("Segoe UI", 9, "italic")).pack(pady=5)

        btn_guardar = ctk.CTkButton(frame_agregar, text="Guardar Producto", fg_color="#28a745", hover_color="#218838", command=lambda: self._guardar_nuevo_producto(entries, ventana_agregar))
        btn_guardar.pack(pady=10)
        # --- BINDS ---
        entries["Código de Barras"].bind("<Return>", lambda e: entries["Nombre del Producto"].focus_set())
        entries["Nombre del Producto"].bind("<Return>", lambda e: entries["Precio"].focus_set())
        entries["Precio"].bind("<Return>", lambda e: entries["Stock Inicial"].focus_set())
        entries["Stock Inicial"].bind("<Return>", lambda e: btn_guardar.invoke())
        ventana_agregar.bind("<Escape>", lambda e: ventana_agregar.destroy())
        helpers.configurar_dialogo(ventana_agregar, self.app, entries["Código de Barras"])
        
        
    def _guardar_nuevo_producto(self, entries, ventana):
        """Valida y guarda los datos del nuevo producto."""
        try:
            codigo = entries["Código de Barras"].get().strip()
            nombre = entries["Nombre del Producto"].get().strip()
            precio = float(entries["Precio"].get())
            stock = int(entries["Stock Inicial"].get())

            if not all([codigo, nombre]):
                self.app.notificar_error("El código y el nombre son obligatorios.")
                return

            umbral_global = self.app.configuracion.get("umbral_alerta_stock", 5)
            exito = db_manager.agregar_producto_nuevo(codigo, nombre, precio, stock, umbral_global)
            if exito:
                self.app.notificar_exito(f"Producto '{nombre}' agregado correctamente.")
    
                ventana.withdraw()
                ventana.after(100, ventana.destroy)
    
                self.filtrar_productos_y_recargar()
            else: 
                self.app.notificar_error("No se pudo agregar el producto.")
        except (ValueError, TypeError):
            self.app.notificar_error("El precio y el stock deben ser números válidos.")

    def modificar_producto(self):

        item_seleccionado = self.app.productos_tab.tree_inventario.selection()
        if not item_seleccionado:
            self.app.notificar_alerta("Seleccioná un producto para modificar.")
            return
        
        codigo_a_modificar = self.app.productos_tab.tree_inventario.item(item_seleccionado, "values")[0]
        
        producto_db = db_manager.obtener_producto_por_codigo(codigo_a_modificar)
    
        if not producto_db: 
            self.app.notificar_error("Producto no encontrado en la base de datos.")
            return

        codigo_barras, nombre, precio, stock, _ = producto_db

        ventana_modificar = ctk.CTkToplevel(self.app)
        ventana_modificar.title(f"Modificar Producto: {codigo_barras}")
        frame_modificar = ctk.CTkFrame(ventana_modificar)
        frame_modificar.pack(expand=True, padx=20, pady=20)

        entries = {}
        campos = {"Nombre": nombre, "Precio": f"{precio:.2f}", "Stock": stock}
        for campo, valor in campos.items():
            ctk.CTkLabel(frame_modificar, text=f"{campo}:").pack(anchor="w", padx=5)
            entry = ctk.CTkEntry(frame_modificar, width=35, font=("Segoe UI", 11))
            entry.insert(0, valor)
            entry.pack(fill="x", padx=5, pady=(0, 10))
            entries[campo] = entry
        btn_guardar = ctk.CTkButton(
            frame_modificar,
            text="Guardar Cambios",
            fg_color="#28a745", hover_color="#218838",
            command=lambda: self._guardar_modificaciones_producto(
                codigo_barras, entries, ventana_modificar
            )
        )
        btn_guardar.pack(pady=10)
        
        entries["Nombre"].bind("<Return>", lambda e: entries["Precio"].focus_set())
        entries["Precio"].bind("<Return>", lambda e: entries["Stock"].focus_set())
        entries["Stock"].bind("<Return>", lambda e: btn_guardar.invoke())
        ventana_modificar.bind("<Escape>", lambda e: ventana_modificar.destroy())
        
        helpers.configurar_dialogo(ventana_modificar, self.app, entries["Nombre"])

    def _guardar_modificaciones_producto(self, codigo, entries, ventana):
        """Valida y guarda las modificaciones de un producto."""
        try:
            nuevo_nombre = entries["Nombre"].get().strip()
            nuevo_precio = float(entries["Precio"].get())
            nuevo_stock = int(entries["Stock"].get())

            if not nuevo_nombre:
                self.app.notificar_error("El nombre del producto no puede estar vacío.")
                return

            exito = db_manager.actualizar_producto_existente(codigo, nuevo_nombre, nuevo_precio, nuevo_stock)
            if exito:
                self.app.notificar_exito(f"Producto '{nuevo_nombre}' modificado.")
    
                ventana.withdraw()
                ventana.after(100, ventana.destroy)
    
                self.filtrar_productos_y_recargar()
                self.app.app_logic.actualizar_alertas_stock()
            else:
                self.app.notificar_error("No se pudo actualizar el producto.")
        except (ValueError, TypeError):
            self.app.notificar_error("El precio y el stock deben ser números válidos.")
    def eliminar_producto(self):
        """Elimina el producto seleccionado previa confirmación."""
        item_seleccionado = self.app.productos_tab.tree_inventario.selection()
        if not item_seleccionado:
            self.app.notificar_error("Seleccioná un producto para eliminar.")
            return

        values = self.app.productos_tab.tree_inventario.item(item_seleccionado, "values")
        codigo, nombre = values[0], values[1]
        
       
        dialogo = CTkMessagebox(
            title="Confirmar Eliminación",
            message=f"¿Estás seguro de que querés eliminar '{nombre}'?",
            icon="warning", 
            option_1="Cancelar",
            option_2="Eliminar",
            sound=True,
            button_color="#D32F2F", 
            button_hover_color="#B71C1C"
        )
        
        if dialogo.get() == "Eliminar":
        
            exito = db_manager.eliminar_producto_existente(codigo)
            if exito:
                self.app.notificar_exito(f"Producto '{nombre}' eliminado correctamente.")
                self.filtrar_productos_y_recargar()
            else: 
                self.app.notificar_error("No se pudo eliminar el producto.")

    def editar_con_doble_click(self, event):
        """Manejador para el evento de doble clic que inicia la modificación."""
        self.modificar_producto()

    def buscar_y_seleccionar_producto(self, codigo_producto):
        """
        Busca un producto por su código en la pestaña de productos,
        lo selecciona y lo enfoca.
        """
        tab = self.app.productos_tab
        tree = tab.tree_inventario

        
        tab.entry_buscar_producto.delete(0, 'end')
        tab.entry_buscar_producto.insert(0, codigo_producto)
        self.filtrar_productos_y_recargar()

        
        for item_id in tree.get_children():
            valores = tree.item(item_id, "values")
            if valores and valores[0] == codigo_producto:
                
                tree.selection_set(item_id)
                tree.focus(item_id)
                tree.see(item_id) 
                break

    # --- LÓGICA DE CARGA RÁPIDA ---

    def abrir_ventana_carga_rapida(self):
        """Muestra la ventana emergente para la carga rápida de múltiples productos."""
        ventana_carga = ctk.CTkToplevel(self.app)
        ventana_carga.title("Carga Rápida de Inventario")
        ventana_carga.transient(self.app)

        productos_a_guardar = []

        frame_principal = ctk.CTkFrame(ventana_carga)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        campos_entries = {
            "Código de Barras": ctk.CTkEntry(frame_principal, font=("Segoe UI", 11)),
            "Nombre": ctk.CTkEntry(frame_principal, font=("Segoe UI", 11)),
            "Precio": ctk.CTkEntry(frame_principal, font=("Segoe UI", 11)),
            "Stock Inicial": ctk.CTkEntry(frame_principal, font=("Segoe UI", 11)),
        }
        for i, (texto, entry) in enumerate(campos_entries.items()):
            ctk.CTkLabel(frame_principal, text=texto, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=2)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
    
        lbl_contador = ctk.CTkLabel(frame_principal, text="Productos en lista: 0", font=("Segoe UI", 10, "italic"))
        lbl_contador.grid(row=len(campos_entries), column=0, columnspan=2, pady=10)

        def agregar_y_siguiente(event=None):
            codigo = campos_entries["Código de Barras"].get().strip()
            nombre = campos_entries["Nombre"].get().strip()
            precio_str = campos_entries["Precio"].get().strip()
            stock_str = campos_entries["Stock Inicial"].get().strip()

            if not all([codigo, nombre, precio_str, stock_str]):
                self.app.notificar_error("Todos los campos son obligatorios.")
                return
            try:
                precio = float(precio_str)
                stock = int(stock_str)
                productos_a_guardar.append((codigo, nombre, precio, stock))
                
                for entry in campos_entries.values():
                    entry.delete(0, 'end')
                
                lbl_contador.configure(text=f"Productos en lista: {len(productos_a_guardar)}")
            except ValueError:
                self.app.notificar_error("El precio y el stock deben ser números válidos.")

        frame_botones = ctk.CTkFrame(frame_principal)
        frame_botones.grid(row=len(campos_entries) + 1, column=0, columnspan=2, pady=20)
        
        btn_agregar = ctk.CTkButton(frame_botones, text="Agregar y Siguiente (Enter)", command=agregar_y_siguiente)
        btn_agregar.pack(side="left", padx=10)

        btn_finalizar = ctk.CTkButton(frame_botones, text="Finalizar y Guardar Todo",
                                      fg_color="#28a745", hover_color="#218838",
                                      command=lambda: self._finalizar_y_guardar_carga_rapida(productos_a_guardar, ventana_carga))
        btn_finalizar.pack(side="left", padx=10)
        helpers.configurar_dialogo(ventana_carga, self.app, campos_entries["Código de Barras"])
        campos_entries["Stock Inicial"].bind("<Return>", agregar_y_siguiente)
        ventana_carga.bind("<Escape>", lambda e: ventana_carga.destroy())

    def _finalizar_y_guardar_carga_rapida(self, productos, ventana):
        """Guarda la lista de productos de la carga rápida en la base de datos."""
        if not productos:
            self.app.notificar_alerta("No hay productos en la lista para guardar.")
            return

        dialogo = CTkMessagebox(
                title="Confirmar Guardado",
                message=f"¿Desea guardar {len(productos)} productos en la base de datos?",
                icon="question",
                option_1="Cancelar",
                option_2="Guardar",
                sound=True
            )
        
        if dialogo.get() != "Guardar":
            return

        agregados, errores = db_manager.agregar_productos_en_lote(productos)
        
        mensaje_final = f"Se guardaron {agregados} productos con éxito."
        if errores:
            self.app.notificar_alerta(f"{mensaje_final}\n\nNo se pudieron agregar {len(errores)} productos.")
        else:
            self.app.notificar_exito(mensaje_final)
        
        ventana.withdraw()
        ventana.after(100, ventana.destroy)
        self.filtrar_productos_y_recargar()

    def realizar_busqueda_productos(self, termino_busqueda, tree_widget):
        """
        Busca productos por nombre y actualiza un Treeview con los resultados.
        """
        if not termino_busqueda:
            tree_widget.delete(*tree_widget.get_children())
            return

        productos_encontrados = db_manager.buscar_productos_por_nombre(termino_busqueda)
        
        tree_widget.delete(*tree_widget.get_children())
        for prod in productos_encontrados:
            codigo, nombre, precio, stock, _ = prod
            tree_widget.insert(
                "", "end", 
                values=(nombre, f"${precio:,.2f}", stock), 
                tags=(codigo,)
            )