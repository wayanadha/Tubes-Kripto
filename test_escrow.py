import json

from core.wallet import Wallet
from core.escrow import Escrow

buyer = Wallet()
seller = Wallet()
arbiter = Wallet()

buyer.decrease_balance(300)

escrow = Escrow(
    buyer=buyer,
    seller=seller,
    arbiter=arbiter,
    amount=300
)

print("\n===== ESCROW CREATED =====")

print(json.dumps(
    escrow.to_dict(),
    indent=4
))

print("\nBuyer Balance :", buyer.balance)
print("Seller Balance :", seller.balance)

print("\n===== SELLER SHIPS =====")

escrow.ship()

print("Status :", escrow.status)

print("\n===== BUYER RELEASE =====")

escrow.release()

print("Status :", escrow.status)

print("Buyer :", buyer.balance)
print("Seller :", seller.balance)

print("\n===== LOG =====")

print(json.dumps(
    escrow.logs,
    indent=4
))