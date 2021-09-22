import argparse
import importlib
import os

PLUGIN_PATH = "plugins"

# Argparser
parser = argparse.ArgumentParser(
    description="Write the description of the tool here",
    epilog="ICT2202 Assignment 1 Team PanzerWerfer"
)
requiredNamed = parser.add_argument_group("required arguments")
parser.add_argument("-o", help="")
args = parser.parse_args()


def load_plugins():
    cwd = os.getcwd()
    plugin_path = "{}\\{}".format(cwd, PLUGIN_PATH)
    plugins = os.listdir(plugin_path)
    print("[+] Loading modules....")
    for plugin in plugins:
        print(plugin)
    print("\n[!] Modules successfully loaded!")
    return plugin_path, plugins


def run_plugins(plugin_path, plugins):
    for plugin in plugins:
        plugin = plugin[:-3]
        plugin_path = "{}.{}".format(PLUGIN_PATH, plugin)
        importlib.import_module(plugin_path)


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