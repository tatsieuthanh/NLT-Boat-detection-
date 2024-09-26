from Crypto.Cipher import AES as PyAES
from Crypto.Util.Padding import pad, unpad
import os
import base64

class AES:
    # Hàm để mã hóa
    def encrypt_aes_cbc(self, key, plaintext):
        # Tạo IV ngẫu nhiên
        iv = os.urandom(16)
        cipher = PyAES.new(key, PyAES.MODE_CBC, iv)
        
        # Đệm plaintext và mã hóa
        ciphertext = cipher.encrypt(pad(plaintext.encode(), PyAES.block_size))
        
        # Trả về IV và ciphertext, mã hóa chúng để dễ dàng lưu trữ
        return base64.b64encode(iv).decode('utf-8'), base64.b64encode(ciphertext).decode('utf-8')

    # Hàm để giải mã
    def decrypt_aes_cbc(self, key, iv, ciphertext):
        iv = base64.b64decode(iv)
        ciphertext = base64.b64decode(ciphertext)
        
        cipher = PyAES.new(key, PyAES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), PyAES.block_size)
        
        return decrypted.decode('utf-8')

# Ví dụ sử dụng
if __name__ == "__main__":
    key = b'Sixteen byte key'  # Khóa phải có độ dài 16, 24 hoặc 32 byte
    plaintext = "Hello, World!"
    
    aes_instance = AES()  # Tạo thể hiện của lớp AES

    # Mã hóa
    iv, ciphertext = aes_instance.encrypt_aes_cbc(key, plaintext)
    print(f'IV: {iv}')
    print(f'Ciphertext: {ciphertext}')
    
    # Giải mã
    decrypted_text = aes_instance.decrypt_aes_cbc(key, iv, ciphertext)
    print(f'Decrypted: {decrypted_text}')
