import json
from windowsprefetch import Prefetch
from main import *


# Global Variables
ROOT = str(get_project_root())
TITLE = "Prefetch"
DESCRIPTION = "This module parses the prefetch files on the target system. Windows creates a prefetch file  \
              when an application is run from a particular location for the very first time.  \
              This is used to help speed up the loading of applications. "
OUTFILE = Path(ROOT + "/data/prefetch/file_activity_prefetch.json")
OUTFILE.parent.mkdir(exist_ok=True, parents=True)


def dump_to_json(file_path, data):
    """"
    Dumps the data extracted to json format.
    :param: file_path, data
    :return: None
    """
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def parse_prefetch():
    """"
    Parses each prefetch file in the specified directory and extract information from them.
    :param: None
    :return: data
    """
    data = []
    prefetch_directory = r"C:\Windows\Prefetch"
    prefetch_files = os.listdir(prefetch_directory)
    for pf_file in prefetch_files:
        try:
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
        except AttributeError:
            pass
    return data


def run():
    """"
    Runs the prefetch module.
    :param: None
    :return: None
    """
    data = parse_prefetch()
    data.insert(0, DESCRIPTION)
    data.insert(0, TITLE)
    dump_to_json(OUTFILE, data)
