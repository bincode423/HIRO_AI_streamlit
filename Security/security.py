import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac, padding
from cryptography.hazmat.backends import default_backend
import moduls.email as em

def encrypt_secure(key: bytes, plaintext: str) -> bytes:
    aes_key = key[:32]
    hmac_key = key[32:]
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(iv + ciphertext)
    tag = h.finalize()
    return iv + ciphertext + tag

from cryptography.exceptions import InvalidSignature

def decrypt_secure(key: bytes, encrypted_data: bytes) -> str:
    aes_key = key[:32]
    hmac_key = key[32:]
    iv = encrypted_data[:16]
    tag = encrypted_data[-32:]
    ciphertext = encrypted_data[16:-32]
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(iv + ciphertext)
    try:
        h.verify(tag)
    except InvalidSignature:
        em.send_email('developer.bin423@gmail.com',f'## 보안 알림\n암호문에서 암호문 손상 또는 키 변경 감지\n암호문이 해킹으로 인해 변경되었거나 외부적 요인으로 손상되었을 가능성이 있습니다.\n대입된 문자열\n{encrypted_data}')
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()
