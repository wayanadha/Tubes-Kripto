from core.wallet import Wallet
from core.transaction import Transaction


wallet = Wallet()


tx = Transaction(
    sender=wallet.address,
    receiver="ADDR_SELLER",
    amount=100,
    nonce=1
)


tx.sign_transaction(wallet)


print(tx.to_dict())


print("\nSignature Status:")
print(tx.verify_signature())