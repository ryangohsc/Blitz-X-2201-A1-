# https://mattcasmith.net/2018/11/23/python-forensics-tools-windows-prefetch/
import time 
import os 
import json

PREFETCH_DIRECTORY = r"C:\\Windows\\Prefetch"
PREFETCH_TITLE = "Prefetch Files"
PREFETCH_DESCRIPTION = "This module parses the prefetch files on the target system."
PREFETCH_OUTFILE = "prefetch.json"

# RECENT_DIRECTORY = r"{}\Recent".format(os.environ['USERPROFILE'])
# RECENT_TITLE = "Recent Files"
# RECENT_DESCRIPTION = "This module parses the recent files on the target system."
# RECENT_OUTFILE = "recent.json"


class FileMetaData:
	def __init__(self):
		self.path = None
		self.first_executed = None
		self.last_executed = None 


def dump_to_json(file_path, data):
	with open(file_path, 'w') as outfile:
		json.dump(data, outfile, default=str) 


def get_file_metadata(directory):
	data = []
	files = os.listdir(directory) 
	for file in files:
		file_obj = FileMetaData()
		file_obj.path = r"{}\{}".format(directory, file)
		file_obj.first_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_obj.path)))
		file_obj.last_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_obj.path)))
		data.append({
			'path'			: file_obj.path, 
			'first_executed': file_obj.first_executed,
			'last_executed' : file_obj.last_executed
			})
	return data


def get_prefetch_data():
	data = get_file_metadata(PREFETCH_DIRECTORY) 
	data = sorted(data, key=lambda k: k['last_executed'], reverse=True)
	data.insert(0, PREFETCH_DESCRIPTION)
	data.insert(0, PREFETCH_TITLE)
	dump_to_json(PREFETCH_OUTFILE, data)	


def run():
	get_prefetch_data()
	get_recentfile_data()


if __name__ == "__main__":
	run()