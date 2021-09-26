import os
from winreg import *
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
import contextlib
import mmap
import xml.etree.ElementTree as ET
from main import convert_time, dt_from_win32_ts, get_project_root
import json
from pathlib import Path

ROOT = str(get_project_root())


def get_user_sid():
    """
    Returns a list user SIDs
    """
    users = []
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList", 0)
    for i in range(QueryInfoKey(query)[0]):
        key = EnumKey(query, i)
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + "\\" + key,
                         0)
        profile = QueryValueEx(query2, "ProfileImagePath")[0].split("\\")
        user = [key, profile[len(profile) - 1]]
        users.append(user)
    return users


def get_user_by_sid(sid):
    """
    Returns the username using the specified SID
    """
    users = get_user_sid()
    username = ""
    try:
        for i in range(len(users)):
            if users[i][0] == sid:
                username = users[i][1]
    except WindowsError:
        pass
    return username


# Drive Letter and Volume Name
def get_known_usb():
    """
    Produces known USB devices from HKLM USBStor
    """
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_known_usb.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKLM USBStor data from registry.")
    my_list.insert(0, "Drive Letter & Volume Name")
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor", 0)
    for i in range(QueryInfoKey(query)[0]):
        device_name = EnumKey(query, i)
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name, 0)
        for j in range(QueryInfoKey(query2)[0]):
            serial_no = EnumKey(query2, j)
            query3 = OpenKey(HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name + "\\" + serial_no, 0)
            for x in range(QueryInfoKey(query3)[1]):
                hardware_id = EnumValue(query3, x)
                if hardware_id[0] == "FriendlyName":
                    friendly_name = hardware_id[1]
                if hardware_id[0] == "HardwareID":
                    hwid = hardware_id[1]
            my_list.append({
                "name": str(device_name),
                "serial": str(serial_no),
                "friendly_name": friendly_name,
                "HWID": hwid
            })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


def get_mounted_devices():
    """
    SYSTEM/MountedDevices
    Compare mounted_devices_data with DosDevices.
    Take Volume{...} compare with get_user() to see if user plugged in the USB
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\MountedDevices", 0)
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_mounted_devices.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKLM MountedDevices data from registry.")
    my_list.insert(0, "Mounted Devices")
    for i in range(QueryInfoKey(query)[1]):
        mounted_devices = EnumValue(query, i)
        mounted_devices_data = mounted_devices[1].hex()
        my_list.append({
            "device_name": str(mounted_devices[0]),
            "registry_data": str(mounted_devices_data)
        })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


def get_portable_devices():
    """
    HKLM Windows Portable Devices
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Portable Devices\Devices", 0)
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_portable_devices.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKLM Windows Portable Devices data from registry.")
    my_list.insert(0, "Windows Portable Devices")
    for i in range(QueryInfoKey(query)[0]):
        list_devices = EnumKey(query, i)
        query2 = OpenKey(HKEY_LOCAL_MACHINE,
                         r"SOFTWARE\Microsoft\Windows Portable Devices\Devices" + "\\" + list_devices, 0)
        for y in range(QueryInfoKey(query2)[1]):
            friendly_name = EnumValue(query2, y)
        my_list.append({
            "device_name": str(list_devices),
            "friendly_name": str(friendly_name)
        })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


def cmp_usb_sn(arg_sn):
    """
    helper function do not include
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor", 0)
    for i in range(QueryInfoKey(query)[0]):
        device_name = EnumKey(query, i)
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name, 0)
        for j in range(QueryInfoKey(query2)[0]):
            serial_no = EnumKey(query2, j)
            serial_no = serial_no[:-2]
            if arg_sn == serial_no:
                return arg_sn
            else:
                continue


# Key Identification
def get_usb_identification():
    """
    HKLM USB
    Will cross check with USBSTOR serial no
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USB", 0)
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_identification.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKLM USB from the registry and compares with USBStor.")
    my_list.insert(0, "USB Identification")
    for i in range(QueryInfoKey(query)[0]):
        vid_pid = EnumKey(query, i)
        if not "vid" in vid_pid.lower() and not "pid" in vid_pid.lower():
            continue
        vid_pid_split = vid_pid.split("&")
        usb_vid = vid_pid_split[0]
        usb_pid = vid_pid_split[1]
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USB" + "\\" + vid_pid, 0)
        for x in range(QueryInfoKey(query2)[0]):
            serial_key = EnumKey(query2, x)
            usb_device = cmp_usb_sn(serial_key)
            if usb_device is None:
                continue
            timestamp = QueryInfoKey(query2)[2]
            timestamp = dt_from_win32_ts(timestamp)
            timestamp = convert_time(timestamp)
            my_list.append({
                "vid": str(usb_vid),
                "pid": str(usb_pid),
                "last modified": str(timestamp)
            })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


# setupapi.dev.log
def get_first_time_setup():
    """
    Gets first time setup log in setupapi.dev.log
    """
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_first_time_setup_interest.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets setupapi.dev.log from the system INF folder and filters it.")
    my_list.insert(0, "First Time Setup")
    winpath = os.environ["WINDIR"] + "\\INF\\"
    with open(winpath + "setupapi.dev.log", "r") as log_file:
        for line in log_file:
            if "_??_USBSTOR#Disk&" in line or "_##_USBSTOR#Disk&" in line:
                next_line = next(log_file)
                my_list.append({
                    "device install": str(line),
                    "device install time": str(next_line)
                })
                with open(filename, "w") as outfile:
                    json.dump(my_list, outfile, indent=4)


# User
def get_user():
    """
    Gets the current user inserted USB devices
    If the device GUID correlates to the keys in the user, it shows that the device is used by the current user
    """
    query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2", 0)
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_user.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKCU MountPoints from the registry of the current user.")
    my_list.insert(0, "MountPoints")
    for i in range(QueryInfoKey(query)[0]):
        list_guid = EnumKey(query, i)
        my_list.append({
            "Device GUID": str(list_guid)
        })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


# Volume Serial Number
def get_vol_sn():
    """
    Checks HKLM\EMDMgmt (External Memory Device Management)
    Not all devices have Windows Media Ready Boost enabled by default especially devices with SSDs.
    But still applicable to corporate devices nonetheless as of the time of writing.
    """
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_vol_sn_emdmgmt.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets HKLM EMDMgmt data from registry for volume serial number.")
    my_list.insert(0, "External Memory Device Management")
    try:
        query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt", 0)
        for i in range(QueryInfoKey(query)[0]):
            list_device = EnumKey(query, i)
            if not "_??_USBSTOR#Disk&" in list_device and not "_##_USBSTOR#Disk&" in list_device:
                continue
            if not "{53f56307-b6bf-11d0-94f2-00a0c91efb8b}" in list_device.lower():
                continue
            index = list_device.index("#{53f56307-b6bf-11d0-94f2-00a0c91efb8b}")
            usb_stor = list_device[0:index + 39]
            usb_stor = usb_stor.replace("_??_USBSTOR#", "")
            usb_stor = usb_stor.replace("_##_USBSTOR#", "")
            if len(usb_stor) == 0:
                continue
            drive_info = list_device[index + 39:]
            if "_" in drive_info:
                vol_sn = drive_info[drive_info.rfind("_") + 1:]
                vol_name = drive_info[0:drive_info.rfind("_")]
                if len(vol_sn) > 0:
                    vsn = int(vol_sn)
                    hex_vol_sn = "%x" % vsn
            query2 = OpenKey(HKEY_CURRENT_USER,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt" + "\\" + list_device, 0)
            timestamp = QueryInfoKey(query2)[2]
            timestamp = dt_from_win32_ts(timestamp)
            timestamp = convert_time(timestamp)
            my_list.append({
                "device name": str(usb_stor),
                "vol_sn": str(vol_sn),
                "volume name": str(vol_name),
                "vsn": str(hex_vol_sn),
                "last modified": str(timestamp)
            })
            with open(filename, "w") as outfile:
                json.dump(my_list, outfile, indent=4)
    except WindowsError:
        my_list.append({
            "not found": "Unable to find the registry key. EMDMgmt is probably not enabled by default"
        })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)


# PnP Events
def usb_activities():
    """
    Accesses the System event file and gets the specified EventID
    """
    my_list = []
    filename = Path(ROOT + "/data/usb/usb_sys_event.json")
    filename.parent.mkdir(exist_ok=True, parents=True)
    my_list.insert(0, "This module gets events from the system event.")
    my_list.insert(0, "System event log")
    try:
        # event_file = os.environ["WINDIR"] + "\\System32\\winevt\\Logs\\System.evtx"
        event_file = str(Path(os.environ["WINDIR"] + "/System32/winevt/Logs/System.evtx"))
        with open(event_file, "r") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                fh = FileHeader(buf, 0x0)
                for xml, record in evtx_file_xml_view(fh):
                    parser = ET.XMLParser(encoding="utf-8")
                    root = ET.fromstring(xml, parser=parser)
                    if root[0][1].text == "20003" or root[0][1].text == "20001":
                        my_list.append({
                            "eventid": root[0][1].text,
                            "computer": root[0][12].text,
                            "usersid": root[0][13].get("UserID"),
                            "user": get_user_by_sid(root[0][13].get("UserID")),
                            "driverfilename": root[1][0][1].text,
                            "deviceinstanceid": root[1][0][2].text,
                            "addservicestatus": root[1][0][5].text,
                            "timestamp": root[0][7].get("SystemTime")
                        })
                        with open(filename, "w") as outfile:
                            json.dump(my_list, outfile, indent=4)
    except FileNotFoundError:
        my_list.append({
            "not found": "Unable to find the registry key. EMDMgmt is probably not enabled by default"
        })
        with open(filename, "w") as outfile:
            json.dump(my_list, outfile, indent=4)
    except:
        pass


def run():
    get_known_usb()
    get_mounted_devices()
    get_portable_devices()
    get_usb_identification()
    get_first_time_setup()
    get_user()
    get_vol_sn()
    usb_activities()


if __name__ == "__main__":
    run()
