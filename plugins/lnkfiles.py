import LnkParse3
import os
import fnmatch
import json
from pathlib import Path
from plugins.main import *

# Global Variables
ROOT = str(get_project_root())

# Windows Lnk Files 
WINDOWS_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(os.environ['USERPROFILE'])
WINDOWS_TITLE = "Windows LNK Files"
WINDOWS_DESCRIPTION = "This module parses the lnk files on the target system. They are shortcut files that link \
						to an application or file commonly found on a user’s desktop, or throughout a system and \
						end with an .LNK extension."
WINDOWS_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_windows_lnk_files.json")

# MS Office Lnk Files 
OFFICE_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Office\\Recent'.format(os.environ['USERPROFILE'])
OFFICE_TITLE = "Microsoft Office LNK Files"
OFFICE_DESCRIPTION = "This module parses the MS Office lnk files on the target system. They are shortcut files that \
						link to an application or file commonly found on a user’s desktop, or throughout a system and \
						end with an .LNK extension."
OFFICE_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_ms_office_lnk_files.json")


class LnkFile:
	def __init__(self):
		self.local_base_path = None
		self.accessed_time = None
		self.creation_time = None
		self.modified_time = None
		self.drive_serial_no = None
		self.drive_type = None


def dump_to_json(file_path, data):
	""""
	Desc   :	Dumps the data extracted to json format.

	Params :	file_path - The path of the file to dump the json data to.
				data - The extracted data.
	"""
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def parse_lnk_files(path, data, lnk_file):
	""""
	Desc   :	Parses the lnk file.

	Params :	path - The path of the lnk file.
				data - A list to contain the data extracted from the lnk file.
				lnk_file - The lnk file itself.
	"""
	current_lnk_file = '{}\\{}'.format(path, lnk_file)
	with open(current_lnk_file, 'rb') as indata:
		lnk_file_obj = LnkFile()
		lnk_meta = LnkParse3.lnk_file(indata)
		json_format = lnk_meta.get_json()

		try:
			lnk_file_obj.local_base_path = json_format['link_info']['local_base_path']
		except KeyError:
			pass

		try:
			lnk_file_obj.accessed_time = convert_time(json_format['header']['accessed_time'])
		except (KeyError, AttributeError):
			pass

		try:
			lnk_file_obj.creation_time = convert_time(json_format['header']['creation_time'])
		except:
			pass

		try:
			lnk_file_obj.modified_time = convert_time(json_format['header']['modified_time'])
		except:
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


def get_lnk_file_data(lnk_files_path, title, description, outfile):
	""""
	Desc   :	Parses, extracts and dumps information extracted from lnk files.

	Params :	lnk_files_path - The directory containing lnk files.
				title - The title of the lnk file module.
				description - The description of the lnk file module.
				outfile - The directory of the file to dump data extracted from the lnk files.
	"""
	try:
		data = []
		WINDOWS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)
		lnk_files = os.listdir(lnk_files_path)
		lnk_files = fnmatch.filter(lnk_files, "*lnk")
		for lnk_file in lnk_files:
			parse_lnk_files(lnk_files_path, data, lnk_file)
		data = sorted(data, key=lambda k: k['accessed_time'], reverse=True)
		data.insert(0, description)
		data.insert(0, title)
		dump_to_json(outfile, data)
	except FileNotFoundError:
		pass


def run():
	""""
	Desc   :	Runs the lnk file module.

	Params :	None.
	"""
	get_lnk_file_data(WINDOWS_LNK_FILE_PATH, WINDOWS_TITLE, WINDOWS_DESCRIPTION, WINDOWS_OUTFILE)
	get_lnk_file_data(OFFICE_LNK_FILE_PATH, OFFICE_TITLE, OFFICE_DESCRIPTION, OFFICE_OUTFILE)
	

if __name__ == "__main__":
	run()
