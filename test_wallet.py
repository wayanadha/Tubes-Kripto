from core.wallet import Wallet
import json

buyer = Wallet()
seller = Wallet()

print("=== BUYER ===")
print(json.dumps(
    buyer.get_wallet_info(),
    indent=4
))

print("\n=== SELLER ===")
print(json.dumps(
    seller.get_wallet_info(),
    indent=4
))

print("\n========================")
print("TRANSFER 250 COIN")
print("========================")

buyer.transfer(
    receiver=seller,
    amount=250
)

print("\nBuyer Balance :", buyer.get_balance())
print("Seller Balance :", seller.get_balance())
print("Buyer Nonce :", buyer.nonce)

print("\n========================")
print("TEST SALDO TIDAK CUKUP")
print("========================")

try:

    buyer.transfer(
        receiver=seller,
        amount=5000
    )

except ValueError as e:

    print("Error :", e)