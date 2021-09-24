import hashlib
from plugins.auxillary import get_project_root
from pathlib import Path
import glob
import os

ROOT = str(get_project_root())
BLOCK_SIZE = 65536
HASHPATH = Path(ROOT + "/master_hash.txt")


def check_exist(arg_filename):
    """
    Checks if file exists and returns the result
    """
    if os.path.exists(arg_filename):
        append_write = "a"
    else:
        append_write = "w"
    return append_write


def get_data_files(arg_path, arg_name):
    """
    Returns all data files
    """
    result = []
    for name in glob.iglob(arg_path + arg_name):
        result.append(name)
    return result


def md5(arg_file):
    """
    Hashes file with MD5 and returns it
    """
    file_hash = hashlib.md5()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha1(arg_file):
    """
    Hashes file with SHA1 and returns it
    """
    file_hash = hashlib.sha1()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha256(arg_file):
    """
    Hashes file with SHA256 and returns it
    """
    file_hash = hashlib.sha256()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def sha512(arg_file):
    """
    Hashes file with SHA512 and returns it
    """
    file_hash = hashlib.sha512()
    with open(arg_file, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def hash_files():
    """
    Hashes files in data and the HTMLReport folder
    """
    try:
        data_folder = get_data_files(str(Path(ROOT)), "/data/**/*.json")
        append_write = check_exist(HASHPATH)
        with open(str(HASHPATH), append_write) as f:
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
        pass
    try:
        report_folder = get_data_files(str(Path(ROOT)), "/HTMLReport/*.html")
        append_write = check_exist(HASHPATH)
        with open(str(HASHPATH), append_write) as f:
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
        pass


def run():
    hash_files()


if __name__ == "__main__":
    run()