import asyncio
import logging
import os

async def coins():
    while True:
        os.system("bash -c 'python3 CryptoCoins.py &'")
        await asyncio.sleep(60)

async def news():
    while True:
        os.system("bash -c 'python3 CryptoNews.py &'")
        await asyncio.sleep(2 * 3600) 

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(coins())
    asyncio.ensure_future(news())
    loop.run_forever()  