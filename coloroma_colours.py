from colorama import Fore, Style


def print_green(text):
	return Fore.GREEN + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE


def print_red(text):
	return Fore.RED + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE


def print_yellow(text):
	return Fore.YELLOW + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE


def print_white(text):
	return Fore.WHITE + Style.BRIGHT + text + Style.NORMAL + Fore.WHITE
