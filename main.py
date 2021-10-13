import argparse
import importlib
import time
import warnings
from dateutil import tz
from datetime import datetime, timedelta
from pathlib import Path
from encryption import *
from coloroma_colours import *

# Global variables
PLUGIN_PATH = "plugins"
LOADED_PLUGINS = []
POST_PROCESSING_PLUGINS = ["keyword_search.py", "report.py", "zehash.py"]
EXCLUDED_PLUGINS = []
warnings.filterwarnings("ignore")
WIN32_EPOCH = datetime(1601, 1, 1)


def init_argparser():
    """"
    Desc   :    Initialise the arg parser.

    Params :    None
    """
    parser = argparse.ArgumentParser(
        description="Write the description of the tool here",
        epilog="ICT2202 Assignment 1 Team Panzerwerfer"
    )
    requiredNamed = parser.add_argument_group("required arguments")
    parser.add_argument("-keydec", help="Imports a private key to decrypt the master hash file.")
    args = parser.parse_args()
    return args


def get_project_root():
    """"
    Desc   :    Returns the root directory of the application.

    Params :    None
    """
    return Path(__file__).parent


def dt_from_win32_ts(timestamp):
    """"
    Desc   :    Converts registry key timestamps to UTC.

    Params :    None
    """
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)


def convert_time(args_utc):
    """"
    Desc   :    Converts UTC to the timezone of the system and returns it.

    Params :    args_utc - The timestamp in UTC to be converted.
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    utc = args_utc.replace(tzinfo=from_zone)
    convert_utc = utc.astimezone(to_zone).strftime(fmt)
    return convert_utc


def return_excluded():
    """"
    Desc   :    Returns the excluded plugins.

    Params :    None.
    """
    return EXCLUDED_PLUGINS


def return_post():
    """"
    Desc   :    Returns the post-processing plugins.

    Params :    None.
    """
    return POST_PROCESSING_PLUGINS


def return_included():
    """"
    Desc   :    Returns the included plugins.

    Params :    None.
    """
    plugin_list = []
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = fnmatch.filter(plugins, "*py")
    for plugin in plugins:
        plugin_list.append(plugin)
    return plugin_list


def cls():
    """"
    Desc   :    Helper function to clear screen.

    Params :    None.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """"
    Desc   :    Prints a banner.

    Params :    None.
    """
    print(print_white(" ######                              #     #"))
    print(print_white(" #     # #      # ##### ######        #   # "))
    print(print_white(" #     # #      #   #       #          # #  "))
    print(print_white(" ######  #      #   #      #   #####    #   "))
    print(print_white(" #     # #      #   #     #            # #  "))
    print(print_white(" #     # #      #   #    #            #   # "))
    print(print_white(" ######  ###### #   #   ######       #     #"))


def load_plugins():
    """"
    Desc   :    Loads plugins the plugins from the "plugin" folder.

    Params :    None.
    """
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = fnmatch.filter(plugins, "*py")
    print(print_yellow("[*] Loading plugins...."))
    for plugin in plugins:
        if plugin in POST_PROCESSING_PLUGINS:
            plugins.remove(plugin)
    print(print_green(print_green("[!] Plugins successfully loaded!")))
    return plugin_path, plugins


def run_plugins(plugin_path, plugins):
    """"
    Desc   :    Runs plugins from the "plugin" folder.

    Params :    plugin_path - The path to the "plugins" folder.
                plugins - A list containing the names of the plugins from the "plugins" folder.
    """
    print(print_yellow("[*] Running plugins!"))
    no_of_plugins = len(plugins)
    for plugin in plugins:
        if plugin not in POST_PROCESSING_PLUGINS:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            print(print_yellow("\t[+] Running {}".format(plugin)))
            module.run()
    for plugin in POST_PROCESSING_PLUGINS:
        plugin_name = plugin[:-3]
        plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
        module = importlib.import_module(plugin_path)
        print(print_yellow("\t[+] Running {}".format(plugin)))
        module.run()


def main():
    """"
    Desc   :    Main function.

    Params :    None.
    """
    args = init_argparser()
    if args.keydec:
        decrypt_masterhash(args.keydec)

    else:
        start_time = time.time()
        print(print_white("-" * 50))
        print_banner()
        print(print_white("-" * 50))
        public_key_path = locate_public_key()
        cls()
        print(print_white("-" * 50))
        print_banner()
        print(print_white("-" * 50))
        plugin_path, plugins = load_plugins()
        run_plugins(plugin_path, plugins)
        encrypt_masterhash(public_key_path)
        print(print_green("\n[!] Total Time Elapsed: %s seconds" % (time.time() - start_time)))
    sys.exit(-1)


if __name__ == '__main__':
    main()
