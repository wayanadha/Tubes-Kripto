from core.wallet import Wallet
from core.transaction import Transaction
import json


wallet = Wallet()


tx = Transaction(
    sender=wallet.address,
    receiver="ADDR_SELLER",
    amount=100,
    nonce=1
)


tx.sign_transaction(wallet)


print("=== TRANSACTION DATA ===")

print(json.dumps(
    tx.to_dict(),
    indent=4
))


print("\n=== SIGNATURE VERIFICATION ===")

if tx.verify_signature():
    print("VALID")
else:
    print("INVALID")