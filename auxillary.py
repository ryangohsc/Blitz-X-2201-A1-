from winreg import *
import wmi


def get_services():
    """
    Displays all services installed
    """
    c = wmi.WMI()
    services = []
    for service in c.Win32_Service():
        services.append(service.DisplayName)
    print(services)


def enum_key(hive, subkey: str):
    with OpenKey(hive, subkey, 0, KEY_ALL_ACCESS) as key:
        num_of_values = QueryInfoKey(key)[1]
        for i in range(num_of_values):
            values = EnumValue(key, i)
            if values[0] == "LangID": continue
            print(*values[:-1], sep="\t")  # todo: edit


def get_windows_version():
    try:
        with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as hklm_hive:
            enum_key(hklm_hive, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")


def get_system_env_var():
    try:
        with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as hklm_hive:
            enum_key(hklm_hive, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")


def get_start_up_apps():
    try:
        with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as hklm_hive:
            enum_key(hklm_hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")


def get_prev_ran_prog():
    try:
        with ConnectRegistry(None, HKEY_CURRENT_USER) as hkcu_hive:
            enum_key(hkcu_hive, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache")
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")
