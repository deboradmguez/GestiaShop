import sqlite3, json
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
    
#caja

def consultar_estado_caja(fecha_db):
    try:
        with conectar_db() as conn:
            caja_hoy = queries.obtener_corte_caja_por_fecha(conn, fecha_db)

            if not caja_hoy:
                return ('inexistente', None)

            usuario, contado_final, fondo_inicial, diferencia = caja_hoy
            
            datos_caja = {
                "usuario": usuario,
                "fondo_inicial": fondo_inicial,
                "contado_final": contado_final,
                "diferencia": diferencia
            }

            if contado_final is None:
                return ('abierta', datos_caja)  # La caja está abierta si no tiene monto final
            else:
                return ('cerrada', datos_caja)   # La caja ya se cerró
                
    except sqlite3.Error as e:
        print(f"Error en DB (consultar_estado_caja): {e}")
        return ('error', None) 
def registrar_apertura_caja(fecha_db, fondo_inicial, usuario):
    try:
        with conectar_db() as conn:
            queries.abrir_caja(conn, fecha_db, fondo_inicial, usuario)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (registrar_apertura_caja): {e}")
        return False
def obtener_resumen_ventas_del_dia(fecha_db):
    try:
        with conectar_db() as conn:
            return queries.obtener_cierre_caja_del_dia(conn, fecha_db)
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_resumen_ventas_del_dia): {e}")
        return [('Efectivo', 0.0), ('Transferencia', 0.0)]
def registrar_cierre_caja(fecha_db, monto_final, diferencia):
    try:
        with conectar_db() as conn:
            queries.cerrar_caja(conn, fecha_db, monto_final, diferencia)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (registrar_cierre_caja): {e}")
        return False
def registrar_ajuste_caja(fecha_db, monto_corregido, diferencia_corregida):
    try:
        with conectar_db() as conn:
            queries.ajustar_cierre_de_caja(conn, fecha_db, monto_corregido, diferencia_corregida)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (registrar_ajuste_caja): {e}")
        return False    
 
#ESTADISTICAS

def obtener_resumen_ventas_periodo(fecha_inicio_db, fecha_fin_db):
   
    try:
        with conectar_db() as conn:
            resultados = queries.obtener_resumen_ventas_periodo(conn, fecha_inicio_db, fecha_fin_db)
            return {
                "efectivo": resultados[0] or 0.0,
                "transferencia": resultados[1] or 0.0,
                "total": resultados[2] or 0.0
            }
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_resumen_ventas_periodo): {e}")
        return {"efectivo": 0.0, "transferencia": 0.0, "total": 0.0}

def obtener_top_productos_periodo(fecha_inicio_db, fecha_fin_db, limite=5):
    try:
        with conectar_db() as conn:
            return queries.obtener_top_productos_periodo(conn, fecha_inicio_db, fecha_fin_db, limite)
    except sqlite3.Error as e:
        print(f"Error en DB (obtener_top_productos_periodo): {e}")
        return []   
 
 #configuracion
 
def cargar_configuracion_completa():
    """
    Gestiona la carga de la configuración completa y la formatea como un diccionario.
    """
    config = {}
    try:
        with conectar_db() as conn:
            for clave, valor in queries.cargar_configuracion(conn):
                try:
                    # Intenta convertir de JSON si es un tipo complejo (como booleanos)
                    config[clave] = json.loads(valor)
                except (json.JSONDecodeError, TypeError):
                    config[clave] = valor # Si no, lo deja como texto
        return config
    except sqlite3.Error as e:
        print(f"Error en DB (cargar_configuracion_completa): {e}")
        return {} # Devuelve un diccionario vacío en caso de error

def guardar_configuracion(nuevos_valores):
    try:
        with conectar_db() as conn:
            # Preparamos los valores para guardarlos como texto
            valores_a_guardar = {
                k: json.dumps(v) if isinstance(v, bool) else str(v)
                for k, v in nuevos_valores.items()
            }
            queries.guardar_configuracion_multiples(conn, valores_a_guardar)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (guardar_configuracion): {e}")
        return False

def restaurar_configuracion():
    from logic.configuracion_logic import CONFIG_DEFAULT 
    try:
        with conectar_db() as conn:
            queries.restaurar_configuracion_default(conn, CONFIG_DEFAULT)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (restaurar_configuracion): {e}")
        return False   

#inventario


def actualizar_desde_inventario(codigo, nombre, precio, stock_a_agregar):
    try:
        with conectar_db() as conn:
            queries.actualizar_producto_inventario(conn, codigo, nombre, precio, stock_a_agregar)
            return True
    except sqlite3.Error as e:
        print(f"Error en DB (actualizar_desde_inventario): {e}")
        return False