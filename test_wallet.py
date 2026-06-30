from core.wallet import Wallet
import json


wallet = Wallet()


wallet_info = wallet.get_wallet_info()


print("=== WALLET INFORMATION ===")

print(json.dumps(
    wallet_info,
    indent=4
))


print("\n=== PRIVATE KEY ===")
print(wallet.get_private_key_pem())