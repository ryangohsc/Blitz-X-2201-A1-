import LnkParse3
import os 
import fnmatch

WINDOWS_RECENT_LNK_FILES = '{}\\AppData\\Roaming\\Microsoft\\Windows\\Recent'.format(os.environ['USERPROFILE'])
OFFICE_RECENT_LNK_FILES = '{}\\AppData\\Roaming\\Microsoft\\Office\\Recent'.format(os.environ['USERPROFILE'])

class Lnkfile:
	def __init__(self):
		self.local_base_path = ""
		self.accessed_time = ""
		self.creation_time = ""
		self.modified_time = ""
		self.drive_serial_no = ""
		self.drive_type = ""

	def set_local_base_path(self, data):
		self.local_base_path = data

	def set_accessed_time(self, data):
		self.accessed_time = data

	def set_creation_time(self, data):
		self.creation_time = data

	def set_modified_time(self, data):
		self.modified_time = data

	def set_drive_serial_no(self, data):
		self.drive_serial_no = data

	def set_drive_type(self, data):
		self.drive_type = data

	def get_local_base_path(self):
		return self.local_base_path

	def get_accessed_time(self):
		return self.accessed_time

	def get_creation_time(self):
		return self.creation_time

	def get_modified_time(self):
		return self.modified_time

	def get_drive_serial_no(self):
		return self.drive_serial_no

	def get_drive_type(self):
		return self.drive_type


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
				lnk_file_obj.set_local_base_path(json_format['link_info']['local_base_path'])
			except KeyError:
				pass

			try:
				lnk_file_obj.set_accessed_time(json_format['header']['accessed_time'])
			except KeyError:
				pass

			try:
				lnk_file_obj.set_creation_time(json_format['header']['creation_time'])
			except KeyError:
				pass

			try:
				lnk_file_obj.set_modified_time(json_format['header']['modified_time'])
			except KeyError:
				pass

			try:
				lnk_file_obj.set_drive_serial_no(json_format['link_info']['location_info']['drive_serial_number'])
			except KeyError:
				pass 

			try:
				lnk_file_obj.set_drive_type(json_format['link_info']['location_info']['drive_type'])
			except KeyError:
				pass

			line = "{}, {}, {}, {}, {}, {}\n".format(lnk_file_obj.get_local_base_path(), 
														lnk_file_obj.get_accessed_time(), 
														lnk_file_obj.get_creation_time(), 
														lnk_file_obj.get_modified_time(), 
														lnk_file_obj.get_drive_serial_no(), 
														lnk_file_obj.get_drive_type())
			file.write(line)


def run():
	parse_lnk_files(WINDOWS_RECENT_LNK_FILES, 'lnkfile_microsoft.txt')
	parse_lnk_files(OFFICE_RECENT_LNK_FILES, 'lnkfile_office.txt')


if __name__ == "__main__":
	run()