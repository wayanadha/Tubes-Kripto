import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Wallet:

    def __init__(self, name="Unknown", private_key=None):
        self.name = name

        if private_key is None:
            self.private_key = self.generate_private_key()
        else:
            self.private_key = private_key

        self.public_key = self.generate_public_key()
        self.address = self.generate_address()

        self.balance = 1000
        self.nonce = 0
        
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
            "name": self.name,
            "address": self.address,
            "balance": self.balance,
            "nonce": self.nonce,
            "public_key": self.get_public_key_pem()
        }

    def get_balance(self):
        return self.balance

    def increase_balance(self, amount):
        self.balance += amount

    def decrease_balance(self, amount):

        if amount > self.balance:
            raise ValueError("Saldo tidak mencukupi.")

        self.balance -= amount

    def increase_nonce(self):
        self.nonce += 1
    
    def transfer(self, receiver, amount):

        if amount <= 0:
            raise ValueError("Jumlah transfer harus lebih dari 0.")

        if amount > self.balance:
            raise ValueError("Saldo tidak mencukupi.")

        self.decrease_balance(amount)

        receiver.increase_balance(amount)

        self.increase_nonce()

    def to_storage_dict(self):

        return {
            "name": self.name,
            "address": self.address,
            "balance": self.balance,
            "nonce": self.nonce,
            "private_key": self.get_private_key_pem(),
            "public_key": self.get_public_key_pem()
        }

    @classmethod
    def from_storage_dict(cls, data):

        private_key = load_pem_private_key(
            data["private_key"].encode(),
            password=None
        )

        wallet = cls(
            name=data["name"],
            private_key=private_key
        )

        wallet.balance = data["balance"]
        wallet.nonce = data["nonce"]

        return wallet