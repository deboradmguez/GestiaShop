import sqlite3, os, sys, uuid
from datetime import datetime
from tkinter import messagebox
from connection import conectar_db

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def obtener_ruta_datos_usuario():
    """
    Obtiene la ruta a una carpeta segura en AppData para guardar los datos.
    Crea la carpeta si no existe.
    """
    # Obtenemos la ruta a la carpeta AppData del usuario (ej: C:\Users\TuUsuario\AppData\Roaming)
    ruta_appdata = os.environ.get('APPDATA')
    if not ruta_appdata:
        # Si no se encuentra, usamos la carpeta de inicio como alternativa
        ruta_appdata = os.path.expanduser("~")

    # Creamos nuestra carpeta de datos dentro de AppData
    ruta_datos = os.path.join(ruta_appdata, "PolirrubroBianca")
    os.makedirs(ruta_datos, exist_ok=True)
    return ruta_datos

# --- Funciones para gestionar productos ---
def agregar_producto(conexion, codigo, nombre, precio, stock, umbral):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (codigo_barras, nombre, precio, stock, umbral_alerta) VALUES (?, ?, ?, ?, ?)",
                   (codigo, nombre, precio, stock, umbral))
    conexion.commit()

def buscar_producto(conexion, codigo):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo_barras = ?", (codigo,))
    return cursor.fetchone()

def actualizar_stock(conexion, codigo, cantidad):
    cursor = conexion.cursor()
    cursor.execute("UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?", (cantidad, codigo))
    conexion.commit()

# app_multirrubro.py

def registrar_venta(conexion, carrito, pago_efectivo, pago_transferencia, referencia):
    """
    Registra una venta completa y sus productos, asignando un número de ticket correlativo.
    """
    cursor = conexion.cursor()
    
    id_transaccion = str(uuid.uuid4())
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_venta = sum(item["precio"] * item["cantidad"] for item in carrito.values())

    try:
        cursor.execute("SELECT MAX(ticket_numero) FROM ventas")
        ultimo_ticket = cursor.fetchone()[0]
        
        # 2. Calcular el nuevo número (si no hay ninguno, empieza en 1)
        nuevo_ticket = (ultimo_ticket or 0) + 1
        # --- FIN DE LA NUEVA LÓGICA ---
        
        # Guarda la transacción completa, incluyendo el nuevo número de ticket
        cursor.execute(
            """
            INSERT INTO ventas (id_transaccion, fecha_hora, pago_efectivo, pago_transferencia, referencia, total_venta, ticket_numero) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (id_transaccion, fecha_hora, pago_efectivo, pago_transferencia, referencia, total_venta, nuevo_ticket)
        )
        
        # Recorre el carrito para guardar cada producto en 'detalle_ventas'
        for codigo, item in carrito.items():
            nombre = item['nombre']
            cantidad = item['cantidad']
            precio_unitario = item['precio']
            total_fila = item['total_fila']
            
            cursor.execute(
                "INSERT INTO detalle_ventas (id_transaccion, codigo_producto, nombre_producto, precio_unitario, cantidad, total_fila) VALUES (?, ?, ?, ?, ?, ?)",
                (id_transaccion, codigo, nombre, precio_unitario, cantidad, total_fila)
            )
            
            # Actualiza el stock de cada producto que no sea "común"
            if not codigo.startswith("PROD_COMUN-"):
                cursor.execute(
                    "UPDATE productos SET stock = stock - ? WHERE codigo_barras = ?",
                    (cantidad, codigo)
                )
            
        conexion.commit()
        return True
        
    except sqlite3.Error as e:
        print(f"Error al registrar la venta: {e}")
        conexion.rollback()
        return False
    
def buscar_productos_por_nombre(conexion, nombre_producto):
    cursor = conexion.cursor()
    cursor.execute("SELECT codigo_barras, nombre, precio, stock, umbral_alerta FROM productos WHERE nombre LIKE ?", (f'%{nombre_producto}%',))
    return cursor.fetchall()

def buscar_productos_filtrados(conexion, filtro_stock, texto_busqueda):
    """
    Busca productos combinando un filtro de stock y una búsqueda por texto.
    
    filtro_stock: 'todos' o 'bajo'.
    texto_busqueda: término para buscar en nombre o código.
    """
    cursor = conexion.cursor()
    
    # Preparamos los parámetros de búsqueda
    texto_like = f"%{texto_busqueda}%"
    
    # Construimos la consulta base
    query = """
        SELECT codigo_barras, nombre, precio, stock, umbral_alerta
        FROM productos
    """
    
    params = []
    
    # Añadimos las condiciones WHERE
    if filtro_stock == 'bajo':
        query += " WHERE stock <= umbral_alerta"
        if texto_busqueda:
            query += " AND (LOWER(nombre) LIKE ? OR codigo_barras LIKE ?)"
            params.extend([texto_like, texto_like])
    else: # 'todos'
        if texto_busqueda:
            query += " WHERE LOWER(nombre) LIKE ? OR codigo_barras LIKE ?"
            params.extend([texto_like, texto_like])
            
    query += " ORDER BY nombre"
    
    cursor.execute(query, params)
    return cursor.fetchall()

def obtener_cierre_caja_del_dia(conexion, fecha_str):
    cursor = conexion.cursor()
    
    # Hacemos una sola consulta para mayor eficiencia, añadiendo el filtro por estado
    cursor.execute("""
        SELECT SUM(pago_efectivo), SUM(pago_transferencia) 
        FROM ventas
        WHERE DATE(fecha_hora) = ? AND estado = 'Completada'
    """, (fecha_str,))
    
    resultados = cursor.fetchone()
    
    # Si no hay ventas en esa fecha, los valores serán None, los convertimos a 0.0
    total_efectivo = resultados[0] if resultados and resultados[0] is not None else 0.0
    total_transferencia = resultados[1] if resultados and resultados[1] is not None else 0.0

    # Retornar los resultados en el formato esperado
    return [('Efectivo', total_efectivo), ('Transferencia', total_transferencia)]

def obtener_historial_ventas_detallado(conexion, fecha_str):
    """
    Obtiene el historial de ventas detallado para una fecha específica,
    uniendo las tablas de ventas y detalle_ventas.
    """
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT 
            v.id_transaccion,
            v.fecha_hora,
            d.nombre_producto,
            d.cantidad,
            d.precio_unitario,
            v.pago_efectivo,
            v.pago_transferencia,
            d.total_fila,
            v.estado,
            v.ticket_numero
        FROM ventas AS v
        JOIN detalle_ventas AS d ON v.id_transaccion = d.id_transaccion
        WHERE DATE(v.fecha_hora) = ?
        ORDER BY v.fecha_hora DESC
        """,
        (fecha_str,)
    )
    return cursor.fetchall()


def obtener_resumen_ventas_periodo(conexion, fecha_inicio, fecha_fin):
    """
    Calcula la facturación total, efectivo y transferencia de un período.
    """
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            SUM(pago_efectivo), 
            SUM(pago_transferencia),
            SUM(total_venta)
        FROM ventas
        WHERE estado = 'Completada' AND DATE(fecha_hora) BETWEEN ? AND ?
    """, (fecha_inicio, fecha_fin))
    
    resultados = cursor.fetchone()
    # Devolvemos un diccionario para un acceso más claro
    return {
        "efectivo": resultados[0] or 0.0,
        "transferencia": resultados[1] or 0.0,
        "total": resultados[2] or 0.0
    }

def obtener_top_productos_periodo(conexion, fecha_inicio, fecha_fin, limite=5):
    """
    Obtiene los productos más vendidos en un período, ordenados por cantidad.
    """
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            d.nombre_producto,
            SUM(d.cantidad) as total_cantidad
        FROM detalle_ventas as d
        JOIN ventas as v ON d.id_transaccion = v.id_transaccion
        WHERE v.estado = 'Completada' AND DATE(v.fecha_hora) BETWEEN ? AND ?
        GROUP BY d.nombre_producto
        ORDER BY total_cantidad DESC
        LIMIT ?
    """, (fecha_inicio, fecha_fin, limite))
    
    return cursor.fetchall()
# En app_multirrubro.py

def inicializar_base_de_datos():
    """
    Se conecta a la base de datos y se asegura de que todas las tablas necesarias
    existan. Si no existen, las crea.
    """
    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            
            # Crear tabla de productos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "productos" (
                "codigo_barras" TEXT UNIQUE, "nombre" TEXT NOT NULL,
                "precio" REAL NOT NULL, "stock" INTEGER NOT NULL,
                "umbral_alerta" INTEGER NOT NULL, PRIMARY KEY("codigo_barras")
            );
            """)

            # Crear tabla de ventas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "ventas" (
                "id_transaccion" TEXT, "fecha_hora" TEXT NOT NULL,
                "pago_efectivo" REAL, "pago_transferencia" REAL,
                "referencia" TEXT, "total_venta" REAL NOT NULL,
                "estado" TEXT DEFAULT 'Completada', "ticket_numero" INTEGER,
                PRIMARY KEY("id_transaccion")
            );
            """)

            # Crear tabla de detalle_ventas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "detalle_ventas" (
                "id_detalle" INTEGER, "id_transaccion" TEXT NOT NULL,
                "codigo_producto" TEXT, "nombre_producto" TEXT NOT NULL,
                "precio_unitario" REAL NOT NULL, "cantidad" INTEGER NOT NULL,
                "total_fila" REAL NOT NULL, PRIMARY KEY("id_detalle" AUTOINCREMENT),
                FOREIGN KEY("id_transaccion") REFERENCES "ventas"("id_transaccion") ON DELETE CASCADE
            );
            """)

            # Crear tabla de cortes_caja
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "cortes_caja" (
                "id" INTEGER, "fecha" TEXT UNIQUE, "fondo_inicial" REAL,
                "contado_final" REAL, "diferencia" REAL, "usuario" TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """)
            
            # Crear tabla de configuración
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "configuracion" (
                "clave" TEXT, "valor" TEXT, PRIMARY KEY("clave")
            );
            """)
            
            # Verificar si la configuración está vacía para llenarla con valores por defecto
            cursor.execute("SELECT COUNT(*) FROM configuracion")
            if cursor.fetchone()[0] == 0:
                config_default = {
                    'nombre_comercio': 'Tu Negocio', 'tema': 'superhero',
                    'mostrar_alertas_stock': 'true', 'umbral_alesta_stock': '5'
                }
                for clave, valor in config_default.items():
                    cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", (clave, valor))

            conexion.commit()
            print("Base de datos inicializada correctamente.")
            return True
            
    except sqlite3.Error as e:
        # Usamos messagebox aquí porque es un error crítico de inicio
        messagebox.showerror("Error Crítico de Base de Datos", f"No se pudo inicializar la base de datos: {e}")
        return False
