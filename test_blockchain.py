from core.blockchain import Blockchain
import json


blockchain = Blockchain()


transactions = [
    {
        "from": "ADDR_A",
        "to": "ADDR_B",
        "amount": 100
    },
    {
        "from": "ADDR_B",
        "to": "ADDR_C",
        "amount": 50
    }
]


blockchain.mine_pending_transactions(
    miner_address="ADDR_MINER",
    transactions=transactions
)


print(json.dumps(
    blockchain.to_dict(),
    indent=4
))


print("\nBlockchain Valid:")
print(blockchain.is_chain_valid())