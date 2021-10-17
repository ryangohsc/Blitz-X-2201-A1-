from winreg import *
import wmi
import json
from pathlib import Path
from plugins.main import *

ROOT = str(get_project_root())


def get_services():
    """"
    Displays all services installed.
    :param: None
    :return: None
    """
    c = wmi.WMI()
    my_list = []
    filename = Path(ROOT + "/data/misc/misc_services.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets currently installed services.")
    my_list.insert(0, "Windows Services")
    try:
        for service in c.Win32_Service():
            my_list.append({
                "service": str(service.DisplayName),
            })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)
    except:
        pass


def get_windows_version():
    """"
    Gets the Windows Version of the installation.
    :param: None
    :return: None
    """
    try:
        my_list = []
        filename = Path(ROOT + "/data/misc/misc_winver.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets the winver from HKLM CurrentVersion from registry.")
        my_list.insert(0, "Windows Version")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)
    except:
        pass


def get_system_env_var():
    """"
    Gets the system environment variables.
    :param: None
    :return: None
    """
    try:
        my_list = []
        filename = Path(ROOT + "/data/misc/misc_system_env.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets system environment variables from current control set.")
        my_list.insert(0, "System Environment Variables")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
            with open(filename, "w") as outfile:
                json.dump(my_list, outfile, indent=4)
    except:
        pass


def get_start_up_apps():
    """"
    Get start up applications from the registry.
    :param: None
    :return: None
    """
    try:
        my_list = []
        filename = Path(ROOT + "/data/misc/misc_startup_apps.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets startup applications from HKLM Run.")
        my_list.insert(0, "Startup Apps")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
            with open(filename, "w") as outfile:
                json.dump(my_list, outfile, indent=4)
    except:
        pass


def get_prev_ran_prog():
    """"
    Gets previously ran programs from the registry.
    :param: None
    :return: None
    """
    try:
        query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache", 0)
        my_list = []
        filename = Path(ROOT + "/data/misc/misc_prev_ran_programs.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets previously ran programs from HKCU MuiCache.")
        my_list.insert(0, "Previously Ran Programs")
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            if name[0] == "LangID":
                continue
            my_list.append({
                str(name[0]): str(name[1])
            })
            with open(filename, "w") as outfile:
                json.dump(my_list, outfile, indent=4)
    except:
        pass


def run():
    """"
    Runs the misc module.
    :param: None
    :return: None
    """
    get_windows_version()
    get_services()
    get_system_env_var()
    get_start_up_apps()
    get_prev_ran_prog()


if __name__ == "__main__":
    run()
