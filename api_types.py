class Transaction:

    def __init__(
            self,
            id: int,
            type: str,
            amount: float,
            payment_system: str,
            currency: str,
            address: str,
            payment_card: str,
            status: str
    ):
        self.id: int = id
        self.type: str = type
        self.amount: float = amount
        self.payment_system: str = payment_system
        self.currency: str = currency
        self.address: str = address
        self.payment_card: str = payment_card
        self.status: str = status


class AccountInfo:

    def __init__(self,
                 balance_rub,
                 balance_usd,
                 balance_uah,
                 balance_on_hold_rub,
                 balance_on_hold_usd,
                 balance_on_hold_uah,
                 lock_withdrawal, lock_account):
        self.balance_rub = round(float(balance_rub), 2)
        self.balance_usd = round(float(balance_usd), 2)
        self.balance_uah = round(float(balance_uah), 2)
        self.balance_on_hold_rub = round(float(balance_on_hold_rub), 2)
        self.balance_on_hold_usd = round(float(balance_on_hold_usd), 2)
        self.balance_on_hold_uah = round(float(balance_on_hold_uah), 2)
        self.lock_withdrawal = int(lock_withdrawal)
        self.lock_account = int(lock_account)
