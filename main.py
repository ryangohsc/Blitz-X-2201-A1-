import argparse
import os
import fnmatch
import importlib
import sys

PLUGIN_PATH = "plugins"
EXCLUDED_PLUGINS = []

# Argparser
parser = argparse.ArgumentParser(
    description="Write the description of the tool here",
    epilog="ICT2202 Assignment 1 Team PanzerWerfer"
)
requiredNamed = parser.add_argument_group("required arguments")
parser.add_argument("-o", help="")
args = parser.parse_args()


def return_excluded():
    """
    Returns the excluded plugins
    """
    return EXCLUDED_PLUGINS


def load_plugins():
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    plugins = fnmatch.filter(plugins, "*py")
    print("[+] Loading plugins....")
    for plugin in plugins:
        print(plugin)
    print("\n[+] Plugins successfully loaded!")
    return plugin_path, plugins


def run_plugins(plugin_path, plugins):
    print("\n[+] Running plugins!")
    for plugin in plugins:
        if plugin in EXCLUDED_PLUGINS:
            pass        
        else:
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
    print("-" * 50)
    print_banner()
    print("-" * 50)
    plugin_path, plugins = load_plugins()
    run_plugins(plugin_path, plugins)
    

if __name__ == '__main__':
    main()