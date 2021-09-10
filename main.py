import argparse
from auxillary import *

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
    Prints the banner
    """
    pass


def main():
    """
    Main function
    """
    print_banner()
    get_prev_ran_prog()


if __name__ == '__main__':
    main()
