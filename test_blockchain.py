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


print("=== BLOCKCHAIN ===")

print(json.dumps(
    blockchain.to_dict(),
    indent=4
))


print("\n=== VALIDATION ===")
print(blockchain.is_chain_valid())

print("\n=== TAMPERING BLOCK ===")

blockchain.chain[1].transactions[0]["amount"] = 999

print(json.dumps(
    blockchain.to_dict(),
    indent=4
))

print("\n=== VALIDATION AFTER TAMPER ===")
print(blockchain.is_chain_valid())