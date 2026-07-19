import uuid
import time


class Escrow:

    STATUS_FUNDED = "FUNDED"
    STATUS_SHIPPED = "SHIPPED"
    STATUS_RELEASED = "RELEASED"
    STATUS_REFUNDED = "REFUNDED"
    STATUS_DISPUTE = "DISPUTE"

    def __init__(self, buyer, seller, arbiter, amount):

        self.escrow_id = str(uuid.uuid4())

        self.buyer = buyer
        self.seller = seller
        self.arbiter = arbiter

        self.amount = amount

        self.status = self.STATUS_FUNDED

        self.created_at = int(time.time())

        self.logs = []

        self.add_log("Escrow created")
        self.add_log("Funds locked")

    # ==========================
    # LOG
    # ==========================

    def add_log(self, message):

        self.logs.append({
            "time": int(time.time()),
            "message": message
        })

    # ==========================
    # SHIP
    # ==========================

    def ship(self):

        if self.status != self.STATUS_FUNDED:
            raise ValueError("Barang tidak bisa dikirim.")

        self.status = self.STATUS_SHIPPED

        self.add_log("Seller shipped item")

    # ==========================
    # RELEASE
    # ==========================

    def release(self):

        if self.status != self.STATUS_SHIPPED:
            raise ValueError("Barang belum dikirim.")

        self.status = self.STATUS_RELEASED

        self.add_log("Buyer confirmed")

        self.seller.increase_balance(
            self.amount
        )

        self.add_log(
            f"{self.amount} coin released to seller"
        )

    # ==========================
    # REFUND
    # ==========================

    def refund(self):

        if self.status not in [
            self.STATUS_FUNDED,
            self.STATUS_SHIPPED
        ]:

            raise ValueError(
                "Refund tidak dapat dilakukan."
            )

        self.status = self.STATUS_REFUNDED

        self.buyer.increase_balance(
            self.amount
        )

        self.add_log(
            f"{self.amount} coin refunded"
        )

    # ==========================
    # DISPUTE
    # ==========================

    def dispute(self):

        if self.status not in [
            self.STATUS_FUNDED,
            self.STATUS_SHIPPED
        ]:

            raise ValueError(
                "Dispute tidak dapat dilakukan."
            )

        self.status = self.STATUS_DISPUTE

        self.add_log("Dispute opened")

    # ==========================
    # ARBITER DECISION
    # ==========================

    def resolve(self, decision):

        if self.status != self.STATUS_DISPUTE:
            raise ValueError(
                "Tidak ada dispute."
            )

        if decision == "release":

            self.seller.increase_balance(
                self.amount
            )

            self.status = self.STATUS_RELEASED

            self.add_log(
                "Arbiter released fund"
            )

        elif decision == "refund":

            self.buyer.increase_balance(
                self.amount
            )

            self.status = self.STATUS_REFUNDED

            self.add_log(
                "Arbiter refunded buyer"
            )

        else:

            raise ValueError(
                "Keputusan arbiter tidak valid."
            )

    # ==========================
    # JSON
    # ==========================

    def to_dict(self):

        return {

            "escrow_id": self.escrow_id,

            "buyer": self.buyer.address,

            "seller": self.seller.address,

            "arbiter": self.arbiter.address,

            "amount": self.amount,

            "status": self.status,

            "created_at": self.created_at,

            "logs": self.logs

        }

    @classmethod
    def from_dict(cls, data, blockchain):

        buyer = blockchain.get_wallet(
            data["buyer"]
        )

        seller = blockchain.get_wallet(
            data["seller"]
        )

        arbiter = blockchain.get_wallet(
            data["arbiter"]
        )

        escrow = cls(
            buyer,
            seller,
            arbiter,
            data["amount"]
        )

        escrow.escrow_id = data["escrow_id"]
        escrow.status = data["status"]
        escrow.logs = data["logs"]
        escrow.created_at = data["created_at"]

        return escrow

