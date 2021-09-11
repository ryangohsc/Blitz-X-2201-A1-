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


def get_windows_version():
    try:
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0)
        for i in range(QueryInfoKey(query)[1]):
            print(EnumValue(query, i))
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")


def get_system_env_var():
    try:
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0)
        for i in range(QueryInfoKey(query)[1]):
            print(EnumValue(query, i))
    except PermissionError:
        print("Unable to get System Environment Variables as this function requires Admin Rights")


def get_start_up_apps():
    try:
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0)
        for i in range(QueryInfoKey(query)[1]):
            print(EnumValue(query, i))
    except PermissionError:
        print("Unable to get Start Up Apps as this function requires Admin Rights")


def get_prev_ran_prog():
    try:
        query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache", 0)
        for i in range(QueryInfoKey(query)[1]):
            print(EnumValue(query, i))
    except PermissionError:
        print("Unable to get previously ran programs as this function requires Admin Rights")
