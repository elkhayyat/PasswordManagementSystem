from cryptography.fernet import Fernet


class KeyGenerator:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()


class Encryption:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data) -> bytes:
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(data)

    def decrypt(self, data) -> str:
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(data).decode()
