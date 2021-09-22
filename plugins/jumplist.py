# Computer\HKEY_CURRENT_USER\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags
# py -m pip install dateutil
# https://isc.sans.edu/forums/diary/Jump+List+Files+Are+OLE+Files/19911/
# https://olefile.readthedocs.io/en/latest/olefile.html#olefile.OleFileIO

import olefile
import LnkParse3
import os
from plugins.lnkfiles import Lnkfile
import json
from pathlib import Path
from plugins.auxillary import get_project_root
from plugins.report import html_template

CURRENT_USER_PROFILE = os.environ['USERPROFILE']
JUMPLISTS_DIRECTORY = r"{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations".format(CURRENT_USER_PROFILE)
TITLE = "Jumplist"
DESCRIPTION = "This module parses the automatic jumplist files on the target system."
ROOT = str(get_project_root())
OUTFILE = Path(ROOT + "/data/jumplist/jumplist.json")
OUTREPORT = Path(ROOT + "/htmlreport/jumplist.html")


def dump_to_json(file_path, data):
	json_obj = json.dumps(data, indent=4, default=str)
	html_template(TITLE, OUTREPORT, json_obj)
	with open(file_path, 'w') as outfile:
		outfile.write(json_obj)


def parse_jumplist_json(json_data, data):
	lnk_file_obj = Lnkfile()
	try:
		lnk_file_obj.local_base_path = json_data['link_info']['local_base_path']
	except KeyError:
		pass

	try:
		lnk_file_obj.accessed_time = json_data['header']['accessed_time']
	except KeyError:
		pass

	try:
		lnk_file_obj.creation_time = json_data['header']['creation_time']
	except KeyError:
		pass

	try:
		lnk_file_obj.modified_time = json_data['header']['modified_time']
	except KeyError:
		pass

	try:
		lnk_file_obj.drive_serial_number = json_data['link_info']['location_info']['drive_serial_number']
	except KeyError:
		pass

	try:
		lnk_file_obj.drive_type = json_data['link_info']['location_info']['drive_type']
	except KeyError:
		pass

	if lnk_file_obj.local_base_path is None or lnk_file_obj.accessed_time is None:
		pass

	else:
		data.append({
			'base_path'			: lnk_file_obj.local_base_path,
			'accessed_time' 	: lnk_file_obj.accessed_time,
			'creation_time'		: lnk_file_obj.creation_time,
			'modified_time' 	: lnk_file_obj.modified_time,
			'drive_serial_no' 	: lnk_file_obj.drive_serial_no,
			'drive_type' 		: lnk_file_obj.drive_type
		})
	return data


def parse_jumplist_file(directory):
	data = []
	jumplists = os.listdir(directory)
	for jumplist in jumplists:
		jumplist_path = "{}\\{}".format(directory, jumplist)
		try:
			with olefile.OleFileIO(jumplist_path) as ole:
				for entry in ole.listdir():
					fin = ole.openstream(entry)
					lnk_meta = LnkParse3.lnk_file(fin)
					json_format = lnk_meta.get_json()       
					data = parse_jumplist_json(json_format, data)
		except:
			pass 
	return data


def run():
	data = parse_jumplist_file(JUMPLISTS_DIRECTORY)
	data = sorted(data, key=lambda k: k['accessed_time'], reverse=True)
	data.insert(0, DESCRIPTION)
	data.insert(0, TITLE)
	OUTFILE.parent.mkdir(exist_ok=True, parents=True)
	OUTREPORT.parent.mkdir(exist_ok=True, parents=True)
	dump_to_json(OUTFILE, data)	


if __name__ == "__main__":
	run()
