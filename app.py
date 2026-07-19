from flask import Flask, jsonify, request

from core.escrow import Escrow
from core.wallet import Wallet
from core.transaction import Transaction
from core.blockchain import Blockchain

from core.storage import (
    load_json,
    save_json,
    WALLET_FILE
)

from core.storage import (
    save_wallets,
    load_wallets,
    save_blockchain,
    load_blockchain,
    save_escrows,
    load_escrows
)

app = Flask(__name__)

# ===================================
# INIT BLOCKCHAIN
# ===================================

chain_data = load_blockchain()

if len(chain_data) > 0:

    blockchain = Blockchain(create_genesis=False)
    blockchain.load_chain(chain_data)

else:

    blockchain = Blockchain()

# ===================================
# LOAD WALLET
# ===================================

stored_wallets = load_wallets()

print("Wallet ditemukan :", len(stored_wallets))

blockchain.load_wallets(stored_wallets)

# ===================================
# LOAD ESCROW
# ===================================

escrows = {}

escrow_data = load_escrows()

for item in escrow_data:

    escrow = Escrow.from_dict(
        item,
        blockchain
    )

    escrows[escrow.escrow_id] = escrow

# ===================================
# HOME
# ===================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
    "success": True,
        "message": "MiniCrypto Backend Running",
        "data": {
            "project": "MiniCrypto Blockchain",
            "status": "running"
        }
    })


# ===================================
# CREATE WALLET
# ===================================

@app.route("/wallet/create", methods=["POST"])
def create_wallet():

    data = request.get_json(silent=True) or {}

    wallet = Wallet(
        name=data.get("name", "Unknown")
    )

    blockchain.register_wallet(wallet)

    save_wallets(
        blockchain.wallets.values()
    )
    
    save_blockchain(blockchain)

    return jsonify({
        "success": True,
        "message":"Wallet berhasil dibuat",
        "data":wallet.get_wallet_info()
    }),201


# ===================================
# GET ALL WALLETS
# ===================================

@app.route("/wallets", methods=["GET"])
def get_wallets():

    wallets = blockchain.get_all_wallets()

    return jsonify({
        "success": True,
        "message": "Daftar wallet berhasil diambil",
        "total": len(wallets),
        "data": wallets
    }), 200


# ===================================
# BLOCKCHAIN
# ===================================

@app.route("/blockchain", methods=["GET"])
def get_blockchain():

    return jsonify({
        "success":True,
        "message":"Blockchain berhasil diambil",
        "length":len(blockchain.chain),
        "data":blockchain.to_dict()
    })

# ===================================
# VERIFY
# ===================================

@app.route("/verify", methods=["GET"])
def verify_chain():

    return jsonify({
        "success":True,
        "message":"Blockchain valid",
        "data":{
            "valid":blockchain.is_chain_valid()
        }
    })

# ===================================
# CREATE TRANSACTION
# ===================================

@app.route("/transaction/create", methods=["POST"])
def create_transaction():

    data = request.get_json()

    sender = blockchain.get_wallet(
        data["sender"]
    )

    receiver = blockchain.get_wallet(
        data["receiver"]
    )

    if sender is None:
        return jsonify({
            "error": "Sender tidak ditemukan"
        }), 404

    if receiver is None:
        return jsonify({
            "error": "Receiver tidak ditemukan"
        }), 404

    tx = Transaction(
        sender=sender.address,
        receiver=receiver.address,
        amount=data["amount"],
        nonce=sender.nonce
    )

    tx.sign_transaction(sender)

    blockchain.add_transaction(tx)

    return jsonify({
        "message": "Transaction berhasil ditambahkan ke mempool",
        "transaction": tx.to_dict()
    })

    return jsonify({
        "success":False,
        "message":str(e)
    }),400

# ===================================
# GET PENDING TRANSACTION
# ===================================

@app.route("/pending", methods=["GET"])
def get_pending():

    return jsonify({
        "total": len(
            blockchain.pending_transactions
        ),
        "transactions":
            blockchain.pending_transactions
    })

# ===================================
# MINE
# ===================================

@app.route("/mine", methods=["POST"])
def mine():

    data = request.get_json()

    miner = blockchain.get_wallet(
        data["miner"]
    )

    if miner is None:

        return jsonify({
            "error": "Miner tidak ditemukan"
        }), 404

    result = blockchain.mine_pending_transactions(
        miner.address
    )

    if result is False:

        return jsonify({
            "message": "Tidak ada transaksi"
        })

    return jsonify({
        "success":True,
        "message":"Block berhasil ditambang",
        "data":{
            "height":len(blockchain.chain),
            "pending_transaction":len(blockchain.pending_transactions)
        }
    })

# ===================================
# CREATE ESCROW
# ===================================

@app.route("/escrow/create", methods=["POST"])
def create_escrow():

    data = request.get_json()

    buyer = blockchain.get_wallet(data["buyer"])
    seller = blockchain.get_wallet(data["seller"])
    arbiter = blockchain.get_wallet(data["arbiter"])

    if buyer is None:
        return jsonify({"error": "Buyer tidak ditemukan"}), 404

    if seller is None:
        return jsonify({"error": "Seller tidak ditemukan"}), 404

    if arbiter is None:
        return jsonify({"error": "Arbiter tidak ditemukan"}), 404

    if buyer.balance < data["amount"]:
        return jsonify({"error": "Saldo buyer tidak cukup"}), 400

    buyer.decrease_balance(data["amount"])

    escrow = Escrow(
        buyer,
        seller,
        arbiter,
        data["amount"]
    )

    escrows[escrow.escrow_id] = escrow
    save_escrows(escrows)
    save_wallets(blockchain.wallets.values())

    return jsonify({
        "success":True,
        "message": "Escrow berhasil dibuat",
        "data":escrow.to_dict()
    }),201

# ===================================
# RELEASE ESCROW
# ===================================

@app.route("/escrow/release", methods=["POST"])
def release_escrow():

    data = request.get_json()

    escrow = escrows.get(data["escrow_id"])

    if escrow is None:
        return jsonify({
            "error": "Escrow tidak ditemukan"
        }), 404

    try:
        escrow.release()

        save_escrows(escrows)
        save_wallets(blockchain.wallets.values())

        return jsonify({
            "success":True,
            "message":"Dana berhasil dilepas",
            "data":escrow.to_dict()
        })

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

# ===================================
# REFUND ESCROW
# ===================================

@app.route("/escrow/refund", methods=["POST"])
def refund_escrow():

    data = request.get_json()

    escrow = escrows.get(
        data["escrow_id"]
    )

    if escrow is None:

        return jsonify({
            "error":"Escrow tidak ditemukan"
        }),404

    try:    
        escrow.refund()
        save_escrows(escrows)
        save_wallets(blockchain.wallets.values())

        return jsonify({
            "success":True,
            "message":"Dana berhasil dikembalikan",
            "data":escrow.to_dict()
        })

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

# ===================================
# GET ESCROW
# ===================================

@app.route("/escrow/<escrow_id>", methods=["GET"])
def get_escrow(escrow_id):

    escrow = escrows.get(
        escrow_id
    )

    if escrow is None:

        return jsonify({
            "error":"Escrow tidak ditemukan"
        }),404

    return jsonify(
        escrow.to_dict()
    )

# ===================================
# SHIP ESCROW
# ===================================

@app.route("/escrow/ship", methods=["POST"])
def ship_escrow():

    data = request.get_json()

    escrow = escrows.get(
        data["escrow_id"]
    )

    if escrow is None:
        return jsonify({
            "error": "Escrow tidak ditemukan"
        }), 404

    try:

        escrow.ship()

        save_escrows(
            escrows
        )

        return jsonify({
            "message": "Barang berhasil dikirim",
            "escrow": escrow.to_dict()
        })

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

# ===================================
# MEMPOOL
# ===================================

@app.route("/mempool", methods=["GET"])
def get_mempool():

    return jsonify({
        "success": True,
        "message": "Daftar transaksi yang belum ditambang",
        "data": blockchain.pending_transactions
    })

# ===================================
# VERIFY TRANSACTION
# ===================================

@app.route("/verify_tx", methods=["POST"])
def verify_transaction():

    data = request.get_json()

    tx_id = data.get("tx_id")

    transaction = blockchain.transactions.get(tx_id)

    if transaction is None:

        return jsonify({
            "success": False,
            "message": "Transaction tidak ditemukan"
        }), 404

    valid = transaction.verify_signature()

    return jsonify({
        "success": True,
        "message": "Verifikasi transaksi berhasil",
        "data": {
            "tx_id": tx_id,
            "valid": valid
        }
    })

# ===================================
# RUN
# ===================================

if __name__ == "__main__":

    app.run(
        debug=True
    )