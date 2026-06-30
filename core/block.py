import time


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
        self.hash = None


    def to_dict(self):

        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }