from typing import List, Union
from datetime import datetime


class Transaction:
    def __init__(self, amount: float, txid: str, direction: str, date: datetime = None, confirmations: int = 0, blockheight: int = None):
        self.amount: float = amount
        self.txid: str = txid
        self.date: datetime = date
        self.blockheight: int = blockheight
        self.direction: str = direction
        self.confirmations: int = confirmations


class TransactionSet:
    def __init__(self):
        self._transactions: list[Transaction] = []
        self._idx = 0

    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        if self._idx < len(self._transactions):
            tx = self._transactions[self._idx]
            self._idx += 1
            return tx
        raise StopIteration

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, txid: str) -> Transaction:
        for transaction in self._transactions:
            if transaction.txid == txid:
                return transaction

    def add(self, item: Transaction):
        self._transactions.append(item)

    def sum(self) -> float:
        try:
            return sum(tx.amount for tx in self._transactions)
        except Exception as ex:
            return 0.0
