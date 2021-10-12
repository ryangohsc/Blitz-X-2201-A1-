import os
import time
import json
from windowsprefetch import Prefetch
from pathlib import Path
from main import convert_time, dt_from_win32_ts, get_project_root

# Global Variables
ROOT = str(get_project_root())
TITLE = "Prefetch"
DESCRIPTION = "This module parses the prefetch files on the target system."
OUTFILE = Path(ROOT + "/data/prefetch/prefetch.json")
OUTFILE.parent.mkdir(exist_ok=True, parents=True)


def dump_to_json(file_path, data):
    """"
    Desc   :Dumps the data extracted to json format.

    Params :file_path - The path of the file to dump the json data to.
            data - The extracted data.
    """
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def parse_prefetch():
    """"
    Desc   :Dumps the data extracted to json format.

    Params :None.
    """
    data = []
    prefetch_directory = r"C:\Windows\Prefetch"
    prefetch_files = os.listdir(prefetch_directory)
    for pf_file in prefetch_files:
        if pf_file[-2:] == "pf":
            full_path = prefetch_directory + r"\\" + pf_file
            first_executed = os.path.getctime(full_path)
            first_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(first_executed))
            last_executed = os.path.getmtime(full_path)
            last_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_executed))
            pf = Prefetch(full_path)
            timestamps = []

            for timestamp in pf.timestamps:
                timestamps.append(timestamp)

            data.append({
                'app_name': pf.executableName,
                'run_count': pf.runCount,
                'last_executed': timestamps
            })
    return data


def run():
    """"
    Desc   :Runs the prefetch module.

    Params :None.
    """
    data = parse_prefetch()
    # data = sorted(data, key=lambda k: k['regkey_last_modified_date'], reverse=True)
    data.insert(0, DESCRIPTION)
    data.insert(0, TITLE)
    dump_to_json(OUTFILE, data)


if __name__ == "__main__":
    run()








# for pf_file in prefetch_files:
#     if pf_file[-2:] == "pf":
#         full_path = prefetch_directory + r"\\" + pf_file
#         first_executed = os.path.getctime(full_path)
#         first_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(first_executed))
#
#         last_executed = os.path.getmtime(full_path)
#         last_executed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_executed))
#
#         test = Prefetch(full_path)
#         print(test.executableName)
#         print(test.runCount)
#         if len(test.timestamps) > 1:
#             print("Last Executed:")
#             for timestamp in test.timestamps:
#                 print("    " + timestamp)
#         else:
#             print("Last Executed: {}".format(test.timestamps[0]))
#

