import sys
import os
import fnmatch
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from colorama import init, Fore, Style


# Global variables
BUFFER_SIZE = 1024 * 1024
init(convert=True)


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


def export_pvt_key(pvt_key, filename, password):
    """"
    Exports the private key to the file system.
    :param: pvt_key, filename, password
    :return: None
    """
    with open(filename, "wb") as file:
        file.write(pvt_key.exportKey('PEM', password))
    file.close()


def export_pub_key(public_key1, filename):
    """"
    Exports the public key to the file system.
    :param: public_key1, filename
    :return: None
    """
    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()


def generate_rsa_key():
    """"
    Generates a 2048-bit AES key and exports it to the file system.
    :param: None
    :return: None
    """
    keypair = RSA.generate(2048)
    public_key = keypair.publickey()

    # Prompt the user to enter a password for to encrypt the private key
    password = input("[+] Enter a password to encrypt the private key: ")

    # Export the public and private key to the file system.
    export_pub_key(public_key, 'public_key.pem')
    export_pvt_key(keypair, 'private_key.pem', password)
    print(print_green("[!] RSA key successfully generated!"))


def locate_public_key():
    """"
    Locates the presence of a public key on the file system.
    :param: None
    :return: "public_key.pem"
    """
    # Searches the file system for the presence of a public key.
    pem_file = fnmatch.filter(os.listdir(os.getcwd()), "*pem")
    if len(pem_file) == 0:
        generate_rsa_key()

    # Searches the file system for the presence of a public key again.
    pem_file = fnmatch.filter(os.listdir(os.getcwd()), "*pem")
    if "public_key.pem" not in pem_file:
        print(print_red("[!] Error! Ensure that public key file is named as 'public_key.pem'"))
        sys.exit(-1)
    return "public_key.pem"


def import_pub_key(pub_key_path):
    """"
    Imports a public key from the file system.
    :param: pub_key_path
    :return: None or recipient_key
    """
    try:
        recipient_key = RSA.import_key(open(pub_key_path).read())
        return recipient_key

    except FileNotFoundError:
        print(print_red("[!] Error unable to open public key file!"))
        return


def generate_sha256_hash(filename):
    """"
    Generates a sha256 hash of a file.
    :param: filename
    :return: sha256_hash
    """
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K.
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        sha256_hash = sha256_hash.hexdigest()
    return sha256_hash


def encrypt_masterhash(pub_key_path):
    """"
    Encrypts the master hash file using AES.
    :param: pub_key_path
    :return: None
    """
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
    print(print_green("[!] Master hashfile successfully encrypted into '{}'!".format(output_filename)))

    # Generate the SHA256 hash of the masterhash file
    sha256_hash = generate_sha256_hash(input_filename)
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_hash = rsa_cipher.encrypt(sha256_hash.encode())
    file_hash_out.write(encrypted_hash)
    print(print_green("[!] Master hashfile's hash successfully encrypted into '{}'!".format(output_hash_filename)))

    # Close file handles
    file_in.close()
    file_out.close()
    file_hash_out.close()
    file_key_out.close()

    # Remove the original master hash txt file
    os.remove(input_filename)


def decrypt_masterhash(pvt_key_path):
    """"
    Decrypts the master hash file using AES and compares it with the decrypted hash obtained from master_hash.bin.
    :param: pvt_key_path
    :return: None
    """
    # Get the file handles
    input_filename = 'master_hash.bin'
    input_hash_filename = 'master_hash_sha256.bin'
    input_aes_filename = 'aes.bin'
    output_filename = 'master_hash_decrypted.txt'

    try:
        file_in = open(input_filename, 'rb')
    except FileNotFoundError:
        print(print_red("[!] master_hash.bin not found!"))
        exit(-1)

    try:
        file_hash_in = open(input_hash_filename, 'rb')
    except FileNotFoundError:
        print("[!] master_hash_sha256.bin not found!")
        exit(-1)

    try:
        file_key_in = open(input_aes_filename, 'rb')
    except FileNotFoundError:
        print("[!] aes.bin not found!")
        exit(-1)

    file_out = open(output_filename, 'wb')

    # Import the private key
    password = input("[+] Enter passphrase: ")

    try:
        pvt_key = RSA.import_key(open(pvt_key_path).read(), passphrase=password)
    except FileNotFoundError:
        print(print_red("[!] The private key: {} cannot be found!".format(pvt_key_path)))
        sys.exit(-1)
    except ValueError:
        print(print_red("[!] Incorrect Password!"))
        sys.exit(-1)
    rsa_cipher = PKCS1_OAEP.new(pvt_key)

    # Decrypt the AES key
    enc_aes_key = file_key_in.read()
    dec_aes_key = rsa_cipher.decrypt(enc_aes_key)
    nonce = file_in.read(16)
    aes_cipher = AES.new(dec_aes_key, AES.MODE_GCM, nonce=nonce)  # Create a cipher object to encrypt data

    # Decrypt the encrypted hashfile
    print("[*] Decrypting '{}'".format(input_hash_filename))
    enc_hash = file_hash_in.read()
    dec_hash = rsa_cipher.decrypt(enc_hash).decode()
    print("\t[+] Decrypted hash obtained: {}".format(dec_hash))

    # Decrypt the data
    print("[*] Decrypting '{}'".format(input_filename))
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
    print("\t[+] SHA-256 hash of master_hash_decrypted.txt: {}".format(sha256_hash))

    # Close file handles
    file_in.close()
    file_hash_in.close()
    file_key_in.close()
    file_out.close()

    # Cleanup bin files
    bin_file = fnmatch.filter(os.listdir(os.getcwd()), "*bin")
    for item in bin_file:
        os.remove(item)
    if dec_hash == sha256_hash:
        print(print_green("[!] The hashes matches! The '{}' has not been tampered with!".format(input_filename)))
    else:
        print(print_red("[!] The hashes does not match! The '{}' might be potentially tampered!".format(input_filename)))
