class Transaction:

    def __init__(
            self,
            id: int,
            type: str,
            amount: float,
            paymentSystem: str,
            currency: str,
            address: str,
            paymentCard: str,
            status: str
    ):
        self.id: int = id
        self.type: str = type
        self.amount: float = amount
        self.paymentSystem: str = paymentSystem
        self.currency: str = currency
        self.address: str = address
        self.paymentCard: str = paymentCard
        self.status: str = status
