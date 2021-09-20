from winreg import *
import json

# Run Once 
RUN_ONCE_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
RUN_ONCE_TITLE =  "RunOnce Registry Data"
RUN_ONCE_DESCRIPTION = "This module parses the run once regkey on the target system."
RUN_ONCE_OUTFILE = "run_once.json"

# Run 
RUN_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
RUN_TITLE =  "Run Registry Data"
RUN_DESCRIPTION = "This module parses the run regkey on the target system."
RUN_OUTFILE = "run.json"

# Typed Paths
TYPED_PATH_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths"
TYPED_PATH_TITLE = "Typed Paths Data"
TYPED_PATH_DESCRIPTION = "This module parses the Typed Paths Reg key on the target system."
TYPED_PATH_OUTFILE = "typed_paths.json"


def dump_to_json(file_path, data):
	with open(file_path, 'w') as outfile:
		json.dump(data, outfile, default=str) 


def get_reg_key_data(reg_key, title, description, outfile):
	data = [] 
	key = OpenKey(HKEY_CURRENT_USER, reg_key)
	i = 0
	try:
		while True:
			value = EnumValue(key, i)
			data.append(value)
			i += 1
	except OSError:
		pass 
	data.insert(0, description)
	data.insert(0, title)	
	dump_to_json(outfile, data)


def run():
	get_reg_key_data(RUN_ONCE_KEY, RUN_ONCE_TITLE, RUN_ONCE_DESCRIPTION, RUN_ONCE_OUTFILE)
	get_reg_key_data(RUN_KEY, RUN_TITLE, RUN_DESCRIPTION, RUN_OUTFILE)
	get_reg_key_data(TYPED_PATH_KEY, TYPED_PATH_TITLE, TYPED_PATH_DESCRIPTION, TYPED_PATH_OUTFILE)


if __name__ == "__main__":
	run()