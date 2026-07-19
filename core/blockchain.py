from flask import ctx
from core import transaction
import json

from core.block import Block
from core.google_sheet import send_block
from core.storage import save_wallets, save_blockchain


class Blockchain:

    def __init__(self, difficulty=3, mining_reward=50, create_genesis=True):

        self.chain = []
        self.wallets = {}

        self.pending_transactions = []

        self.transactions = {}

        self.difficulty = difficulty
        self.mining_reward = mining_reward

        if create_genesis:
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

    # ==========================
    # WALLET
    # ==========================

    def register_wallet(self, wallet):

        self.wallets[wallet.address] = wallet

        return wallet.address
    
    def get_wallet(self, address):
        return self.wallets.get(address)

    def load_wallets(self, wallets):

        for wallet in wallets:
            self.register_wallet(wallet)

    def get_all_wallets(self):

        return [
            wallet.get_wallet_info()
            for wallet in self.wallets.values()
        ]

    def has_sufficient_balance(self, sender, amount):

        wallet = self.get_wallet(sender)

        if wallet is None:
            return False

        return wallet.balance >= amount
    
    def load_wallets(self, wallets):

        for wallet in wallets:
            self.register_wallet(wallet)

    # ==========================
    # MEMPOOL
    # ==========================

    def add_transaction(self, transaction):

        # Transaction object
        if hasattr(transaction, "verify_signature"):

            if not transaction.verify_signature():
                raise ValueError("Digital signature tidak valid.")

            if not self.has_sufficient_balance(
                transaction.sender,
                transaction.amount
            ):
                raise ValueError("Saldo tidak mencukupi.")

            self.pending_transactions.append(
                transaction.to_dict()
            )

        # Dictionary (misalnya mining reward / testing)
        else:

            self.pending_transactions.append(transaction)

    def get_pending_transactions(self):

        return self.pending_transactions

    # ==========================
    # MINING
    # ==========================

    def mine_pending_transactions(self, miner_address):

        if len(self.pending_transactions) == 0:
            print("Tidak ada transaksi untuk ditambang.")
            return False

        reward_transaction = {
            "from": "SYSTEM",
            "to": miner_address,
            "amount": self.mining_reward,
            "type": "mining_reward"
        }

        transactions = self.pending_transactions.copy()
        transactions.append(reward_transaction)

        latest_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=latest_block.hash
        )

        new_block.mine_block(self.difficulty)

        # update saldo wallet

        for tx in transactions:

            # Update sender
            if tx["from"] != "SYSTEM":

                sender = self.get_wallet(tx["from"])

                if sender:
                    sender.decrease_balance(tx["amount"])

                    # Tambah nonce setelah transaksi berhasil masuk block
                    sender.increase_nonce()

            # Update receiver
            receiver = self.get_wallet(tx["to"])

            if receiver:
                receiver.increase_balance(tx["amount"])

        self.chain.append(new_block)
        # Simpan blockchain
        save_blockchain(self)

        # Simpan wallet terbaru
        save_wallets(self.wallets.values())

        # Kirim block ke Google Spreadsheet
        send_block(new_block)

        # kosongkan mempool
        self.pending_transactions = []

        return True

    # ==========================
    # BLOCK
    # ==========================

    def add_block(self, transactions):

        latest_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=latest_block.hash
        )

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        send_block(new_block)


    # ==========================
    # VALIDATION
    # ==========================

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash != current_block.calculate_hash():
                return False

        return True

    def load_chain(self, chain_data):

        self.chain = []

        for block_data in chain_data:

            block = Block.from_dict(
                block_data
            )

            self.chain.append(block)

    # ==========================
    # JSON
    # ==========================

    def to_dict(self):

        return [
            block.to_dict()
            for block in self.chain
        ]

    def save_to_json(self, filename="blockchain.json"):

        with open(filename, "w") as file:

            json.dump(
                self.to_dict(),
                file,
                indent=4
            )