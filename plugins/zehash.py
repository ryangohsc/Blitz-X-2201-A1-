import glob
import os
import hashlib
from pathlib import Path
from colorama import init, Fore, Style


# Global Variables
BLOCK_SIZE = 65536
ROOT = os.getcwd()
HASHPATH = Path(ROOT + "/master_hash.txt")
HASHPATHDEC = Path(ROOT + "/master_hash_decrypted.txt")


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


def check_exist(arg_filename):
    """"
    Helper function that checks if file exists and returns the result.
    :param: arg_filename
    :return: append_write
    """
    if os.path.exists(arg_filename):
        append_write = "a"
    else:
        append_write = "w"
    return append_write


def get_data_files(arg_path, arg_name):
    """"
    Returns all data files.
    :param: arg_path - Path containing all the data files.
            arg_name - The name of the data file.
    :return: result
    """
    result = []
    for name in glob.iglob(arg_path + arg_name):
        result.append(name)
    return result


def md5(arg_file):
    """"
    Hashes file with MD5 and returns it.
    :param: arg_file - File to be hashed.
    :return: file_hash.hexdigest()
    """
    file_hash = hashlib.md5()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha1(arg_file):
    """"
    Hashes file with SHA1 and returns it.
    :param: arg_file - File to be hashed.
    :return: file_hash.hexdigest()
    """
    file_hash = hashlib.sha1()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha256(arg_file):
    """"
    Hashes file with SHA256 and returns it.
    :param: arg_file - File to be hashed.
    :return: file_hash.hexdigest()
    """
    file_hash = hashlib.sha256()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha512(arg_file):
    """"
    Hashes file with SHA512 and returns it.
    :param: arg_file - File to be hashed.
    :return: file_hash.hexdigest()
    """
    file_hash = hashlib.sha512()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def hash_files(hash_path):
    """"
    Hashes files in data and the HTMLReport folder.
    :param: None
    :return: None
    """
    try:
        data_folder = get_data_files(str(Path(ROOT)), "/data/**/*.json")
        append_write = check_exist(hash_path)
        with open(str(hash_path), append_write) as f:
            if append_write == "w":
                f.write("MD5\n")
            else:
                f.write("\nMD5\n")
            for data in data_folder:
                result = md5(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-1\n")
            for data in data_folder:
                result = sha1(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-256\n")
            for data in data_folder:
                result = sha256(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-512\n")
            for data in data_folder:
                result = sha512(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
    except:
        print(print_red("[!] Error hashing files in the 'data' folder!"))
    try:
        report_folder = get_data_files(str(Path(ROOT)), "/HTMLReport/*.html")
        append_write = check_exist(hash_path)
        with open(str(hash_path), append_write) as f:
            if append_write == "w":
                f.write("MD5\n")
            else:
                f.write("\nMD5\n")
            for data in report_folder:
                result = md5(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-1\n")
            for data in report_folder:
                result = sha1(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-256\n")
            for data in report_folder:
                result = sha256(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
            f.write("\nSHA-512\n")
            for data in report_folder:
                result = sha512(data)
                p = Path(data)
                filename = p.name
                f.write(filename + " - " + result + "\n")
    except:
        print(print_red("[!] Error hashing files in the 'HTMLReport' folder!"))


def comparison(hash_recal_path):
    """"
    Calculates the SHA256 hash of master_hash_recal.txt and master_hash_decrypted.txt and compares them.
    :param: hash_recal_path
    :return: None
    """
    print("[*] Calculating the hash of 'master_hash_recal.txt'!")
    hash_recal_path_hash = sha256(hash_recal_path)
    print("\t[+] SHA-256 hash: {}".format(hash_recal_path_hash))
    print("[*] Calculating the hash of 'master_hash_decrypted.txt!'")
    hash_decrypted_path_hash = sha256(HASHPATHDEC)
    print("\t[+] SHA-256 hash: {}".format(hash_decrypted_path_hash))

    if hash_recal_path_hash != hash_decrypted_path_hash:
        print(print_red("[!] The hashes does not match! The file in the 'data' or 'HTMLReport' might be potentially tampered!"))
    else:
        print(print_green("[!] The hashes matches! The files in the 'data' or 'HTMLReport' are forensically sound!"))


def run(hash_path):
    """"
    Runs the zehash module.
    :param: None
    :return: None
    """
    hash_files(HASHPATH)
