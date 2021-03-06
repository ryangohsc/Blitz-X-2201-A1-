import olefile
import LnkParse3
import json
from plugins.lnkfiles import LnkFile
from main import *


# Global Variables
ROOT = str(get_project_root())
CURRENT_USER_PROFILE = os.environ['USERPROFILE']
JUMPLISTS_DIRECTORY = r"{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations".format(CURRENT_USER_PROFILE)
TITLE = "Jumplist"
DESCRIPTION = "This module parses the automatic jumplist files on the target system. Jump Lists are created by  \
				software applications or Operating System so that the user can“jump”directly to recently opened  \
				files and folders."
OUTFILE = Path(ROOT + "/data/jumplist/file_activity_jumplist.json")
OUTFILE.parent.mkdir(exist_ok=True, parents=True)


def dump_to_json(file_path, data):
	""""
	Dumps the data extracted to json format.
	:param: file_path, data
	:return: None
	"""
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def parse_jumplist_json(json_data, data):
	""""
	Parses the jumplist file.
	:param: json_data, data
	:return: data
	"""
	lnk_file_obj = LnkFile()
	try:
		lnk_file_obj.local_base_path = json_data['link_info']['local_base_path']
	except KeyError:
		pass

	try:
		lnk_file_obj.accessed_time = convert_time(json_data['header']['accessed_time'])
	except (KeyError, AttributeError):
		pass

	try:
		lnk_file_obj.creation_time = convert_time(json_data['header']['creation_time'])
	except (KeyError, AttributeError):
		pass

	try:
		lnk_file_obj.modified_time = convert_time(json_data['header']['modified_time'])
	except (KeyError, AttributeError):
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
	""""
	Parses the jumplist file.
	:param: directory
	:return: data
	"""
	# Browse to the directory that contains jumplist files.
	data = []
	jumplists = os.listdir(directory)

	# Parse each individual jumplist and extract data from them.
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
	""""
	Runs the jumplist file module.
	:param: None
	:return: None
	"""
	data = parse_jumplist_file(JUMPLISTS_DIRECTORY)
	data = sorted(data, key=lambda k: k['accessed_time'], reverse=True)
	data.insert(0, DESCRIPTION)
	data.insert(0, TITLE)
	dump_to_json(OUTFILE, data)
