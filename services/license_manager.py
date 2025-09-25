import sys, uuid, hashlib
from datetime import datetime, timedelta
try:
    import winreg
except ImportError:
    pass

REG_PATH = r"Software\GestiaShop\Licencia"
TRIAL_DAYS = 8
SECRET_KEY = "minina_debo_4372"

def get_machine_uuid():
    """Obtiene un identificador único para la máquina."""
    return uuid.getnode()

def is_windows():
    return sys.platform == "win32"

def guardar_fecha_primer_uso():
    if not is_windows():
        return
        
    try:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        start_date = datetime.now().strftime("%Y-%m-%d")
        winreg.SetValueEx(reg_key, "StartDate", 0, winreg.REG_SZ, start_date)
        winreg.SetValueEx(reg_key, "IsLicensed", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error al acceder al registro: {e}")

def verificar_licencia():
    if not is_windows():
        return True, "Versión completa"

    try:
        # Intentar abrir la clave del registro
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        
        # Leer valores
        is_licensed, _ = winreg.QueryValueEx(reg_key, "IsLicensed")
        start_date_str, _ = winreg.QueryValueEx(reg_key, "StartDate")
        winreg.CloseKey(reg_key)
        
        if is_licensed == 1:
            return True, "Versión completa"

        # Si no está licenciado, verificar si el período de prueba ha expirado
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        dias_transcurridos = (datetime.now() - start_date).days
        
        if dias_transcurridos > TRIAL_DAYS:
            return False, "Período de prueba finalizado"
        else:
            dias_restantes = TRIAL_DAYS - dias_transcurridos
            return True, f"Versión de prueba - Días restantes: {dias_restantes}"

    except FileNotFoundError:
        # --- ESTA ES LA CORRECCIÓN ---
        # Si no existe la clave, es el primer uso. La creamos.
        guardar_fecha_primer_uso()
        # Y le informamos al usuario que la prueba ha comenzado.
        return True, f"Versión de prueba iniciada. Tienes {TRIAL_DAYS} días."
        # --- FIN DE LA CORRECCIÓN ---

    except Exception as e:
        print(f"Error al verificar la licencia: {e}")
        return False, f"Error al verificar la licencia: {e}"

def validar_codigo_activacion(codigo):
    try:
        # Genera el hash esperado
        maquina_id = str(get_machine_uuid()).encode()
        codigo_esperado = hashlib.sha256(maquina_id + SECRET_KEY.encode()).hexdigest()

        if codigo == codigo_esperado:
            # Si el código es válido, actualiza el registro para marcar como licenciado
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
            winreg.SetValueEx(reg_key, "IsLicensed", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(reg_key)
            return True, "Licencia activada con éxito."
        else:
            return False, "Código de activación incorrecto."
    except Exception as e:
        return False, f"Error en la validación: {e}"