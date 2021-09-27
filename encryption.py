from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

def encrypt():
    pub_key = r"C:\Users\tux\Documents\GitHub\2202-A1\public_key.pem"
    recipient_key = RSA.import_key(open(pub_key).read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    session_key = get_random_bytes(16)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

def export_pvt_key(pvt_key, filename):
    with open(filename, "wb") as file:
        file.write(pvt_key.exportKey('PEM', "test"))
    file.close()

def export_pub_key(public_key1, filename):
    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()

keypair = RSA.generate(2048)
public_key = keypair.publickey()
export_pvt_key(keypair, 'private_key.pem')
export_pub_key(public_key, 'public_key.pem')