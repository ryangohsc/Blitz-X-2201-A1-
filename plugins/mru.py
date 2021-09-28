from winreg import *
from win32com.shell import shell
from plugins.misc import *
import json
import fnmatch
from pathlib import Path
from main import convert_time, dt_from_win32_ts, get_project_root


TITLE = "MRU"
ROOT = str(get_project_root())
DESCRIPTION = "This module parses the MRU on the target system."
OUTFILE = Path(ROOT + "/data/mru/file_activity_mru.json")


class Mru:
	def __init__(self):
		self.reg_last_modified = None
		self.reg_path = None


def dump_to_json(file_path, data):
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def get_recentdoc_subkeys():
	key = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU"
	sub_key_list = []
	key = OpenKey(HKEY_CURRENT_USER, key)
	try:
		sub_keys, values, time = QueryInfoKey(key)
		for i in range(sub_keys):
			subkey = EnumKey(key, i)
			sub_key_list.append(subkey)
	except WindowsError:
		pass
	return sub_key_list


def parse_mru(title, description):
	data = []
	key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU")
	sub_keys = get_recentdoc_subkeys()
	for item in sub_keys:
		item_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU\\{}".format(item)
		key = OpenKey(HKEY_CURRENT_USER, item_path)
		i = 0
		while i < 20:
			try:
				value = EnumValue(key, i)[1]
				pidl = shell.StringAsPIDL(value)
				path = shell.SHGetPathFromIDList(pidl)
				timestamp = QueryInfoKey(key)[2]
				timestamp = dt_from_win32_ts(timestamp)
				timestamp = convert_time(timestamp)
				mru = Mru(timestamp, value)
			except:
				pass
			data.append({
				'regkey_last_modified_date'	: timestamp,
				'path' 						: path
			})
			i += 1
	data = sorted(data, key=lambda k: k['regkey_last_modified_date'], reverse=True)
	data.insert(0, description)
	data.insert(0, title)
	return data


def run():
	data = parse_mru(TITLE, DESCRIPTION)
	OUTFILE.parent.mkdir(exist_ok=True, parents=True)
	dump_to_json(OUTFILE, data)


if __name__ == "__main__":
	run()
