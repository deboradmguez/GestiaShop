import tkinter as tk
from tkinter import messagebox

# from ..database import database_manager as db # Lo usaremos en el futuro

class InventarioLogic:
    """
    Controlador especializado para toda la lógica de la pestaña de Inventario.
    """
    def __init__(self, app_controller):
        self.app = app_controller
        # Almacena los datos del producto buscado para poder comparar si hubo cambios
        self.producto_actual_original = {} 

    def buscar_producto_para_inventario(self, event=None):
        """Busca un producto por código y muestra sus datos en los campos de edición."""
        codigo = self.app.inventario_tab.entry_codigo_inv.get().strip()
        if not codigo:
            return

        # --- Lógica de Base de Datos (simulada por ahora) ---
        # producto = db.buscar_producto(codigo)
        producto = ("789", "Producto de Inventario C", 300.0, 15, 5) # Simulación
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.", parent=self.app)
            self._limpiar_campos()
            return
        
        # Guardamos los datos originales para comparar después
        self.producto_actual_original = {
            "codigo": producto[0],
            "nombre": producto[1],
            "precio": producto[2],
            "stock": producto[3]
        }
        
        # --- Actualización de la UI ---
        # Llenamos la interfaz con los datos encontrados
        entries = self.app.inventario_tab.entries
        entries["nombre_edit"].delete(0, tk.END)
        entries["nombre_edit"].insert(0, self.producto_actual_original["nombre"])
        entries["precio_edit"].delete(0, tk.END)
        entries["precio_edit"].insert(0, f"{self.producto_actual_original['precio']:.2f}")
        entries["lbl_stock_actual"].config(text=str(self.producto_actual_original["stock"]))
        entries["stock_agregar"].delete(0, tk.END)
        
        self.app.inventario_tab.btn_confirmar_cambios.config(state="normal")
        entries["nombre_edit"].focus()

    def guardar_cambios_inventario(self, event=None):
        """
        Verifica si los datos del producto han cambiado y, si es así, los guarda.
        """
        if not self.producto_actual_original:
            return
        
        try:
            entries = self.app.inventario_tab.entries
            nuevo_nombre = entries["nombre_edit"].get().strip()
            nuevo_precio = float(entries["precio_edit"].get())
            stock_a_agregar = int(entries["stock_agregar"].get() or "0")
        except (ValueError, TypeError):
            messagebox.showerror("Error de Formato", "El precio y el stock a agregar deben ser números válidos.", parent=self.app)
            return

        # --- Lógica de Negocio ---
        # Comparamos si hubo algún cambio
        hubo_cambios = (
            nuevo_nombre != self.producto_actual_original["nombre"] or
            nuevo_precio != self.producto_actual_original["precio"] or
            stock_a_agregar != 0
        )

        if not hubo_cambios:
            messagebox.showinfo("Información", "No se detectaron cambios.", parent=self.app)
            self._limpiar_campos()
            return

        # Si hubo cambios, procedemos a guardar
        codigo = self.producto_actual_original["codigo"]
        
        # --- Lógica de Base de Datos (simulada) ---
        # exito = db.actualizar_producto_inventario(codigo, nuevo_nombre, nuevo_precio, stock_a_agregar)
        # if exito:
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.", parent=self.app)
        self._limpiar_campos()
        # Avisamos al controlador de productos que sus datos pueden haber cambiado
        self.app.productos_logic.filtrar_productos_y_recargar()
        # else:
        #     messagebox.showerror("Error", "No se pudo actualizar el producto.", parent=self.app)
        
    def _limpiar_campos(self):
        """Limpia todos los campos de la pestaña y resetea el estado."""
        self.producto_actual_original = {}
        tab = self.app.inventario_tab
        
        tab.entry_codigo_inv.delete(0, tk.END)
        for clave, widget in tab.entries.items():
            if clave == "lbl_stock_actual":
                widget.config(text="0")
            else:
                widget.delete(0, tk.END)
        
        tab.btn_confirmar_cambios.config(state="disabled")
        tab.entry_codigo_inv.focus()