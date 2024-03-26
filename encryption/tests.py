import random
import string

from cryptography.fernet import Fernet
from django.test import TestCase

from encryption.encryption import Encryption

generate_random_text = lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=100))


# Create your tests here.
class TestEncryption(TestCase):
    # prepare the test
    def setUp(self):
        self.key = Fernet.generate_key()
        self.encryption = Encryption(self.key)
        self.random_text = generate_random_text()

        encrypted_text = self.encryption.encrypt(self.random_text.encode())
        decrypted_text = self.encryption.decrypt(encrypted_text)
        print(100 * "*")
        print("Generating Key")
        print(f"Key: {self.key}")
        print(f"Type: {type(self.key)}")
        print(f"Length: {len(self.key)}")
        print("Original Text: ", self.random_text)
        print("Encrypted Text: ", encrypted_text)
        print("Decrypted Text: ", decrypted_text)
        print("Decrypted Text Type: ", type(decrypted_text))
        print(isinstance(decrypted_text, bytes))

    def test_encryption_key_not_none(self):
        self.assertNotEqual(self.key, None)

    def test_encryption_key_length(self):
        self.assertEqual(len(self.key), 44)

    def test_encryption_key_type(self):
        self.assertTrue(isinstance(self.key, bytes))

    def test_decrypted_text_equals_original_text(self):
        encrypted_text = self.encryption.encrypt(self.random_text.encode())
        decrypted_text = self.encryption.decrypt(encrypted_text)
        self.assertEqual(self.random_text, decrypted_text)

    def test_decrypted_text_type(self):
        encrypted_text = self.encryption.encrypt(self.random_text.encode())
        decrypted_text = self.encryption.decrypt(encrypted_text)
        self.assertTrue(isinstance(decrypted_text, str))
