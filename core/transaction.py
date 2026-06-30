import uuid
import time
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


class Transaction:

    def __init__(
        self,
        sender,
        receiver,
        amount,
        nonce,
        tx_type="native_transfer"
    ):

        self.tx_id = str(uuid.uuid4())
        self.type = tx_type
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.nonce = nonce
        self.timestamp = int(time.time())

        self.signature = None
        self.public_key = None


    def get_payload(self):

        payload = {
            "tx_id": self.tx_id,
            "type": self.type,
            "from": self.sender,
            "to": self.receiver,
            "amount": self.amount,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }

        return json.dumps(
            payload,
            sort_keys=True
        )


    def sign_transaction(self, wallet):

        payload = self.get_payload().encode()

        signature = wallet.private_key.sign(
            payload,
            ec.ECDSA(hashes.SHA256())
        )


        self.signature = signature.hex()

        self.public_key = wallet.get_public_key_pem()


    def verify_signature(self):

        try:

            public_key = serialization.load_pem_public_key(
                self.public_key.encode()
            )


            public_key.verify(
                bytes.fromhex(self.signature),
                self.get_payload().encode(),
                ec.ECDSA(hashes.SHA256())
            )


            return True


        except InvalidSignature:

            return False



    def to_dict(self):

        return {
            "tx_id": self.tx_id,
            "type": self.type,
            "from": self.sender,
            "to": self.receiver,
            "amount": self.amount,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "public_key": self.public_key,
            "signature": self.signature
        }