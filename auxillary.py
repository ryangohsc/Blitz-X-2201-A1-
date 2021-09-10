from winreg import *
import wmi


def getServices():
    """
    Displays all services installed
    """
    c = wmi.WMI()
    for service in c.Win32_Service():
        print(service.DisplayName)
