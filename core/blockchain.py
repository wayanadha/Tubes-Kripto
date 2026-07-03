from core.block import Block


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()


    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            transactions=[],
            previous_hash="0"
        )

        self.chain.append(genesis_block)


    def get_latest_block(self):
        return self.chain[-1]


    def add_block(self, transactions):

        latest_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=latest_block.hash
        )

        self.chain.append(new_block)


    def to_dict(self):

        return [
            block.to_dict()
            for block in self.chain
        ]