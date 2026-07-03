from core.block import Block


class Blockchain:

    def __init__(self, difficulty=3, mining_reward=50):
        self.chain = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
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

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)

    def mine_pending_transactions(self, miner_address, transactions):

        reward_transaction = {
            "from": "SYSTEM",
            "to": miner_address,
            "amount": self.mining_reward,
            "type": "mining_reward"
        }

        all_transactions = transactions + [reward_transaction]

        latest_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            transactions=all_transactions,
            previous_hash=latest_block.hash
        )

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # cek apakah previous hash masih sesuai
            if current_block.previous_hash != previous_block.hash:
                return False

            # cek apakah hash block masih sama
            if current_block.hash != current_block.calculate_hash():
                return False

        return True

    def to_dict(self):

        return [
            block.to_dict()
            for block in self.chain
        ]