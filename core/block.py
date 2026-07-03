import time
import hashlib
import json


class Block:

    def __init__(
        self,
        index,
        transactions,
        previous_hash
    ):

        self.index = index
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash

        self.nonce = 0
        self.hash = self.calculate_hash()


    def calculate_hash(self):

        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }


        block_string = json.dumps(
            block_data,
            sort_keys=True
        )


        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    def mine_block(self, difficulty):

        target = "0" * difficulty

        while self.hash[:difficulty] != target:

            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block {self.index} berhasil ditambang!")
        print(f"Nonce : {self.nonce}")
        print(f"Hash  : {self.hash}")

    def to_dict(self):

        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }