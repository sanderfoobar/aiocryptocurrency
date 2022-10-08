from datetime import datetime

import aiohttp

from aiocryptocurrency import Transaction, TransactionSet
from aiocryptocurrency.coins import Coin


class Nero(Coin):
    # @TODO: support authentication
    def __init__(self):
        super(Nero, self).__init__()
        self.host = "127.0.0.1"
        self.url = None
        self._div = None

    async def send(self, address: str, amount: float) -> str:
        """returns txid"""
        await self._generate_url()
        if amount <= 0:
            raise Exception("amount cannot be zero or less")

        amount_atomic = int(amount * self._div)

        async with aiohttp.ClientSession() as session:
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "transfer",
                "params": {
                    "destinations": [{
                        "amount": amount_atomic,
                        "address": address
                    }]
                }
            }

            async with session.post(self.url, json=data) as resp:
                blob = await resp.json()
                if 'result' not in blob:
                    raise Exception("Invalid response")
                return blob['result']['tx_hash']

    async def create_address(self) -> dict:
        """returns both payment_id and address"""
        await self._generate_url()

        async with aiohttp.ClientSession() as session:
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "make_integrated_address"
            }

            async with session.get(self.url, json=data) as resp:
                blob = await resp.json()
                if 'result' not in blob:
                    raise Exception("Invalid response")

                res = blob['result']
                if "integrated_address" not in res or 'payment_id' not in res:
                    raise Exception("Invalid result response")

                return {
                    "address": res['integrated_address'],
                    "payment_id": res['payment_id']
                }

    async def list_txs(self, address: str = None, payment_id: str = None, *args, **kwargs) -> TransactionSet:
        txset = TransactionSet()
        await self._generate_url()

        height = 0
        async with aiohttp.ClientSession() as session:
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_height",
            }

            async with session.get(self.url, json=data) as resp:
                blob = await resp.json()
                height = blob.get('result', {}).get('height', 0)

        if not height:
            logging.error(f"could not get height at {self.url}")
            return txset

        async with aiohttp.ClientSession() as session:
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_payments",
                "params": {
                    "payment_id": payment_id
                }
            }

            async with session.get(self.url, json=data) as resp:
                blob = await resp.json()
                if 'result' not in blob:
                    raise Exception(f"Invalid response; {blob}")

                res = blob['result']
                payments = res.get('payments', [])
                if not payments:
                    return txset

                transactions = payments
                for transaction in transactions:
                    amount = float(transaction['amount']) / self._div

                    tx = Transaction(amount=amount,
                                     txid=transaction['tx_hash'],
                                     date=datetime.now(),
                                     blockheight=transaction['block_height'],
                                     direction='in',
                                     confirmations=(height - transaction['block_height']))
                    txset.add(tx)

        return txset

    async def _generate_url(self) -> None:
        self.url = f"http://{self.host}:{self.port}/json_rpc"


class Wownero(Nero):
    def __init__(self):
        # ./wownero-wallet-rpc --rpc-bind-port 45678 --disable-rpc-login --wallet-file /home/user/wallet_name.keys --password
        super(Wownero, self).__init__()
        self.port = 45678
        self._div = 1e11


class Monero(Nero):
    def __init__(self):
        super(Monero, self).__init__()
        self.port = 34567
        self._div = 1e12
