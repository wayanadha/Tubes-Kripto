from core.wallet import Wallet
from core.transaction import Transaction
from core.blockchain import Blockchain

buyer = Wallet()

blockchain = Blockchain()

tx = Transaction(
    sender=buyer.address,
    receiver="ADDR_SELLER",
    amount=100,
    nonce=buyer.nonce
)

tx.sign_transaction(buyer)

blockchain.add_transaction(tx)

print("Pending Transaction:")
print(blockchain.get_pending_transactions())

print("\nMining...\n")

blockchain.mine_pending_transactions("ADDR_MINER")

print("\nBlockchain Valid:")
print(blockchain.is_chain_valid())

blockchain.save_to_json()

print("\nBlockchain berhasil disimpan ke blockchain.json")