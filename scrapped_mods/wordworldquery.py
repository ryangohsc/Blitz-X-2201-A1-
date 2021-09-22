from winreg import *

REG_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\WordWheelQuery"
NAME = 0
VALUE = 1


def get_subkeys(key_handle):
	sub_key_list = []
	try:
		sub_keys,values,time = QueryInfoKey(key_handle)
		for i in range(sub_keys):
			subkey = EnumKey(key_handle, i)
			sub_key_list.append(subkey)
	except WindowsError:
		pass
	return sub_key_list	


def write_to_json(data, mru_list_order):
	sorted_data = []
	for order_number in mru_list_order:
		for item in data:
			if item[NAME] == str(order_number):
				sorted_data.append(item)
	


def parse_mru_list(mru_value):
	mru_value = mru_value.hex().strip("f")
	x = 8
	mru_list_order = [int(mru_value[i: i + x][:2], 16) for i in range(0, len(mru_value), x)]
	return mru_list_order


def enum_wordwheel_regkey(reg_key):
	data = []
	mru_list_order = []
	key = OpenKey(HKEY_CURRENT_USER, reg_key)
	i = 0
	try:
		while True:
			value = EnumValue(key, i)
			if value[NAME] == "MRUListEx":
				mru_list_order = parse_mru_list(value[VALUE])
			else:
				data.append(value)
			i += 1
	except OSError:
		pass 
	return data, mru_list_order


def run():
	data, mru_list_order = enum_wordwheel_regkey(REG_KEY) 
	print(mru_list_order)
	print(data)


	# write_to_json(data, mru_list_order)


if __name__ == "__main__":
	run()