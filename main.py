import warnings
import argparse
import importlib
import time
import fnmatch
import sys
from dateutil import tz
from datetime import datetime, timedelta
from plugins.encryption import *
from plugins.zehash import *
from colorama import init, Fore, Style


# Global variables
PLUGIN_PATH = "plugins"
LOADED_PLUGINS = []
POST_PROCESSING_PLUGINS = ["keyword_search.py", "report.py", "zehash.py"]
EXCLUDED_PLUGINS = ["encryption.py"]
warnings.filterwarnings("ignore")
WIN32_EPOCH = datetime(1601, 1, 1)
HASHPATH = Path(os.getcwd() + "/master_hash.txt")
HASH_RECAL = Path(os.getcwd() + "/master_hash_recal.txt")


def print_green(text):
    """"
    Prints a sentence in the color green.
    :param: text
    :return: Fore.GREEN + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE
    """
    return Fore.GREEN + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE


def print_red(text):
    """"
    Prints a sentence in the color red.
    :param: text
    :return: Fore.RED + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE
    """
    return Fore.RED + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE


def get_project_root():
    """"
    Returns the root directory of the application.
    :param: None
    :return: os.getcwd()
    """
    return os.getcwd()


def dt_from_win32_ts(timestamp):
    """"
    Converts registry key timestamps to UTC.
    :param: timestamp
    :return: WIN32_EPOCH + timedelta(microseconds=timestamp // 10)
    """
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)


def convert_time(args_utc):
    """"
    Converts UTC to the timezone of the system and returns it.
    :param: args_utc
    :return: convert_utc
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    utc = args_utc.replace(tzinfo=from_zone)
    convert_utc = utc.astimezone(to_zone).strftime(fmt)
    return convert_utc


def return_excluded():
    """"
    Returns the excluded plugins.
    :param: None
    :return: EXCLUDED_PLUGINS
    """
    return EXCLUDED_PLUGINS


def return_post():
    """"
    Returns the post-processing plugins.
    :param: None
    :return: POST_PROCESSING_PLUGINS
    """
    return POST_PROCESSING_PLUGINS


def return_included():
    """"
    Returns the included plugins.
    :param: None
    :return: plugin_list
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


def init_argparser():
    """"
    Initialise the arg parser.
    :param: None
    :return: args
    """
    parser = argparse.ArgumentParser(
        description="Blitz-X (Blitz-eXtractor) is a modular forensic triage tool written in Python designed to access \
                    various forensic artifacts on Windows relating to user data exfiltration. The tool will parse the \
                    artifacts, and present them in a format viable for analysis. The output may provide valuable \
                    insights during an incident response in a Windows environment while waiting for a full disk image \
                    to be acquired. The tool is meant to run on live systems on the offending User Account with administrative rights.",
        epilog="ICT2202 Assignment 1 Team Panzerwerfer"
    )
    parser.add_argument("--keydec", help="Imports a private key to decrypt the master hash file.")
    parser.add_argument("--keywords", help="Imports a keyword list to perform a keyword search on the data extracted.")
    args = parser.parse_args()
    return args


def cls():
    """"
    Helper function to clear screen.
    :param: None
    :return: os.system("cls" if os.name == "nt" else "clear")
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """"
    Prints a banner.
    :param: None
    :return: None
    """
    print(" ######                              #     #")
    print(" #     # #      # ##### ######        #   # ")
    print(" #     # #      #   #       #          # #  ")
    print(" ######  #      #   #      #   #####    #   ")
    print(" #     # #      #   #     #            # #  ")
    print(" #     # #      #   #    #            #   # ")
    print(" ######  ###### #   #   ######       #     #")


def load_plugins():
    """"
    Loads plugins the plugins from the "plugin" folder.
    :param: None
    :return: plugin_path, plugins
    """
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = fnmatch.filter(plugins, "*py")
    print("[*] Loading plugins....")
    for plugin in plugins:
        if plugin in POST_PROCESSING_PLUGINS or plugin in EXCLUDED_PLUGINS:
            plugins.remove(plugin)
    print(print_green("[!] Plugins successfully loaded!"))
    return plugin_path, plugins


def run_plugins(plugin_path, plugins, keyword_list):
    """"
    Runs plugins from the "plugin" folder.
    :param: plugin_path, plugins
    :return: None
    """
    print(("[*] Running plugins!"))
    no_of_plugins = len(plugins)
    for plugin in plugins:
        if plugin not in POST_PROCESSING_PLUGINS and plugin not in EXCLUDED_PLUGINS:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            print("\t[+] Running {}".format(plugin))
            module.run()
    for plugin in POST_PROCESSING_PLUGINS:
        plugin_name = plugin[:-3]
        plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
        module = importlib.import_module(plugin_path)
        print("\t[+] Running {}".format(plugin))
        if plugin_name == "keyword_search":
            module.run(keyword_list)
        elif plugin_name == "zehash":
            module.run(HASHPATH)
        else:
            module.run()


def execute():
    """"
    Main function.
    :param: None
    :return: None
    """
    args = init_argparser()

    # Checks if the keydec keywords is present
    if args.keydec:
        cls()
        print("-" * 50)
        print_banner()
        print("-" * 50)
        decrypt_masterhash(args.keydec)
        print("\n[*] Recalculating the hashes for all data and report files and compiling them into 'master_hash_recal.txt!'")
        hash_files(HASH_RECAL)
        comparison(HASH_RECAL)
        sys.exit(0)
    start_time = time.time()
    print("-" * 50)
    print_banner()
    print("-" * 50)
    public_key_path = locate_public_key()
    cls()
    print("-" * 50)
    print_banner()
    print("-" * 50)

    # Loads all the plugins in the 'plugins' folder
    plugin_path, plugins = load_plugins()

    # Runs of all the plugins in the 'plugins' folder
    run_plugins(plugin_path, plugins, args.keywords)

    # Encrypts the master hash file
    encrypt_masterhash(public_key_path)
    print(print_green("\n[!] Total Time Elapsed: %s seconds" % (time.time() - start_time)))
    sys.exit(0)
