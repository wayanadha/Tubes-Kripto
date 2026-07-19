import json
import os

from core.wallet import Wallet

# ==========================
# Folder & File
# ==========================

DATA_FOLDER = "data"

WALLET_FILE = os.path.join(DATA_FOLDER, "wallets.json")
BLOCKCHAIN_FILE = os.path.join(DATA_FOLDER, "blockchain.json")
ESCROW_FILE = os.path.join(DATA_FOLDER, "escrows.json")


# ==========================
# Generic JSON
# ==========================

def load_json(path):

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:

        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_json(path, data):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==========================
# Wallet Storage
# ==========================

def save_wallets(wallets):

    wallet_list = []

    for wallet in wallets:
        wallet_list.append(
            wallet.to_storage_dict()
        )

    save_json(
        WALLET_FILE,
        wallet_list
    )


def load_wallets():

    wallet_data = load_json(
        WALLET_FILE
    )

    wallets = []

    for item in wallet_data:

        wallets.append(
            Wallet.from_storage_dict(item)
        )

    return wallets


# ==========================
# Blockchain Storage
# ==========================

def save_blockchain(blockchain):

    save_json(
        BLOCKCHAIN_FILE,
        blockchain.to_dict()
    )


def load_blockchain():

    return load_json(
        BLOCKCHAIN_FILE
    )


# ==========================
# Escrow Storage
# ==========================

def save_escrows(escrows):

    escrow_list = []

    for escrow in escrows.values():

        escrow_list.append(
            escrow.to_dict()
        )

    save_json(
        ESCROW_FILE,
        escrow_list
    )


def load_escrows():

    return load_json(
        ESCROW_FILE
    )