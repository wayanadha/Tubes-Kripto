from core.wallet import Wallet
from core.blockchain import Blockchain

blockchain = Blockchain()

wallet1 = Wallet()
wallet2 = Wallet()

blockchain.register_wallet(wallet1)
blockchain.register_wallet(wallet2)

print(blockchain.get_all_wallets())