import sys, uuid, hashlib
from datetime import datetime, timedelta
try:
    import winreg
except ImportError:
    pass

REG_PATH = r"Software\GestiaShop" 
TRIAL_DAYS = 8
SECRET_KEY = "minina_debo_4372"

class LicenciaLogic:
    def __init__(self, app_controller=None):
        self.app = app_controller

    def _is_windows(self):
        return sys.platform == "win32"

    def _get_machine_uuid(self):
        return str(uuid.getnode())

    def _guardar_fecha_primer_uso(self):
        if not self._is_windows():
            return
        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
            start_date = datetime.now().strftime("%Y-%m-%d")
            winreg.SetValueEx(reg_key, "StartDate", 0, winreg.REG_SZ, start_date)
            winreg.SetValueEx(reg_key, "IsLicensed", 0, winreg.REG_DWORD, 0) # 0 = No licenciado
            winreg.CloseKey(reg_key)
        except Exception as e:
            print(f"Error al guardar la fecha de primer uso en el registro: {e}")

    def verificar_licencia(self):
        if not self._is_windows():
            # Para sistemas no Windows, asumimos que está licenciado
            return True, "Versión Completa (No-Windows)"
        
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            is_licensed, _ = winreg.QueryValueEx(reg_key, "IsLicensed")
            start_date_str, _ = winreg.QueryValueEx(reg_key, "StartDate")
            winreg.CloseKey(reg_key)
            
            if is_licensed == 1:
                return True, "Versión Completa"

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            dias_transcurridos = (datetime.now() - start_date).days
            
            if dias_transcurridos > TRIAL_DAYS:
                return False, "Período de prueba finalizado."
            else:
                dias_restantes = TRIAL_DAYS - dias_transcurridos
                return True, f"Versión de prueba. Días restantes: {dias_restantes}"

        except FileNotFoundError:
            # Si la clave no existe, es el primer uso. La creamos.
            self._guardar_fecha_primer_uso()
            return True, f"Versión de prueba iniciada. Tienes {TRIAL_DAYS} días."
        except Exception as e:
            print(f"Error al verificar la licencia: {e}")
            return False, "Error al verificar la licencia."

    def validar_codigo_activacion(self, codigo_ingresado):
        if not self._is_windows():
            return False, "La activación solo está disponible en Windows."

        try:
            maquina_id = self._get_machine_uuid().encode()
            codigo_esperado = hashlib.sha256(maquina_id + SECRET_KEY.encode()).hexdigest()

            if codigo_ingresado.strip() == codigo_esperado:
                reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                winreg.SetValueEx(reg_key, "IsLicensed", 0, winreg.REG_DWORD, 1) # 1 = Licenciado
                winreg.CloseKey(reg_key)
                return True, "¡Licencia activada con éxito!"
            else:
                return False, "El código de activación es incorrecto."
        except Exception as e:
            return False, f"Error durante la validación: {e}"