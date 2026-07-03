from core.blockchain import Blockchain
import json


blockchain = Blockchain()

blockchain.add_block(
    [
        {
            "from": "ADDR_A",
            "to": "ADDR_B",
            "amount": 100
        }
    ]
)

blockchain.add_block(
    [
        {
            "from": "ADDR_B",
            "to": "ADDR_C",
            "amount": 50
        }
    ]
)

print("\n=== BLOCKCHAIN ===\n")

print(
    json.dumps(
        blockchain.to_dict(),
        indent=4
    )
)

print("\n=== VALID ===")
print(blockchain.is_chain_valid())