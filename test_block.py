from core.block import Block


block = Block(
    index=1,
    transactions=[
        {
            "from": "ADDR_A",
            "to": "ADDR_B",
            "amount": 100
        }
    ],
    previous_hash="000000"
)


print(block.to_dict())