from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import json

# Ensure the key is 16 bytes and the IV is also 16 bytes
key = b"NLT@2024@09@Ver1" # 16 bytes
iv =  b"IV4@#NLT@2024@09" # 16 bytes

class AESCipher:
    def __init__(self):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_data = self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return b64encode(encrypted_data).decode('utf-8') 

    def decrypt(self, data):
        raw = b64decode(data)  # Decode from Base64
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_data = unpad(self.cipher.decrypt(raw), AES.block_size)
        return decrypted_data.decode('utf-8')

if __name__ == "__main__":
    cipher_instance = AESCipher()
    
    # Encrypt
    encrypted = cipher_instance.encrypt("hello")
    print(f'Encrypted: {encrypted}')
    
    # Decrypt
    decrypted = cipher_instance.decrypt(encrypted)
    print(f'Decrypted: {decrypted}')
