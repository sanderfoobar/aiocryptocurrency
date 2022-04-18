import json
from operator import attrgetter
from typing import List, Union
from datetime import datetime

from dateutil.parser import parse as dateutil_parse


class Transaction:
    def __init__(self, amount: float, txid: str, direction: str, date: Union[datetime, str], confirmations: int = 0, blockheight: int = None):
        self.amount: float = amount
        self.txid: str = txid
        if isinstance(date, str):
            self.date = dateutil_parse(date)
        else:
            self.date: datetime = date
        self.blockheight: int = blockheight
        self.direction: str = direction
        self.confirmations: int = confirmations

    @classmethod
    def from_json(cls, data: dict):
        return Transaction(
            data['amount'],
            data['txid'],
            datetime.strptime(data['d1ate'], '%Y-%m-%d %H:%M'),
            data['blockheight'],
            data['direction'],
            data['confirmations']
        )

    def json(self):
        return {
            'amount': self.amount,
            'txid': self.txid,
            'date': self.date.strftime('%Y-%m-%d %H:%M'),
            'blockheight': self.blockheight,
            'direction': self.direction,
            'confirmations': self.confirmations
        }


class TransactionSet:
    def __init__(self):
        self._transactions: list[Transaction] = []
        self._idx = 0

    def serialize(self) -> str:
        data = [tx.json() for tx in self._transactions]
        if not data:
            return json.dumps([])

        return json.dumps(data, sort_keys=True, indent=True)

    @classmethod
    def from_json(cls, val: dict):
        cls = TransactionSet()
        if not val or not isinstance(val, list):
            return cls

        for r in val:
            tx = Transaction(**r)
            cls.add(tx)
        return cls

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

    def __getitem__(self, txid: str) -> Optional[Transaction]:
        for transaction in self._transactions:
            if transaction.txid == txid:
                return transaction

    def __add__(self, other: 'TransactionSet'):
        ts = TransactionSet()
        ts._transactions = self._transactions
        for tx in other:
            ts.add(tx)
        ts.sort()
        return ts

    def sort(self):
        self._transactions.sort(key=lambda tx: tx.date, reverse=True)

    def add(self, item: Transaction):
        self._transactions.append(item)
        self.sort()

    def filter(self, direction='in') -> 'TransactionSet':
        txset = TransactionSet()
        txset._transactions = [tx for tx in self._transactions if tx.direction == direction]
        return txset

    def sum(self, direction='in') -> float:
        try:
            return sum(tx.amount for tx in self._transactions if tx.direction == direction)
        except Exception as ex:
            return 0.0
