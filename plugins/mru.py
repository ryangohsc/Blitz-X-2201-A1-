from win32com.shell import shell
from plugins.misc import *
import json
from pathlib import Path
from main import convert_time, dt_from_win32_ts, get_project_root

# Global Variables
ROOT = str(get_project_root())
TITLE = "Most Recently Used (MRU)"
DESCRIPTION = "This module parses the MRU on the target system. The MRU list is a Windows-based application that \
				includes registry of recently opened webpages, documents, files, images and other applications."
OUTFILE = Path(ROOT + "/data/mru/file_activity_mru.json")


def dump_to_json(file_path, data):
	""""
	Desc   :	Dumps the data extracted to json format.

	Params :	file_path - The path of the file to dump the json data to.
				data - The extracted data.
	"""
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def get_openSavePidlMRU():
	""""
	Desc   :	Gets the sub keys of the OpenSavePidlMRU key.

	Params :	None.
	"""
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


def parse_mru():
	""""
	Desc   :	Parses the MRU and extracts data from it.

	Params :	None.
	"""
	try:
		data = []
		sub_keys = get_openSavePidlMRU()
		OUTFILE.parent.mkdir(exist_ok=True, parents=True)
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
					data.append({
						'regkey_last_modified_date'	: timestamp,
						'path' 						: path
					})
				except:
					pass
				i += 1
		return data
	except FileNotFoundError:
		pass


def run():
	""""
	Desc   :	Runs the MRU module.

	Params :	None.
	"""
	data = parse_mru()
	data = sorted(data, key=lambda k: k['regkey_last_modified_date'], reverse=True)
	data.insert(0, DESCRIPTION)
	data.insert(0, TITLE)
	dump_to_json(OUTFILE, data)


if __name__ == "__main__":
	run()
