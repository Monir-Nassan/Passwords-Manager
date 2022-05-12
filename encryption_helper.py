from Crypto.Cipher import AES

def encrypt(key, text):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipertext, tag = cipher.encrypt_and_digest(text.encode())
    return nonce, cipertext, tag


def decrypt(key, cipherdtext, nonce, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    text = cipher.decrypt(cipherdtext)
    try:
        cipher.verify(tag)
        return True, text
    except ValueError:
        print('Wrong Tag')
        return False, 'Wrong tag'


