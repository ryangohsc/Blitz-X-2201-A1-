from winreg import *
from win32com.shell import shell
from Registry import Registry
import LnkParse3
from auxillary import *

# Last visited MRU 

import codecs 



def get_recentdoc_subkeys():
	key = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU"
	sub_key_list =[]
	key = OpenKey(HKEY_CURRENT_USER, key)
	try:
		sub_keys,values,time = QueryInfoKey(key)
		for i in range(sub_keys):
			subkey = EnumKey(key, i)
			sub_key_list.append(subkey)
	except WindowsError:
		pass
	return sub_key_list




# Last visited MRU 

key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU")

# mru_list_ex = EnumValue(key, 0)[1].hex()
# mru_list_ex = mru_list_ex.strip("f")
# x = 8
# mru_list_order = [int(mru_list_ex[i: i + x][:2], 16) for i in range(0, len(mru_list_ex), x)]
# # print(mru_list_order)

sub_keys = get_recentdoc_subkeys()

key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU\\docx")
test = EnumValue(key, 6)[1]
pidl = shell.StringAsPIDL(test)
path = shell.SHGetPathFromIDList(pidl)


timestamp = QueryInfoKey(key)[2]
timestamp = dt_from_win32_ts(timestamp)
timestamp = convert_time(timestamp)


print(path)
print(timestamp)






# https://github.com/eopdyke/RecentDocs-MRU-Parser/blob/1797f504ee8af141d95581576a32cd0ab4772ae5/mru_parse.py#L82
# https://www.andreafortuna.org/2017/10/18/windows-registry-in-forensic-analysis/
# https://github.com/raptIRJuan/RecentDocsMRU/blob/master/recentdocs-mru.py
# def parse_MRUListEx(mrulist):
# 	size = (len(mrulist) - 4) / 4
# 	struct_arg = "%sI" % (size)
# 	return struct.unpack(struct_arg, mrulist.rstrip('\xff\xff\xff\xff'))


# query = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs", 0)
# sub_key_list =[]


# # The list of files recently opened directly from Windows Explorer are stored into
# key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs")

# mru_list_ex = EnumValue(key, 0)[1].hex()
# mru_list_ex = mru_list_ex.strip("f")
# x = 8
# mru_list_order = [int(mru_list_ex[i: i + x][:2], 16) for i in range(0, len(mru_list_ex), x)]
# print(mru_list_order)


# print(EnumValue(key, 2)[1].hex())




def get_recentdoc_subkeys():
	key = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs"
	sub_key_list =[]
	key = OpenKey(HKEY_CURRENT_USER, key)
	try:
		sub_keys,values,time = QueryInfoKey(key)
		for i in range(sub_keys):
			subkey = EnumKey(key, i)
			sub_key_list.append(subkey)
	except WindowsError:
		pass
	return sub_key_list


# # def get_sub_sub_keys():


# key_list = get_recentdoc_subkeys()
# for item in key_list:
# 	print(item)

