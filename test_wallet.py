from core.wallet import Wallet
import json


wallet = Wallet()

print("=== WALLET INFO ===")
print(json.dumps(
    wallet.get_wallet_info(),
    indent=4
))

print("\n=== TEST BALANCE ===")
print("Balance Awal :", wallet.get_balance())

wallet.decrease_balance(200)

print("Setelah Kurang 200 :", wallet.get_balance())

wallet.increase_balance(500)

print("Setelah Tambah 500 :", wallet.get_balance())

wallet.increase_nonce()

print("Nonce :", wallet.nonce)