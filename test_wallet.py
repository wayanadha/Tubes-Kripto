from core.wallet import Wallet


wallet = Wallet()


print("PRIVATE KEY")
print(wallet.get_private_key_pem())


print("PUBLIC KEY")
print(wallet.get_public_key_pem())