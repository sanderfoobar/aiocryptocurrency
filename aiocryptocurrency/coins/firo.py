import json
from datetime import datetime
from typing import Union, Optional

import aiohttp

from aiocryptocurrency import TransactionSet, Transaction
from aiocryptocurrency.coins import Coin


class Firo(Coin):
    def __init__(self):
        super(Firo, self).__init__()
        self.host = '127.0.0.1'
        self.port = 8888
        self.basic_auth: Optional[tuple[str]] = None
        self.url = None

    async def send(self, address: str, amount: float) -> str:
        """returns txid"""
        if amount <= 0:
            raise Exception("amount cannot be zero or less")

        data = {
            "method": "sendtoaddress",
            "params": [address, amount]
        }

        blob = await self._make_request(data=data)
        return blob['result']

    async def create_address(self) -> dict:
        """returns an address"""
        data = {
            "method": "getnewaddress"
        }
        blob = await self._make_request(data=data)

        address = blob['result']
        if address is None or not isinstance(address, str):
            raise Exception("Invalid result")

        return {
            "address": address
        }

    async def tx_details(self, txid: str):
        if not isinstance(txid, str) or not txid:
            raise Exception("bad address")

        data = {
            "method": "gettransaction",
            "params": [txid]
        }

        blob = await self._make_request(data=data)
        return blob['result']

    async def list_txs(self, address: str, minimum_confirmations: int = 3) -> Optional[TransactionSet]:
        txset = TransactionSet()
        if not isinstance(address, str) or not address:
            raise Exception("bad address")

        results = await self._make_request(data={
            "method": "listreceivedbyaddress",
            "params": [minimum_confirmations]
        })

        if not isinstance(results.get('result'), list):
            return txset

        try:
            result = [r for r in results['result'] if r['address'] == address][0]
        except Exception as ex:
            return txset

        for txid in result.get('txids', []):
            # fetch tx details
            tx = await self.tx_details(txid)

            # fetch blockheight
            tx['blockheight'] = await self.blockheight(tx['blockhash'])
            date = datetime.fromtimestamp(tx['blocktime'])

            txset.add(Transaction(amount=tx['amount'],
                                  txid=tx['txid'],
                                  date=date,
                                  blockheight=tx['blockheight'],
                                  direction='in',
                                  confirmations=tx['confirmations']))

        return txset

    async def blockheight(self, blockhash: str) -> int:
        """blockhash -> blockheight"""
        if not isinstance(blockhash, str) or not blockhash:
            raise Exception("bad address")

        data = {
            "method": "getblock",
            "params": [blockhash]
        }
        blob = await self._make_request(data=data)

        height = blob['result'].get('height', 0)
        return height

    async def _generate_url(self) -> None:
        self.url = f'http://{self.host}:{self.port}/'

    async def _make_request(self, data: dict = None) -> dict:
        await self._generate_url()

        opts = {
            "headers": {
                "User-Agent": self.user_agent
            }
        }

        if self.basic_auth:
            opts['auth'] = await self._make_basic_auth()

        async with aiohttp.ClientSession(**opts) as session:
            async with session.post(self.url, json=data) as resp:
                if resp.status == 401:
                    raise Exception("Unauthorized")
                blob = await resp.json()
                if 'result' not in blob:
                    if blob:
                        blob = json.dumps(blob, indent=4, sort_keys=True)
                    raise Exception(f"Invalid response: {blob}")
                return blob
