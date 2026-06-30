import uuid
import time
import json


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