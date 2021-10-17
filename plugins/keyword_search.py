import os
import json
import re
from main import *

TITLE = 0
DESCRIPTION = 1
ROOT = str(get_project_root())
OUTFILE = Path(ROOT + "/data/keyword_search/keyword_search.json")


def dump_to_json(file_path, data):
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def recursive_search():
    pass


def run():
    choice = input("[+] Do you wish to run a keyword search? (y/n): ")

    if choice == "y":
        # Read keywords
        with open('keywords.txt', 'r') as f:
            keywords = f.read().splitlines()

        data_root_folder_path = "{}/data".format(get_project_root())
        data_sub_folders = os.listdir(data_root_folder_path)
        export_data = []

        # Read data files
        for sub_folder in data_sub_folders:
            data_sub_folders_path = "{}/{}".format(data_root_folder_path, sub_folder)
            data_files = os.listdir(data_sub_folders_path)

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
                                break
                if matches == 0:
                    export_data.append({
                        "not found": "Unable to find any results from the keyword search!"
                    })
        OUTFILE.parent.mkdir(exist_ok=True, parents=True)
        dump_to_json(OUTFILE, export_data)
    else:
        pass


if __name__ == "__main__":
    run()