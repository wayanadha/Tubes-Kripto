import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class Wallet:

    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()


    def generate_private_key(self):
        private_key = ec.generate_private_key(
            ec.SECP256K1()
        )

        return private_key


    def generate_public_key(self):
        public_key = self.private_key.public_key()

        return public_key


    def get_private_key_pem(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()


    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()


    def generate_address(self):

        public_key = self.get_public_key_pem()

        hashed = hashlib.sha256(
            public_key.encode()
        ).hexdigest()

        address = "ADDR_" + hashed[:40]

        return address


    def get_wallet_info(self):

        return {
            "address": self.address,
            "public_key": self.get_public_key_pem()
        }