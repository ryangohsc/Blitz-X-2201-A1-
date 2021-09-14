import LnkParse3
import os 
import fnmatch

WINDOWS_RECENT_LNK_FILES = '{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(os.environ['USERPROFILE'])
OFFICE_RECENT_LNK_FILES = '{}\\AppData\\Roaming\\Microsoft\\Office\\Recent'.format(os.environ['USERPROFILE'])

class Lnkfile:
	def __init__(self):
		self.local_base_path = None
		self.accessed_time = None
		self.creation_time = None
		self.modified_time = None
		self.drive_serial_no = None
		self.drive_type = None


def parse_lnk_files(path, filename):
	lnk_files = os.listdir(path)
	lnk_files = fnmatch.filter(lnk_files, "*lnk")

	file = open(filename,"w")
	for lnk_file in lnk_files:
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

			line = "{}, {}, {}, {}, {}, {}\n".format(lnk_file_obj.local_base_path, \
														lnk_file_obj.accessed_time, \
														lnk_file_obj.creation_time, \
														lnk_file_obj.modified_time, \
														lnk_file_obj.drive_serial_no, \
														lnk_file_obj.drive_type)
			file.write(line)


def run():
	parse_lnk_files(WINDOWS_RECENT_LNK_FILES, 'lnkfile_microsoft.txt')
	parse_lnk_files(OFFICE_RECENT_LNK_FILES, 'lnkfile_office.txt')


if __name__ == "__main__":
	run()