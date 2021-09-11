import sys
import os.path
from winreg import *
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view


# Drive Letter and Volume Name
def known_usb():
    """
    Produces known USB devices from HKLM USBStor
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\USBStor', 0)
    for i in range(QueryInfoKey(query)[0]):
        device_name = EnumKey(query, i)
        print(device_name)
        query2 = OpenKey(HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\USBStor' + "\\" + device_name, 0)
        for j in range(QueryInfoKey(query2)[0]):
            serial_no = EnumKey(query2, j)
            print("Serial: " + serial_no)
            query3 = OpenKey(HKEY_LOCAL_MACHINE,
                             r'SYSTEM\CurrentControlSet\Enum\USBStor' + "\\" + device_name + "\\" + serial_no, 0)
            for x in range(QueryInfoKey(query3)[1]):
                hardware_id = EnumValue(query3, x)
                print(hardware_id[0] + ": " + str(hardware_id[1]))
            query4 = OpenKey(HKEY_LOCAL_MACHINE,
                             r'SYSTEM\CurrentControlSet\Enum\USBStor' + "\\" + device_name + "\\" + serial_no + "\Device Parameters\Partmgr",
                             0)
            for y in range(QueryInfoKey(query4)[1]):
                partmgr = EnumValue(query4, y)
                print(partmgr[0] + ": " + str(partmgr[1]))
        print("\n")


def get_mounted_devices():
    """
    SYSTEM/MountedDevices
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r'SYSTEM\MountedDevices', 0)
    for i in range(QueryInfoKey(query)[1]):
        mounted_devices = EnumValue(query, i)
        print(mounted_devices[0] + ": " + str(mounted_devices[1]))


def get_portable_devices():
    """
    HKLM Windows Portable Devices
    """
    query = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows Portable Devices\Devices', 0)
    for i in range(QueryInfoKey(query)[0]):
        list_devices = EnumKey(query, i)
        print(list_devices)
        query2 = OpenKey(HKEY_LOCAL_MACHINE,
                         r'SOFTWARE\Microsoft\Windows Portable Devices\Devices' + "\\" + list_devices, 0)
        for y in range(QueryInfoKey(query2)[1]):
            friendly_name = EnumValue(query2, y)
            print(friendly_name[0] + ": " + str(friendly_name[1]))


# First/Last Times
def get_first_last_times():
    pass


# User
def get_user():
    pass


# Volume Serial Number
def get_vol_sn():
    pass


# Key Identification
def get_usb_identification():
    pass


# PnP Events
def usb_activities():
    pass
