def __init__(self):
    self.private_key = self.generate_private_key()
    self.public_key = self.generate_public_key()
    self.address = self.generate_address()