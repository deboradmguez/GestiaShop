import sys, os, sqlite3
def conectar_db():
    
    if getattr(sys, 'frozen', False):
        ruta_appdata = os.environ.get('APPDATA', os.path.expanduser("~"))
        ruta_datos = os.path.join(ruta_appdata, "GestiaShop")
        os.makedirs(ruta_datos, exist_ok=True)
        ruta_db = os.path.join(ruta_datos, 'gestiaShop.db')
    else:
        ruta_db = 'gestiaShop.db'
    
    # El resto de la función de conexión es igual
    conn = sqlite3.connect(
        ruta_db,
        timeout=20,
        check_same_thread=False,
        isolation_level='IMMEDIATE'
    )
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn