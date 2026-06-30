from core.block import Block
import json

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


print(json.dumps(
    block.to_dict(),
    indent=4
))

print("\nBlock Hash:")
print(block.hash)


# Test perubahan data
block.transactions[0]["amount"] = 999

print("\nHash Setelah Data Diubah:")
print(block.calculate_hash())