from core.transaction import Transaction


tx = Transaction(
    sender="ADDR_BUYER",
    receiver="ADDR_SELLER",
    amount=100,
    nonce=1
)


print(tx.to_dict())