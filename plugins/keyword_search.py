import json
import re
from main import *


# Global Variables
TITLE = 0
DESCRIPTION = 1
ROOT = str(get_project_root())
OUTFILE = Path(ROOT + "/data/keyword_search/keyword_search.json")
OUTFILE.parent.mkdir(exist_ok=True, parents=True)


def dump_to_json(file_path, data):
    """"
    Dumps the data extracted to json format.
    :param: file_path, data
    :return: None
    """
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def recursive_search(keyword_list):
    """"
    Runs a recursive search into the "data" folder to extract data that contains the keywords.
    :param: None
    :return: export_data
    """
    # Read keywords
    try:
        with open(keyword_list, 'r') as f:
            keywords = f.read().splitlines()
    except FileNotFoundError:
        print(print_red("\t[!] Unable to find keyword file! Skipping keyword search!"))
        return

    data_root_folder_path = "{}/data".format(get_project_root())
    data_sub_folders = os.listdir(data_root_folder_path)
    export_data = []

    # Read data files.
    for sub_folder in data_sub_folders:
        data_sub_folders_path = "{}/{}".format(data_root_folder_path, sub_folder)
        data_files = os.listdir(data_sub_folders_path)

        # Parse each data file to look out for data that matches the keywords.
        for data_file in data_files:
            data_file_path = "{}/{}".format(data_sub_folders_path, data_file)
            with open(data_file_path, 'r') as file:
                matches = 0
                loaded_data = json.load(file)
                export_data.append(loaded_data[0])
                export_data.append(loaded_data[1])
                loaded_data.pop(0)
                loaded_data.pop(0)
                for entry in loaded_data:
                    result = ' '.join(filter(None, list(map(str, entry.values()))))
                    for keyword in keywords:
                        if re.search(keyword, result):
                            matches += 1
                            export_data.append(entry)
            if matches == 0:
                export_data.append({
                    "not found": "Unable to find any results from the keyword search!"
                })
    return export_data


def run(keyword_list):
    """"
    Runs the keyword_search module.
    :param: None
    :return: None
    """
    if keyword_list is not None:
        export_data = recursive_search(keyword_list)
        dump_to_json(OUTFILE, export_data)
        print(print_green("\t[!] Keyword search successfully ran!"))
    else:
        print(print_red("\t[!] No wordlist provided! Skipping keyword search!"))
