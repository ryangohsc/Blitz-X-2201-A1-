from winreg import *
import json
from pathlib import Path
from plugins.main import *

# Global Variables
ROOT = str(get_project_root())

# Run Once 
RUN_ONCE_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
RUN_ONCE_TITLE = "RunOnce Registry Data"
RUN_ONCE_DESCRIPTION = "This module parses the run once regkey on the target system. Run once registry keys cause  \
                       programs to run each time a user logs on. "
RUN_ONCE_OUTFILE = Path(ROOT + "/data/reg_activity/file_activity_run_once.json")

# Run 
RUN_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
RUN_TITLE = "Run Registry Data"
RUN_DESCRIPTION = "This module parses the run regkey on the target system. Run registry keys cause programs  \
                  to run each time a user logs on. "
RUN_OUTFILE = Path(ROOT + "/data/reg_activity/file_activity_run.json")

# Typed Paths
TYPED_PATH_KEY = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths"
TYPED_PATH_TITLE = "Typed Paths Data"
TYPED_PATH_DESCRIPTION = "This module parses the Typed Paths Reg key on the target system. The last 25  \
                         directories typed into the file explorer path bar are recorded by this reg key."
TYPED_PATH_OUTFILE = Path(ROOT + "/data/reg_activity/file_activity_typed_paths.json")


def dump_to_json(file_path, data):
    """"
    Desc   :    Dumps the data extracted to json format.

    Params :    file_path - The path of the file to dump the json data to.
                data - The extracted data.
    """
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def get_reg_key_data(reg_key, title, description, outfile):
    """"
    Desc   :    Gets the data from the registry key.

    Params :    reg_key - The registry key.
                title - The title of the reg_user_activity_module.
                description - The description of the reg_user_activity_module.
                outfile - The outfile where the data will be exported to.
    """
    data = []
    RUN_ONCE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)
    key = OpenKey(HKEY_CURRENT_USER, reg_key)
    i = 0
    try:
        while True:
            value = EnumValue(key, i)
            data.append({
                str(value[0]): str(value[1])
            })
            i += 1
    except OSError:
        pass
    data.insert(0, description)
    data.insert(0, title)
    dump_to_json(outfile, data)


def run():
    """"
    Desc   :    Runs the reg_user_activity module.

    Params :    None.
    """
    get_reg_key_data(RUN_ONCE_KEY, RUN_ONCE_TITLE, RUN_ONCE_DESCRIPTION, RUN_ONCE_OUTFILE)
    get_reg_key_data(RUN_KEY, RUN_TITLE, RUN_DESCRIPTION, RUN_OUTFILE)
    get_reg_key_data(TYPED_PATH_KEY, TYPED_PATH_TITLE, TYPED_PATH_DESCRIPTION, TYPED_PATH_OUTFILE)


if __name__ == "__main__":
    run()
