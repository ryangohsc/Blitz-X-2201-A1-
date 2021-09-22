from winreg import *
import wmi
from dateutil import tz
from datetime import datetime, timedelta
import json
from pathlib import Path


WIN32_EPOCH = datetime(1601, 1, 1)


def dt_from_win32_ts(timestamp):
    """
    Converts registry key timestamps to UTC
    """
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)


def convert_time(args_utc):
    """
    Converts UTC to the timezone of the system and returns it
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    utc = args_utc.replace(tzinfo=from_zone)
    convert_utc = utc.astimezone(to_zone).strftime(fmt)
    return convert_utc


def get_services():
    """
    Displays all services installed
    """
    c = wmi.WMI()
    my_list = []
    filename = Path("misc/services.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets currently installed services.")
    my_list.insert(0, "Services")
    for service in c.Win32_Service():
        my_list.append({
            "service": str(service.DisplayName),
        })
    json_obj = json.dumps(my_list, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_obj)


def get_windows_version():
    try:
        my_list = []
        filename = Path("misc/winver.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets the winver from HKLM CurrentVersion from registry.")
        my_list.insert(0, "Windows Version")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
        json_obj = json.dumps(my_list, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_obj)
    except PermissionError:
        print("Unable to get Windows Version as this function requires Admin Rights")


def get_system_env_var():
    try:
        my_list = []
        filename = Path("misc/system_env.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets system environment variables from current control set.")
        my_list.insert(0, "System Environment Variables")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
            json_obj = json.dumps(my_list, indent=4)
            with open(filename, "w") as outfile:
                outfile.write(json_obj)
    except PermissionError:
        print("Unable to get System Environment Variables as this function requires Admin Rights")


def get_start_up_apps():
    try:
        my_list = []
        filename = Path("misc/startup_apps.json")
        filename.parent.mkdir(exist_ok=True, parents=True)
        my_list.insert(0, "This module gets startup applications from HKLM Run.")
        my_list.insert(0, "Startup Apps")
        query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0)
        for i in range(QueryInfoKey(query)[1]):
            name = EnumValue(query, i)
            my_list.append({
                str(name[0]): str(name[1])
            })
            json_obj = json.dumps(my_list, indent=4)
            with open(filename, "w") as outfile:
                outfile.write(json_obj)
    except PermissionError:
        print("Unable to get Start Up Apps as this function requires Admin Rights")


def get_prev_ran_prog():
    try:
        query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache", 0)
        my_list = []
        filename = Path("misc/prev_ran_programs.json")
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
            json_obj = json.dumps(my_list, indent=4)
            with open(filename, "w") as outfile:
                outfile.write(json_obj)
    except PermissionError:
        print("Unable to get previously ran programs as this function requires Admin Rights")


def run():
    get_windows_version()
    get_services()
    get_system_env_var()
    get_start_up_apps()
    get_prev_ran_prog()


if __name__ == "__main__":
    run()
