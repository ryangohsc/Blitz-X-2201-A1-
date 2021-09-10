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
    random_char = random.choice(list(cowsay.char_names))
    print(cowsay.get_output_string(random_char, "ICT2202 A1 Assignment by Team PanzerWerfer"))


def main():
    """
    Main function
    """
    print("-" * 80)
    print_banner()
    print("-" * 80)
    get_prev_ran_prog()


if __name__ == '__main__':
    main()
