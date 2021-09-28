import argparse
import os
import fnmatch
import importlib
import hashlib
import time
from dateutil import tz
from datetime import datetime, timedelta
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


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
parser.add_argument("-keygen", help="Generate a set of RSA public and private key.", action='store_true')
parser.add_argument("-keyenc", help="Imports a public key to encrypt the master hash file.")
parser.add_argument("-keydec", help="Imports a private key to decrypt the master hash file.")
parser.add_argument("-wordlist", help="Imports a list of keywords for the keyword search module.")
args = parser.parse_args()


WIN32_EPOCH = datetime(1601, 1, 1)
BUFFER_SIZE = 1024 * 1024

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
    plugins = fnmatch.filter(plugins, "*py")
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


def export_pvt_key(pvt_key, filename, password):
    with open(filename, "wb") as file:
        file.write(pvt_key.exportKey('PEM', password))
    file.close()


def export_pub_key(public_key1, filename):
    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()


def generate_rsa_keys():
    keypair = RSA.generate(2048)
    public_key = keypair.publickey()
    password = input("[+] Enter a password to encrypt the private key: ")
    export_pvt_key(keypair, 'private_key.pem', password)
    export_pub_key(public_key, 'public_key.pem')
    print("[!] RSA keys successfully generated!")


def import_pub_key(pub_key_path):
    try:
        recipient_key = RSA.import_key(open(pub_key_path).read())
        return recipient_key

    except FileNotFoundError:
        print("[!] Error unable to open public key file!")
        return


def encrypt_masterhash(pub_key_path):
    try:
        # Import the public key
        public_key = RSA.import_key(open(pub_key_path).read())

        input_filename = 'master_hash.txt'
        output_filename = 'master_hash_sha256.bin'

        sha256_hash = hashlib.sha256()
        with open(input_filename, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            sha256_hash = sha256_hash.hexdigest()

        rsa_cipher = PKCS1_OAEP.new(public_key)
        encrypted_hash = rsa_cipher.encrypt(sha256_hash.encode())

        file_out = open(output_filename, 'wb')
        file_out.write(encrypted_hash)
        file_out.close()
        print("[!] Master hashfile's hash successfully encrypted!")
    except FileNotFoundError:
        print("[!] Error unable to open public key file!")
    return


def decrypt_masterhash(pvt_key_path):
    input_filename = 'master_hash.txt'
    input_filename_encrypted_hash = 'master_hash_sha256.bin'
    file_in = open(input_filename, 'rb')
    file_in_hash = open(input_filename_encrypted_hash, 'rb')

    # try:
    # Import the private key
    password = input("[+] Enter passphrase: ")
    pvt_key = RSA.import_key(open(pvt_key_path).read(), passphrase=password)

    # Decrypt the encrypted hashfile
    enc_hash = file_in_hash.read()
    rsa_cipher = PKCS1_OAEP.new(pvt_key)
    dec_hash = rsa_cipher.decrypt(enc_hash)

    sha256_hash = hashlib.sha256()
    with open(input_filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        sha256_hash = sha256_hash.hexdigest()

    if dec_hash.decode() == sha256_hash:
        print("[!] Hash verified! File was not tampered with!")

    else:
        print("[!] Hash verification failure! File was tampered with!")


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
    if args.keygen:
        generate_rsa_keys()

    elif args.keyenc:
        encrypt_masterhash(args.keyenc)

    elif args.keydec:
        decrypt_masterhash(args.keydec)

    elif args.wordlist:
        pass

    else:
        start_time = time.time()
        print("-" * 50)
        print_banner()
        print("-" * 50)
        plugin_path, plugins = load_plugins()
        run_plugins(plugin_path, plugins)
        print("[!] Total Time Elapsed: %s seconds" % (time.time() - start_time))
    exit(-1)


if __name__ == '__main__':
    main()