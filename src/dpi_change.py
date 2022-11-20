import win32api
import win32con


def set_dpi(dpi: int):
    try:
        real_value = 1 if dpi == 125 else 0
        key = "Control Panel\Desktop\PerMonitorSettings\AUS2722L5LMQS083030_14_07E4_8C^A133EEACD46DEB102F26E14D876CFD94"
        open_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, key, 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(open_key, "DpiValue", 0, win32con.REG_DWORD, real_value)
        win32api.RegCloseKey(open_key)
    except Exception as e:
        raise e
