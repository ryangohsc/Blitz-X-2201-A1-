import argparse
import os
import fnmatch
import importlib
from dateutil import tz
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys

PLUGIN_PATH = "plugins"
EXCLUDED_PLUGINS = []
POST_PROCESSING_PLUGINS = ["report.py, zehash.py"]

# Argparser
parser = argparse.ArgumentParser(
    description="Write the description of the tool here",
    epilog="ICT2202 Assignment 1 Team Panzerwerfer"
)
requiredNamed = parser.add_argument_group("required arguments")
parser.add_argument("-o", help="")
args = parser.parse_args()


WIN32_EPOCH = datetime(1601, 1, 1)


def get_project_root():
    """
    Returns project root directory
    """
    return Path(__file__).parent


def dt_from_win32_ts(timestamp):
    """
    Converts registry key timestamps to UTC
    """
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)


def convert_time(args_utc):
    """
    Converts UTC to the timezone of the system and returns it
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    utc = args_utc.replace(tzinfo=from_zone)
    convert_utc = utc.astimezone(to_zone).strftime(fmt)
    return convert_utc


def return_excluded():
    """
    Returns the excluded plugins
    """
    return EXCLUDED_PLUGINS


def return_post():
    """
    Returns the post-processing plugins
    """
    return POST_PROCESSING_PLUGINS


def return_included():
    """
    Returns the included plugins
    """
    plugin_list = []
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = fnmatch.filter(plugins, "*py")
    for plugin in plugins:
        if plugin in EXCLUDED_PLUGINS:
            pass
        else:
            plugin_list.append(plugin)
    return plugin_list


def load_plugins():
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = return_included()
    print("[+] Loading plugins....")
    for plugin in plugins:
        print(plugin)
    print("\n[+] Plugins successfully loaded!")
    return plugin_path, plugins


def run_plugins(plugin_path, plugins):
    print("\n[+] Running plugins!")
    for plugin in plugins:
        if plugin in EXCLUDED_PLUGINS or plugin in POST_PROCESSING_PLUGINS:
            pass
        else:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            module.run()
        if plugin in POST_PROCESSING_PLUGINS:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            module.run()
    print("\n[!] Plugins successfully executed!")


def print_banner():
    """
    Prints a banner
    """
    print(" ######                              #     #")
    print(" #     # #      # ##### ######        #   # ")
    print(" #     # #      #   #       #          # #  ")
    print(" ######  #      #   #      #   #####    #   ")
    print(" #     # #      #   #     #            # #  ")
    print(" #     # #      #   #    #            #   # ")
    print(" ######  ###### #   #   ######       #     #")


def main():
    """
    Main function
    """
    start_time = time.time()
    print("-" * 50)
    print_banner()
    print("-" * 50)
    plugin_path, plugins = load_plugins()
    run_plugins(plugin_path, plugins)
    print("[!] Total Time Elapsed: %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
