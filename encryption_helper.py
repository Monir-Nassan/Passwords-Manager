from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

def encrypt(key, text):

    iv = generate_iv()

    padded_text = pad(text.encode(), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(padded_text)

    return encrypted_text, iv


def decrypt(key, encrypted_text, iv):

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)

    padded_text = cipher.decrypt(encrypted_text)
    text = unpad(padded_text, AES.block_size)

    return text




def generate_iv():
    return get_random_bytes(AES.block_size)

