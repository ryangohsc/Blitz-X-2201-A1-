import LnkParse3
import os 
import fnmatch
import json
from pathlib import Path
from plugins.auxillary import get_project_root

ROOT = str(get_project_root())

# Windows Lnk Files 
WINDOWS_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(os.environ['USERPROFILE'])
WINDOWS_TITLE = "Windows LNK Files"
WINDOWS_DESCRIPTION = "This module parses the lnk files on the target system."
WINDOWS_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_windows_lnk_files.json")

# MS Office Lnk Files 
OFFICE_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Office\\Recent'.format(os.environ['USERPROFILE'])
OFFICE_TITLE = "Microsoft Office LNK Files"
OFFICE_DESCRIPTION = "This module parses the office lnk files on the target system."
OFFICE_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_ms_office_lnk_files.json")


class Lnkfile:
	def __init__(self):
		self.local_base_path = None
		self.accessed_time = None
		self.creation_time = None
		self.modified_time = None
		self.drive_serial_no = None
		self.drive_type = None


def dump_to_json(file_path, data):
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def parse_lnk_files(path, data, lnk_file):
	current_lnk_file = '{}\\{}'.format(path, lnk_file)
	with open(current_lnk_file, 'rb') as indata:
		lnk_file_obj = Lnkfile()
		lnk_meta = LnkParse3.lnk_file(indata)
		json_format = lnk_meta.get_json()

		try:
			lnk_file_obj.local_base_path = json_format['link_info']['local_base_path']
		except KeyError:
			pass

		try:
			lnk_file_obj.accessed_time = json_format['header']['accessed_time']
		except KeyError:
			pass

		try:
			lnk_file_obj.creation_time = json_format['header']['creation_time']
		except KeyError:
			pass

		try:
			lnk_file_obj.modified_time = json_format['header']['modified_time']
		except KeyError:
			pass

		try:
			lnk_file_obj.drive_serial_number = json_format['link_info']['location_info']['drive_serial_number']
		except KeyError:
			pass 

		try:
			lnk_file_obj.drive_type = json_format['link_info']['location_info']['drive_type']
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


def get_lnk_file_data(lnk_file_path, title, description, outfile):
	data = []
	lnk_files = os.listdir(lnk_file_path)
	lnk_files = fnmatch.filter(lnk_files, "*lnk")	
	for lnk_file in lnk_files:
		parse_lnk_files(lnk_file_path, data, lnk_file)
	data = sorted(data, key=lambda k: k['accessed_time'], reverse=True)
	data.insert(0, description)
	data.insert(0, title)
	dump_to_json(outfile, data)


def run():
	WINDOWS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)
	OFFICE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)
	get_lnk_file_data(WINDOWS_LNK_FILE_PATH, WINDOWS_TITLE, WINDOWS_DESCRIPTION, WINDOWS_OUTFILE)
	get_lnk_file_data(OFFICE_LNK_FILE_PATH, OFFICE_TITLE, OFFICE_DESCRIPTION, OFFICE_OUTFILE)
	

if __name__ == "__main__":
	run()
