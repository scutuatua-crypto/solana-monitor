#!/usr/bin/env python3
import asyncio
import aiohttp
from datetime import datetime

WALLET_ADDRESS = "4b2Zkq2Lvt15v9PXeNmbkwMZbDfUXbgdmXd4x2j6cWxX"
POLL_INTERVAL = 15

class C:
    RESET, GREEN, RED, DIM, CYAN = "\033[0m", "\033[92m", "\033[91m", "\033[2m", "\033[96m"

async def fetch_sol(session):
    url = "https://api.mainnet-beta.solana.com"
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [WALLET_ADDRESS]}
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()
            return data["result"]["value"] / 1_000_000_000
    except Exception as e:
        print(f"Error: {e}")
    return None

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            sol = await fetch_sol(session)
            print(f"{C.CYAN}--- SOLANA MONITOR ---{C.RESET}")
            if sol is not None:
                print(f"{C.GREEN}Balance: {sol} SOL{C.RESET}")
            else:
                print(f"{C.RED}Cannot fetch balance{C.RESET}")
            print(f"{C.DIM}Update: {datetime.now().strftime('%H:%M:%S')}{C.RESET}")
            await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
