#Computer\HKEY_CURRENT_USER\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags

# https://isc.sans.edu/forums/diary/Jump+List+Files+Are+OLE+Files/19911/
# https://olefile.readthedocs.io/en/latest/olefile.html#olefile.OleFileIO

import olefile
import LnkParse3
import os
from lnkfiles import Lnkfile

CURRENT_USER_PROFILE = os.environ['USERPROFILE']
JUMPLISTS_DIRECTORY = r"{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations".format(CURRENT_USER_PROFILE)


def write_to_json():
	pass


def parse_jumplist_json(json_data):
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

	line = "{}, {}, {}, {}, {}, {}\n".format(lnk_file_obj.local_base_path, \
												lnk_file_obj.accessed_time, \
												lnk_file_obj.creation_time, \
												lnk_file_obj.modified_time, \
												lnk_file_obj.drive_serial_no, \
												lnk_file_obj.drive_type)	
	print(line)

def parse_jumplist_file(directory):
	jumplists = os.listdir(directory)
	for jumplist in jumplists:
		jumplist_path = "{}\\{}".format(directory, jumplist)
		try:
			with olefile.OleFileIO(jumplist_path) as ole:
				for entry in ole.listdir():
					fin = ole.openstream(entry)
					lnk_meta = LnkParse3.lnk_file(fin)
					json_format = lnk_meta.get_json()       
					parse_jumplist_json(json_format)
		except:
			pass 

parse_jumplist_file(JUMPLISTS_DIRECTORY)




