# aiocryptocurrency

Provides a single abstract interface for managing the funds of various 
cryptocurrency wallets via their RPC interfaces.

## Support for:

This project currently supports the following coins:

- Monero
- Wownero
- Firo

## Quick start

```text
pip install aiocryptocurrency
```

Example using [Firo](https://firo.org/) (the API is the same for other coins).

```python3
import asyncio


from aiocryptocurrency.coins.nero import Wownero, Monero
from aiocryptocurrency.coins.firo import Firo


async def main():
    # ./firod -testnet -rpcbind=127.0.0.1 -rpcallowip=127.0.0.1 -rpcport=18888 -rpcuser=admin -rpcpassword=admin
    firo = Firo()
    firo.port = 18888
    firo.basic_auth = ('admin', 'admin')

    # create a new receiving address
    blob = await firo.create_address()
    address = blob['address']

    # # list incoming txs
    txs = await firo.list_txs(address)
    for tx in txs:
        print(tx.txid)

    # send payment
    dest = 'TRwRAjxfAVKVZYQGdmskZRDSBw9E5YqjC8'
    amount = 0.05
    txid = await firo.send(dest, amount)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
