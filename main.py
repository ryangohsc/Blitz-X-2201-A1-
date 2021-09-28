import argparse
import os
import fnmatch
import importlib
import hashlib
import time
import warnings
from dateutil import tz
from datetime import datetime, timedelta
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


PLUGIN_PATH = "plugins"
EXCLUDED_PLUGINS = []
POST_PROCESSING_PLUGINS = ["keyword_search.py", "report.py", "zehash.py"]

# Argparser
parser = argparse.ArgumentParser(
    description="Write the description of the tool here",
    epilog="ICT2202 Assignment 1 Team Panzerwerfer"
)
requiredNamed = parser.add_argument_group("required arguments")
parser.add_argument("-keydec", help="Imports a private key to decrypt the master hash file.")
args = parser.parse_args()

warnings.filterwarnings("ignore")
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
    print("[*] Loading plugins....")
    for plugin in plugins:
        print(plugin)
    print("[!] Plugins successfully loaded!")
    return plugin_path, plugins


def run_plugins(plugin_path, plugins):
    print("[*] Running plugins!")
    for plugin in plugins:
        if plugin in EXCLUDED_PLUGINS:
            pass
        elif plugin in POST_PROCESSING_PLUGINS:
            pass
        else:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            module.run()
            print("\t[+] Running {}".format(plugin))
    for plugin in plugins:
        if plugin in POST_PROCESSING_PLUGINS:
            plugin_name = plugin[:-3]
            plugin_path = "{}.{}".format(PLUGIN_PATH, plugin_name)
            module = importlib.import_module(plugin_path)
            module.run()
            print("\t[+] Running {}".format(plugin))
    print("[!] Plugins successfully executed!")


def export_pvt_key(pvt_key, filename, password):
    with open(filename, "wb") as file:
        file.write(pvt_key.exportKey('PEM', password))
    file.close()


def export_pub_key(public_key1, filename):
    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()


def generate_rsa_key():
    keypair = RSA.generate(2048)
    public_key = keypair.publickey()
    password = input("[+] Enter a password to encrypt the private key: ")
    export_pub_key(public_key, 'public_key.pem')
    export_pvt_key(keypair, 'private_key.pem', password)
    print("[!] RSA key successfully generated!")


def locate_public_key():
    pem_file = fnmatch.filter(os.listdir(get_project_root()), "*pem")
    if len(pem_file) == 0:
        generate_rsa_key()
    pem_file = fnmatch.filter(os.listdir(get_project_root()), "*pem")
    if "public_key.pem" not in pem_file:
        print("[!] Error! Ensure that public key file is named as 'public_key.pem'")
        exit(-1)
    return "public_key.pem"


def import_pub_key(pub_key_path):
    try:
        recipient_key = RSA.import_key(open(pub_key_path).read())
        return recipient_key

    except FileNotFoundError:
        print("[!] Error unable to open public key file!")
        return


def generate_sha256_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        sha256_hash = sha256_hash.hexdigest()
    return sha256_hash


def encrypt_masterhash(pub_key_path):
    # Import the public key
    public_key = RSA.import_key(open(pub_key_path).read())

    # Get the file handles
    input_filename = 'master_hash.txt'
    output_filename = 'master_hash.bin'
    output_hash_filename = 'master_hash_sha256.bin'
    output_aes_filename = 'aes.bin'
    file_in = open(input_filename, 'rb')
    file_out = open(output_filename, 'wb')
    file_hash_out = open(output_hash_filename, 'wb')
    file_key_out = open(output_aes_filename, 'wb')

    # Generate AES cipher and cipher key
    aes_key = get_random_bytes(32)
    aes_cipher = AES.new(aes_key, AES.MODE_GCM)  # Create a cipher object to encrypt data
    file_out.write(aes_cipher.nonce)  # Write out the nonce to the output file under the salt

    # Export encrypted AES key
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_key = rsa_cipher.encrypt(aes_key)
    file_key_out.write(encrypted_key)

    # Encrypt data
    data = file_in.read(BUFFER_SIZE)  # Read in some of the file
    while len(data) != 0:  # Check if we need to encrypt anymore data
        encrypted_data = aes_cipher.encrypt(data)  # Encrypt the data we read
        file_out.write(encrypted_data)  # Write the encrypted data to the output file
        data = file_in.read(BUFFER_SIZE)  # Read some more of the file to see i

    tag = aes_cipher.digest()  # Signal to the cipher that we are done and get the tag
    file_out.write(tag)
    print("[!] Master hash file successfully encrypted!")

    # Generate the SHA256 hash of the masterhash file
    sha256_hash = generate_sha256_hash(input_filename)
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_hash = rsa_cipher.encrypt(sha256_hash.encode())
    file_hash_out.write(encrypted_hash)
    print("[!] Master hashfile's hash successfully encrypted!")

    # Close file handles
    file_in.close()
    file_out.close()
    file_hash_out.close()
    file_key_out.close()

    # Remove the original master hash txt file
    os.remove(input_filename)
    return


def decrypt_masterhash(pvt_key_path):
    # Get the file handles
    input_filename = 'master_hash.bin'
    input_hash_filename = 'master_hash_sha256.bin'
    input_aes_filename = 'aes.bin'
    output_filename = 'master_hash_decrypted.txt'
    file_in = open(input_filename, 'rb')
    file_hash_in = open(input_hash_filename, 'rb')
    file_key_in = open(input_aes_filename, 'rb')
    file_out = open(output_filename, 'wb')

    # Import the private key
    password = input("[+] Enter passphrase: ")
    pvt_key = RSA.import_key(open(pvt_key_path).read(), passphrase=password)
    rsa_cipher = PKCS1_OAEP.new(pvt_key)

    # Decrypt the AES key
    enc_aes_key = file_key_in.read()
    dec_aes_key = rsa_cipher.decrypt(enc_aes_key)
    nonce = file_in.read(16)
    aes_cipher = AES.new(dec_aes_key, AES.MODE_GCM, nonce=nonce)  # Create a cipher object to encrypt data

    # Decrypt the encrypted hashfile
    enc_hash = file_hash_in.read()
    dec_hash = rsa_cipher.decrypt(enc_hash).decode()

    # Decrypt the data
    file_in_size = os.path.getsize(input_filename)
    encrypted_data_size = file_in_size - 16 - 16

    for _ in range(int(encrypted_data_size / BUFFER_SIZE)):
        data = file_in.read(BUFFER_SIZE)
        decrypted_data = aes_cipher.decrypt(data)
        file_out.write(decrypted_data)
    data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))
    decrypted_data = aes_cipher.decrypt(data)
    file_out.write(decrypted_data)
    file_out.close()

    # Generate the SHA256 hash of the masterhash file
    sha256_hash = generate_sha256_hash(output_filename)

    # Close file handles
    file_in.close()
    file_hash_in.close()
    file_key_in.close()
    file_out.close()

    # Cleanup bin files
    bin_file = fnmatch.filter(os.listdir(get_project_root()), "*bin")
    for item in bin_file:
        os.remove(item)
    print(dec_hash)
    print(sha256_hash)


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
    if args.keydec:
        decrypt_masterhash(args.keydec)

    else:
        public_key_path = locate_public_key()
        start_time = time.time()
        print("-" * 50)
        print_banner()
        print("-" * 50)
        plugin_path, plugins = load_plugins()
        run_plugins(plugin_path, plugins)
        encrypt_masterhash(public_key_path)
        print("\n[!] Total Time Elapsed: %s seconds" % (time.time() - start_time))
    exit(-1)


if __name__ == '__main__':
    main()
