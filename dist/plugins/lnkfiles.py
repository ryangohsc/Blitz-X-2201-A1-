import LnkParse3
import json
from main import *


# Global Variables
ROOT = str(get_project_root())

# Windows Lnk Files 
WINDOWS_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(os.environ['USERPROFILE'])
WINDOWS_TITLE = "Windows LNK Files"
WINDOWS_DESCRIPTION = "This module parses the lnk files on the target system. They are shortcut files that link \
						to an application or file commonly found on a user’s desktop, or throughout a system and \
						end with an .LNK extension."
WINDOWS_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_windows_lnk_files.json")
WINDOWS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

# MS Office Lnk Files 
OFFICE_LNK_FILE_PATH = r'{}\\AppData\\Roaming\\Microsoft\\Office\\Recent'.format(os.environ['USERPROFILE'])
OFFICE_TITLE = "Microsoft Office LNK Files"
OFFICE_DESCRIPTION = "This module parses the MS Office lnk files on the target system. They are shortcut files that \
						link to an application or file commonly found on a user’s desktop, or throughout a system and \
						end with an .LNK extension."
OFFICE_OUTFILE = Path(ROOT + "/data/lnk_files/file_activity_ms_office_lnk_files.json")
OFFICE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)


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
	Dumps the data extracted to json format.
	:param: file_path, data
	:return: None
	"""
	with open(file_path, "w") as outfile:
		json.dump(data, outfile, default=str, indent=4)


def parse_lnk_files(path, data, lnk_file):
	""""
	Parses the lnk file.
	:param: path, data, lnk_file
	:return: data
	"""
	# Parse the currently opened lnk file.
	current_lnk_file = '{}\\{}'.format(path, lnk_file)
	with open(current_lnk_file, 'rb') as indata:
		lnk_file_obj = LnkFile()
		lnk_meta = LnkParse3.lnk_file(indata)
		json_format = lnk_meta.get_json()

		# Get the local_base_path
		try:
			lnk_file_obj.local_base_path = json_format['link_info']['local_base_path']
		except KeyError:
			pass

		# Get the accessed_time
		try:
			lnk_file_obj.accessed_time = convert_time(json_format['header']['accessed_time'])
		except (KeyError, AttributeError):
			pass

		# Get the creation_time
		try:
			lnk_file_obj.creation_time = convert_time(json_format['header']['creation_time'])
		except (KeyError, AttributeError):
			pass

		# Get the modified_time
		try:
			lnk_file_obj.modified_time = convert_time(json_format['header']['modified_time'])
		except (KeyError, AttributeError):
			pass

		# Get the drove_serial_number
		try:
			lnk_file_obj.drive_serial_number = json_format['link_info']['location_info']['drive_serial_number']
		except (KeyError, AttributeError):
			pass

		# Get the drive_type
		try:
			lnk_file_obj.drive_type = json_format['link_info']['location_info']['drive_type']
		except KeyError:
			pass

		# Exclude the lnk file if a local_base_path or accessed_time attribute is missing.
		if lnk_file_obj.local_base_path is None or lnk_file_obj.accessed_time is None:
			pass

		# Store the data extracted.
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
	Parses, extracts and dumps information extracted from lnk files.
	:param: lnk_files_path, title, description, outfile
	:return: data
	"""
	try:
		data = []
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
	Runs the lnk file module.
	:param: None
	:return: None
	"""
	# Get the lnk files related to Windows activities
	get_lnk_file_data(WINDOWS_LNK_FILE_PATH, WINDOWS_TITLE, WINDOWS_DESCRIPTION, WINDOWS_OUTFILE)

	# Get the lnk files related to MS Office activities
	get_lnk_file_data(OFFICE_LNK_FILE_PATH, OFFICE_TITLE, OFFICE_DESCRIPTION, OFFICE_OUTFILE)
