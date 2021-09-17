import os
from winreg import *
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
import contextlib
import mmap
import xml.etree.ElementTree as ET
from auxillary import convert_time, dt_from_win32_ts


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
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor", 0)
    for i in range(QueryInfoKey(query)[0]):
        device_name = EnumKey(query, i)
        print(device_name)
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name, 0)
        for j in range(QueryInfoKey(query2)[0]):
            serial_no = EnumKey(query2, j)
            print("Serial: " + serial_no)
            query3 = OpenKey(HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name + "\\" + serial_no, 0)
            for x in range(QueryInfoKey(query3)[1]):
                hardware_id = EnumValue(query3, x)
                print(hardware_id[0] + ": " + str(hardware_id[1]))
            query4 = OpenKey(HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Enum\USBStor" + "\\" + device_name + "\\" + serial_no + "\Device Parameters\Partmgr",
                             0)
            for y in range(QueryInfoKey(query4)[1]):
                partmgr = EnumValue(query4, y)
                print(partmgr[0] + ": " + str(partmgr[1]))
        print("\n")


def get_mounted_devices():
    """
    SYSTEM/MountedDevices
    Compare mounted_devices_data with DosDevices.
    Take Volume{...} compare with get_user() to see if user plugged in the USB
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\MountedDevices", 0)
    for i in range(QueryInfoKey(query)[1]):
        mounted_devices = EnumValue(query, i)
        mounted_devices_data = mounted_devices[1].hex()
        print(mounted_devices[0] + ": " + mounted_devices_data)


def get_portable_devices():
    """
    HKLM Windows Portable Devices
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Portable Devices\Devices", 0)
    for i in range(QueryInfoKey(query)[0]):
        list_devices = EnumKey(query, i)
        print(list_devices)
        query2 = OpenKey(HKEY_LOCAL_MACHINE,
                         r"SOFTWARE\Microsoft\Windows Portable Devices\Devices" + "\\" + list_devices, 0)
        for y in range(QueryInfoKey(query2)[1]):
            friendly_name = EnumValue(query2, y)
            print(friendly_name[0] + ": " + str(friendly_name[1]))


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
    for i in range(QueryInfoKey(query)[0]):
        vid_pid = EnumKey(query, i)
        if not "vid" in vid_pid.lower() and not "pid" in vid_pid.lower():
            continue
        vid_pid_split = vid_pid.split("&")
        usb_vid = vid_pid_split[0]
        usb_pid = vid_pid_split[1]
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USB" + "\\" + vid_pid, 0)
        for i in range(QueryInfoKey(query2)[0]):
            serial_key = EnumKey(query2, i)
            usb_device = cmp_usb_sn(serial_key)
            if usb_device is None:
                continue
            timestamp = QueryInfoKey(query2)[2]
            timestamp = dt_from_win32_ts(timestamp)
            timestamp = convert_time(timestamp)
            print("VID: " + usb_vid + "\nPID: " + usb_pid + "\nLast Modified: " + timestamp + "\n")


# setupapi.dev.log
def get_first_time_setup():
    """
    Gets first time setup log in setupapi.dev.log
    """
    winpath = os.environ["WINDIR"] + "\\INF\\"
    log_file = open(winpath + "setupapi.dev.log", "r")
    print(log_file.read())
    log_file.close()


# User
def get_user():
    """
    Gets the current user inserted USB devices
    If the device GUID correlates to the keys in the user, it shows that the device is used by the current user
    """
    query = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2", 0)
    for i in range(QueryInfoKey(query)[0]):
        list_guid = EnumKey(query, i)
        print(list_guid)


# Volume Serial Number
def get_vol_sn():
    """
    Checks HKLM\EMDMgmt (External Memory Device Management)
    Not all devices have Windows Media Ready Boost enabled by default especially devices with SSDs.
    But still applicable to corporate devices nonetheless as of the time of writing.
    """
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
            print(usb_stor)
            print(
                "Volume Serial Number: " + vol_sn + "\nVolume Name: " + vol_name + "\nVSN: " + hex_vol_sn + "\nLast Modified: " + timestamp)
    except WindowsError:
        print("Unable to find the registry key. EMDMgmt is probably not enabled by default.")


# PnP Events
def usb_activities():
    """
    Accesses the System event file and gets the specified EventID
    """
    event_file = os.environ["WINDIR"] + "\\System32\\winevt\\logs\\System.evtx"
    with open(event_file, "r") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
            fh = FileHeader(buf, 0x0)
            for xml, record in evtx_file_xml_view(fh):
                root = ET.fromstring(xml)
                if root[0][1].text == "20003" or root[0][1].text == "20001":
                    print(root[0][7].get("SystemTime") + " EventID: " + root[0][1].text + " Computer: " + root[0][
                        12].text + " User SID: " + root[0][13].get("UserID") + " User: " + get_user_by_sid(
                        root[0][13].get("UserID")))
                    print("DriverFileName: " + root[1][0][1].text)
                    print("DeviceInstanceID: " + root[1][0][2].text)
                    print("AddServiceStatus: " + root[1][0][5].text + "\n")
                    # print(xml) #  This works too if want to print in XML format


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
