from database.connection import conectar_db
import json


CONFIG_DEFAULT = {
    "nombre_comercio": "nombre del comercio",
    "tema": "superhero",
    "mostrar_alertas_stock": True,
    "umbral_alerta_stock": 5
}


def crear_tabla_configuracion():
    """Crear tabla de configuración si no existe"""
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT
            )
        """)
        
        # Insertar valores por defecto si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM configuracion")
        if cursor.fetchone()[0] == 0:
            for clave, valor in CONFIG_DEFAULT.items():
                cursor.execute(
                    "INSERT INTO configuracion (clave, valor) VALUES (?, ?)",
                    (clave, json.dumps(valor) if isinstance(valor, (list, dict)) else str(valor))
                )
        
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error al crear tabla de configuración: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def cargar_configuracion():
    """Cargar configuración desde la base de datos"""
    config = CONFIG_DEFAULT.copy()
    conexion = None
    
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT clave, valor FROM configuracion")
        
        for clave, valor in cursor.fetchall():
            try:
                # Intentar cargar como JSON para tipos complejos
                config[clave] = json.loads(valor)
            except (json.JSONDecodeError, TypeError):
                # Si falla, usar el valor directamente
                config[clave] = valor
        
        # Convertir tipos específicos
        if 'mostrar_alertas_stock' in config:
            config['mostrar_alertas_stock'] = str(config['mostrar_alertas_stock']).lower() in ('true', '1', 'yes')
        if 'umbral_alerta_stock' in config:
            config['umbral_alerta_stock'] = int(config['umbral_alerta_stock'])
        if 'decimales' in config:
            config['decimales'] = int(config['decimales'])
            
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
    finally:
        if conexion:
            conexion.close()
    
    return config

def guardar_configuracion(clave, valor):
    """Guardar un valor de configuración"""
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Convertir a string si es un tipo complejo
        if isinstance(valor, (list, dict, bool)):
            valor_guardar = json.dumps(valor)
        else:
            valor_guardar = str(valor)
        
        cursor.execute(
            "INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)",
            (clave, valor_guardar)
        )
        
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error al guardar configuración {clave}: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def guardar_configuracion_multiples(valores):
    """Guardar múltiples valores de configuración a la vez"""
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        for clave, valor in valores.items():
            if isinstance(valor, (list, dict, bool)):
                valor_guardar = json.dumps(valor)
            else:
                valor_guardar = str(valor)
            
            cursor.execute(
                "INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)",
                (clave, valor_guardar)
            )
        
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error al guardar configuración múltiple: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def restaurar_configuracion_default():
    """Restaurar configuración a valores por defecto"""
    return guardar_configuracion_multiples(CONFIG_DEFAULT)