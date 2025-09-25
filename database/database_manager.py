import sqlite3
from .connection import conectar_db
from . import queries

#PRODUCTOS
def agregar_producto_nuevo(codigo, nombre, precio, stock, umbral):
    try:
        with conectar_db() as conn:
            queries.agregar_producto(conn, codigo, nombre, precio, stock, umbral)
            return True
    except sqlite3.IntegrityError:
        # Este error específico ocurre si el 'codigo_barras' ya existe (UNIQUE).
        print(f"Error en DB: El código de barras '{codigo}' ya existe.")
        return False
    except sqlite3.Error as e:
        print(f"Error en DB (agregar_producto_nuevo): {e}")
        return False
def actualizar_producto_existente(codigo, nombre, precio, stock):
    try:
        with conectar_db() as conn:
            # Llama a la función de queries.py
            queries.actualizar_producto(conn, codigo, nombre, precio, stock)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (actualizar_producto_existente): {e}")
        return False
    
def eliminar_producto_existente(codigo):
    try:
        with conectar_db() as conn:
            queries.eliminar_producto(conn, codigo)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (eliminar_producto_existente): {e}")
        return False
def obtener_lista_productos_a_reponer():
    try:
        with conectar_db() as conn:
            productos = queries.obtener_productos_para_reponer(conn)
            return productos
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_lista_productos_a_reponer): {e}")
        return [] # Devuelve una lista vacía en caso de error
def obtener_producto_por_codigo(codigo):
    try:
        with conectar_db() as conn:
            producto = queries.buscar_producto(conn, codigo)
            return producto
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_producto_por_codigo): {e}")
        return None

def obtener_productos_filtrados(tipo_filtro, texto_busqueda):
    try:
        with conectar_db() as conn:
            productos = queries.buscar_productos_filtrados(conn, tipo_filtro, texto_busqueda)
            return productos
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_productos_filtrados): {e}")
        return []
def agregar_productos_en_lote(productos):
    agregados = 0
    errores = []
    umbral_global = 5 # Podríamos obtener esto de la config en el futuro

    # Preparamos la lista de tuplas para la base de datos
    productos_para_db = [
        (codigo, nombre, precio, stock, umbral_global)
        for codigo, nombre, precio, stock in productos
    ]

    try:
        with conectar_db() as conn:
            queries.agregar_productos_en_lote(conn, productos_para_db)
            agregados = len(productos_para_db)
            return agregados, errores
    except sqlite3.IntegrityError as e:
        # Este error ocurre si un código de barras ya existe
        #se podria intentar insertar uno por uno para ver cuál falla
        print(f"Error de integridad en DB (agregar_productos_en_lote): {e}")
        return 0, [str(e)]
    except sqlite3.Error as e:
        print(f"Error en DB (agregar_productos_en_lote): {e}")
        return 0, [str(e)]

#VENTAS
def registrar_nueva_venta(carrito, pago_efectivo, pago_transferencia, referencia):
    try:
        with conectar_db() as conn:
            queries.registrar_venta(conn, carrito, pago_efectivo, pago_transferencia, referencia)
        return True
    except sqlite3.Error as e:
        print(f"Error en DB (registrar_nueva_venta): {e}")
        # La transacción se revierte automáticamente si hay una excepción
        return False  
def obtener_historial_por_fecha(fecha):
    try:
        with conectar_db() as conn:
            historial = queries.obtener_historial_ventas_detallado(conn, fecha)
            return historial
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_historial_por_fecha): {e}")
        return []
def anular_venta_existente(id_transaccion):
    """
    Gestiona la anulación de una venta de forma transaccional.
    Devuelve True si fue exitoso, False si hubo un error.
    """
    try:
        with conectar_db() as conn:
            queries.anular_venta(conn, id_transaccion)
        return True
    except sqlite3.Error as e:
        print(f"Error en DB (anular_venta_existente): {e}")
        return False 

# Por ejemplo:
# def agregar_producto_nuevo(datos): ...
# def registrar_una_venta(carrito, pago_info): ...
# def obtener_historial_del_dia(fecha): ...
# etc.