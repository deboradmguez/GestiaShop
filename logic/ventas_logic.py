import tkinter as tk
from tkinter import Toplevel, ttk
import uuid

# Importamos las ventanas emergentes que son parte de la UI de esta lógica
from ui.windows.busqueda_window import BusquedaWindow
from ui.windows.cobrar_window import CobrarWindow
from utilities.dialogs import ConfirmacionDialog
from database import database_manager as db_manager
from utilities import helpers

class VentasLogic:
    """
    Controlador especializado para toda la lógica de la pestaña de Ventas.
    """
    def __init__(self, app_controller):
        self.app = app_controller # Referencia a la App principal para acceder al estado y las vistas

    # --- LÓGICA PRINCIPAL DEL CARRITO ---

    def buscar_y_agregar_a_carrito(self):
        """Busca un producto por código y lo agrega al carrito."""
        codigo = self.app.ventas_tab.entry_codigo.get()
        if not codigo: return

        producto_db = db_manager.obtener_producto_por_codigo(codigo)
        producto_db = ("12345", "Producto de Ejemplo", 150.0, 50, 5) # Simulación

        if producto_db:
            codigo_barras, nombre, precio, stock_total, _ = producto_db
            stock_en_carrito = self.app.carrito.get(codigo_barras, {}).get("cantidad", 0)
            if stock_total - stock_en_carrito <= 0:
                self.app.notificar_alerta(f"No hay más stock disponible para '{nombre}'.", parent=self.app)
                self.app.ventas_tab.entry_codigo.delete(0, 'end')
                return
            self._agregar_a_carrito((codigo_barras, nombre, precio, 1), stock_total)
            self.app.ventas_tab.entry_codigo.delete(0, 'end')
        else:
            self.app.notificar_alerta("Producto no encontrado.")
            self.app.ventas_tab.entry_codigo.delete(0, 'end')

    def _agregar_a_carrito(self, producto, stock_info=None):
        """Método interno para añadir o actualizar un producto en el carrito."""
        codigo, nombre, precio, cantidad = producto
        if codigo in self.app.carrito:
            self.app.carrito[codigo]["cantidad"] += cantidad
        else:
            self.app.carrito[codigo] = {"nombre": nombre, "precio": precio, "cantidad": cantidad, "stock": stock_info}
        self._recalcular_total_carrito()
        self.app.ventas_tab.actualizar_vista(self.app.carrito, self.app.total_venta)

    def _recalcular_total_carrito(self):
        """Calcula el total de la venta basado en el estado actual del carrito."""
        self.app.total_venta = sum(d["precio"] * d["cantidad"] for d in self.app.carrito.values())

    def vaciar_carrito(self):
        """Limpia todos los productos del carrito previa confirmación."""
        if not self.app.carrito: return
        
        dialogo = ConfirmacionDialog(
            parent=self.app, 
            title="Confirmar Acción", 
            message="¿Desea vaciar el carrito por completo?"
        )
        
        # 3. Mostramos el diálogo y esperamos la respuesta
        respuesta = dialogo.show()

        if respuesta:
            self.app.carrito.clear()
            self._recalcular_total_carrito()
            self.app.ventas_tab.actualizar_vista(self.app.carrito, self.app.total_venta)
            self.app.notificar_exito("Carrito vaciado")
    
    def quitar_producto_del_carrito(self):
        """Quita el producto seleccionado en la tabla del carrito."""
        item_id = self.app.ventas_tab.tree_carrito.focus()
        if not item_id: return
        
        nombre_producto = self.app.ventas_tab.tree_carrito.item(item_id, "values")[0]
        codigo_a_quitar = next((c for c, d in self.app.carrito.items() if d["nombre"] == nombre_producto), None)

        if codigo_a_quitar:
            del self.app.carrito[codigo_a_quitar]
            self._recalcular_total_carrito()
            self.app.ventas_tab.actualizar_vista(self.app.carrito, self.app.total_venta)

    # --- LÓGICA DE VENTANAS EMERGENTES (Pop-ups) ---

    def modificar_cantidad_carrito(self, event=None):
        """Muestra una ventana emergente para modificar la cantidad de un producto."""
        item_id = self.app.ventas_tab.tree_carrito.focus()
        if not item_id: return
        
        valores = self.app.ventas_tab.tree_carrito.item(item_id, "values")
        nombre_producto_ui = valores[0]
        codigo_a_modificar = next((c for c, d in self.app.carrito.items() if d["nombre"] == nombre_producto_ui), None)
        if not codigo_a_modificar: return
        
        producto_en_carrito = self.app.carrito[codigo_a_modificar]
        nombre = producto_en_carrito["nombre"]
        cantidad_actual = producto_en_carrito["cantidad"]
        
        # producto_db = db.buscar_producto(codigo_a_modificar)
        producto_db = ("12345", "Producto de Ejemplo", 150.0, 50, 5) # Simulación
        stock_total_db = producto_db[3] if producto_db else None

        # Creación de la ventana
        ventana_cantidad = Toplevel(self.app)
        ventana_cantidad.title("Modificar Cantidad")
        ventana_cantidad.transient(self.app)
        ventana_cantidad.grab_set()
        ventana_cantidad.resizable(False, False)

        frame = ttk.Frame(ventana_cantidad, padding=20)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text=f"Nueva cantidad para '{nombre}':").pack(pady=5)
        entry_cantidad = ttk.Entry(frame, justify="center")
        entry_cantidad.insert(0, str(cantidad_actual))
        entry_cantidad.pack(pady=5)
        entry_cantidad.focus()

        btn_guardar = ttk.Button(frame, text="Guardar", command=lambda: self._guardar_nueva_cantidad(codigo_a_modificar, entry_cantidad, stock_total_db, ventana_cantidad))
        btn_guardar.pack(pady=10)
        helpers.centrar_ventana(ventana_cantidad, self.app)
        entry_cantidad.bind("<Return>", lambda e: btn_guardar.invoke())
        ventana_cantidad.bind("<Escape>", lambda e: ventana_cantidad.destroy())

    def _guardar_nueva_cantidad(self, codigo, entry, stock_disponible, ventana):
        """Valida y guarda la nueva cantidad de un producto."""
        try:
            nueva_cantidad = int(entry.get().strip())
            if nueva_cantidad <= 0:
                self.app.notificar_alerta("La cantidad debe ser mayor a cero.")
                return
            if stock_disponible is not None and nueva_cantidad > stock_disponible:
                self.app.notificar_alerta(f"Stock Insuficiente. El stock máximo es {stock_disponible}.", parent=ventana)
                return

            self.app.carrito[codigo]["cantidad"] = nueva_cantidad
            self._recalcular_total_carrito()
            self.app.ventas_tab.actualizar_vista(self.app.carrito, self.app.total_venta)
            ventana.destroy()
        except ValueError:
            self.app.notificar_error("La cantidad debe ser un número válido.")

    def mostrar_ventana_busqueda(self):
        """Muestra la ventana de búsqueda de productos por nombre."""
        BusquedaWindow(parent=self.app, controller=self.app)

    def agregar_producto_desde_busqueda(self, codigo_barras):
        """Agrega un producto al carrito desde la ventana de búsqueda."""
        # producto_db = db.buscar_producto(codigo_barras)
        producto_db = ("45678", "Producto Buscado", 250.0, 30, 5) # Simulación
        if producto_db:
            _, nombre, precio, stock, _ = producto_db
            self._agregar_a_carrito((codigo_barras, nombre, precio, 1), stock)

    def agregar_producto_comun(self):
        """Muestra una ventana para agregar un producto no inventariado."""
        ventana_comun = Toplevel(self.app)
        ventana_comun.title("Agregar Producto Común")
        ventana_comun.transient(self.app)
        ventana_comun.grab_set()

        frame = ttk.Frame(ventana_comun, padding=20)
        frame.pack()

        campos = {"Nombre": ttk.Entry(frame), "Precio": ttk.Entry(frame), "Cantidad": ttk.Entry(frame)}
        for texto, entry in campos.items():
            ttk.Label(frame, text=f"{texto}:").pack()
            entry.pack(pady=5)
        campos["Nombre"].focus()

        btn_confirmar = ttk.Button(frame, text="Agregar", command=lambda: self._confirmar_y_agregar_comun(campos, ventana_comun))
        btn_confirmar.pack(pady=10)
        
        campos["Cantidad"].bind("<Return>", lambda e: btn_confirmar.invoke())
        helpers.centrar_ventana(ventana_comun, self.app)

    def _confirmar_y_agregar_comun(self, entries, ventana):
        """Valida y agrega un producto común al carrito."""
        try:
            nombre = entries["Nombre"].get().strip()
            precio = float(entries["Precio"].get())
            cantidad = int(entries["Cantidad"].get())
            if not nombre or precio <= 0 or cantidad <= 0:
                self.app.notificar_alerta("Todos los campos son obligatorios y los números deben ser positivos.")
                return

            codigo_comun = f"PROD_COMUN-{uuid.uuid4()}"
            self._agregar_a_carrito((codigo_comun, nombre, precio, cantidad), None)
            ventana.destroy()
        except (ValueError, TypeError):
            self.app.notificar_error("Precio y cantidad deben ser números válidos.")

    # --- LÓGICA DE FINALIZACIÓN DE VENTA ---

    def mostrar_ventana_cobrar(self):
        """Valida y muestra la ventana de cobro."""
        if not self.app.carrito:
            self.app.notificar_alerta("El carrito está vacío.")
            return
        CobrarWindow(parent=self.app, controller=self.app, total_a_cobrar=self.app.total_venta)

    def finalizar_venta(self, payment_data):
        """Procesa la venta, la guarda, y limpia el estado."""
        if not self.app.carrito: return False
        
        venta_exitosa = db_manager.registrar_nueva_venta(
             carrito=self.app.carrito,
             pago_efectivo=payment_data.get("pago_efectivo", 0.0),
             pago_transferencia=payment_data.get("pago_transferencia", 0.0),
             referencia=payment_data.get("referencia", "")
         )
        if venta_exitosa:
            self.app.carrito.clear()
            self._recalcular_total_carrito()
            self.app.ventas_tab.actualizar_vista(self.app.carrito, self.app.total_venta)
            
            # Notificar a otros controladores que una venta ocurrió
            if hasattr(self.app, 'productos_logic'):
                self.app.productos_logic.filtrar_productos_y_recargar()
            # if hasattr(self.app, 'historial_logic'):
            #     self.app.historial_logic.recargar_historial()
            
            self.app.notificar_exito("Venta realizada correctamente.")
            return True
        else:
            self.app.notificar_error("No se pudo registrar la venta.")
            return False

