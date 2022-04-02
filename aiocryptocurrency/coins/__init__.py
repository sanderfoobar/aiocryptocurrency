import re
import os
from typing import Union, Optional

import aiohttp

from aiocryptocurrency import TransactionSet, Transaction

SUPPORTED_COINS = {
        "firo": "firo",
        "monero": "xmr",
        "wownero": "wow"
}


class Coin:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 0
        self.basic_auth: Optional[tuple[str]] = None
        self.verify_tls = False
        self.user_agent = "aiocryptocurrency"

    async def send(self, address: str, amount: float):
        raise NotImplemented()

    async def create_address(self, *args, **kwargs):
        raise NotImplemented()

    async def list_txs(self, *args, **kwargs) -> TransactionSet:
        raise NotImplemented()

    async def _generate_url(self):
        raise NotImplemented()

    async def _make_basic_auth(self):
        return aiohttp.BasicAuth(
            login=self.basic_auth[0],
            password=self.basic_auth[1]
        )
