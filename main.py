import argparse
from auxillary import *
import cowsay
import random

# Argparser
parser = argparse.ArgumentParser(
    description="Write the description of the tool here",
    epilog="ICT2202 Assignment 1 Team PanzerWerfer"
)
requiredNamed = parser.add_argument_group("required arguments")
# parser.add_argument("-o", help="")
args = parser.parse_args()


def print_banner():
    """
    Prints a random banner
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
    get_prev_ran_prog()


if __name__ == '__main__':
    main()
