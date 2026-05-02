#!/usr/bin/env python3
“””
Solana Wallet Monitor + Reward System
Powered by Solscan API v2
“””

import asyncio
import aiohttp
import os
from datetime import datetime
from typing import Optional

# ─── CONFIG ───────────────────────────────────────────────

WALLET_ADDRESS = “4b2Zkq2Lvt15v9PXeNmbkwMZbDfUXbgdmXd4x2j6cWxX”
SOLSCAN_API_KEY = os.environ.get("SOLSCAN_API_KEY")
SOLSCAN_BASE    = “https://pro-api.solscan.io/v2.0”
RPC_URL         = “https://api.mainnet-beta.solana.com”  # fallback

POLL_INTERVAL = 15  # วินาที

# Reward tiers

REWARD_TIERS = [
{“min”: 0,    “max”: 1,    “label”: “🥉 Bronze Holder”},
{“min”: 1,    “max”: 10,   “label”: “🥈 Silver Holder”},
{“min”: 10,   “max”: 100,  “label”: “🥇 Gold Holder”},
{“min”: 100,  “max”: 1000, “label”: “💎 Platinum Holder”},
{“min”: 1000, “max”: 9e18, “label”: “👑 Diamond Holder”},
]

# ─── COLORS ───────────────────────────────────────────────

class C:
RESET   = “\033[0m”
BOLD    = “\033[1m”
GREEN   = “\033[92m”
YELLOW  = “\033[93m”
CYAN    = “\033[96m”
RED     = “\033[91m”
MAGENTA = “\033[95m”
WHITE   = “\033[97m”
DIM     = “\033[2m”
BLUE    = “\033[94m”

def now(): return datetime.now().strftime(”%H:%M:%S”)
def lamports_to_sol(v): return v / 1_000_000_000

def get_tier(sol: float) -> str:
for t in REWARD_TIERS:
if t[“min”] <= sol < t[“max”]:
return t[“label”]
return “👑 Diamond Holder”

def print_header():
os.system(“clear”)
print(f”{C.CYAN}{C.BOLD}”)
print(“╔══════════════════════════════════════════════════════════╗”)
print(“║      🌊  SOLANA MONITOR + REWARDS  •  Solscan v2  🌊      ║”)
print(“╚══════════════════════════════════════════════════════════╝”)
print(f”{C.RESET}”)
short = WALLET_ADDRESS[:8] + “…” + WALLET_ADDRESS[-8:]
print(f”  {C.DIM}Wallet : {C.WHITE}{short}{C.RESET}”)
print(f”  {C.DIM}Updated: {C.WHITE}{now()}{C.RESET}  {C.DIM}(every {POLL_INTERVAL}s){C.RESET}”)
print()

# ─── SOLSCAN API ──────────────────────────────────────────

async def solscan_get(session: aiohttp.ClientSession, path: str, params: dict = {}):
headers = {“token”: SOLSCAN_API_KEY}
url = f”{SOLSCAN_BASE}{path}”
try:
async with session.get(url, headers=headers, params=params,
timeout=aiohttp.ClientTimeout(total=15)) as resp:
data = await resp.json()
if data.get(“success”):
return data.get(“data”)
except Exception:
pass
return None

# ─── FALLBACK RPC ─────────────────────────────────────────

async def rpc_get_sol(session: aiohttp.ClientSession) -> Optional[float]:
payload = {“jsonrpc”: “2.0”, “id”: 1, “method”: “getBalance”,
“params”: [WALLET_ADDRESS]}
try:
async with session.post(RPC_URL, json=payload,
timeout=aiohttp.ClientTimeout(total=10)) as resp:
data = await resp.json()
val = data.get(“result”, {}).get(“value”)
return lamports_to_sol(val) if val is not None else None
except Exception:
return None

# ─── FETCH DATA ───────────────────────────────────────────

async def fetch_sol(session) -> Optional[float]:
data = await solscan_get(session, “/account/balance”,
{“address”: WALLET_ADDRESS})
if data and “lamports” in data:
return lamports_to_sol(data[“lamports”])
return await rpc_get_sol(session)

async def fetch_tokens(session) -> list:
data = await solscan_get(session, “/account/token-accounts”,
{“address”: WALLET_ADDRESS, “type”: “token”,
“page”: 1, “page_size”: 20})
tokens = []
if data:
items = data if isinstance(data, list) else data.get(“items”, [])
for item in items:
dec = item.get(“decimals”, 0)
amount = float(item.get(“amount”, 0)) / (10 ** dec)
if amount > 0:
tokens.append({
“symbol”: item.get(“token_symbol”) or “???”,
“amount”: amount,
“mint”:   item.get(“token_address”) or “”,
“usd”:    float(item.get(“value”) or 0),
})
return tokens

async def fetch_transactions(session, limit=5) -> list:
data = await solscan_get(session, “/account/transactions”,
{“address”: WALLET_ADDRESS, “page”: 1,
“page_size”: limit})
txs = []
if data:
items = data if isinstance(data, list) else data.get(“transactions”, [])
for tx in (items or [])[:limit]:
txs.append({
“sig”:    tx.get(“trans_id”) or tx.get(“signature”) or “”,
“status”: tx.get(“status”) or “unknown”,
“fee”:    tx.get(“fee”, 0),
“time”:   tx.get(“block_time”) or tx.get(“blockTime”),
“type”:   “”,
})
return txs

async def fetch_portfolio(session) -> Optional[dict]:
return await solscan_get(session, “/account/info”,
{“address”: WALLET_ADDRESS})

# ─── DISPLAY ──────────────────────────────────────────────

def display_sol(sol: float, portfolio):
tier = get_tier(sol)
usd = 0
if portfolio and isinstance(portfolio, dict):
usd = float(portfolio.get(“sol_balance_usd”) or 0)

```
print(f"{C.BOLD}  💰 SOL Balance{C.RESET}")
usd_str = f"  {C.DIM}≈ ${usd:,.2f} USD{C.RESET}" if usd else ""
print(f"     {C.GREEN}{C.BOLD}{sol:.6f} SOL{C.RESET}{usd_str}")
print(f"     Reward Tier → {C.YELLOW}{C.BOLD}{tier}{C.RESET}")
print()
```

def display_tokens(tokens: list):
print(f”{C.BOLD}  🪙 SPL Tokens{C.RESET}”)
if not tokens:
print(f”     {C.DIM}No tokens found{C.RESET}”)
else:
for t in tokens[:10]:
sym = t[“symbol”].ljust(8)
amt = f”{t[‘amount’]:>14,.4f}”
usd = f”  {C.DIM}≈ ${t[‘usd’]:,.2f}{C.RESET}” if t[“usd”] else “”
print(f”     {C.CYAN}{sym}{C.RESET}  {C.WHITE}{amt}{C.RESET}{usd}”)
print()

def display_transactions(txs: list):
print(f”{C.BOLD}  📋 Recent Transactions{C.RESET}”)
if not txs:
print(f”     {C.DIM}No transactions{C.RESET}”)
else:
for tx in txs:
ok = tx[“status”] in (“success”, “finalized”, “confirmed”)
st = f”{C.GREEN}✓{C.RESET}” if ok else f”{C.RED}✗{C.RESET}”
sig = (tx[“sig”][:14] + “…”) if tx[“sig”] else “???”
ts = datetime.fromtimestamp(tx[“time”]).strftime(”%m/%d %H:%M”) if tx[“time”] else “”
fee = lamports_to_sol(tx[“fee”]) if tx[“fee”] else 0
print(f”     {st}  {C.DIM}{sig}  {ts}  fee:{fee:.6f}{C.RESET}”)
print()

def display_alerts(sol, prev_sol, tokens, prev_tokens):
alerts = []
if prev_sol is not None:
diff = sol - prev_sol
if abs(diff) > 0.000001:
d = f”+{diff:.6f}” if diff > 0 else f”{diff:.6f}”
alerts.append(f”{‘📈’ if diff > 0 else ‘📉’} SOL {d}”)

```
if prev_tokens:
    prev_map = {t["mint"]: t["amount"] for t in prev_tokens}
    for t in tokens:
        prev_amt = prev_map.get(t["mint"], 0)
        if t["amount"] > prev_amt + 0.0001:
            alerts.append(f"📈 {t['symbol']} เข้า +{t['amount'] - prev_amt:.4f}")

if alerts:
    print(f"{C.MAGENTA}{C.BOLD}  🔔 ALERT!{C.RESET}")
    for a in alerts:
        print(f"     {C.YELLOW}{C.BOLD}{a}{C.RESET}")
    print()
```

# ─── MAIN ─────────────────────────────────────────────────

async def main():
prev_sol, prev_tokens = None, []

```
print(f"\n{C.CYAN}  🚀 Starting Solana Monitor...{C.RESET}")
print(f"  Wallet  : {WALLET_ADDRESS}")
print(f"  API     : Solscan v2")
print(f"  Interval: {POLL_INTERVAL}s\n")
await asyncio.sleep(1)

async with aiohttp.ClientSession() as session:
    while True:
        print_header()
        sol       = await fetch_sol(session)
        tokens    = await fetch_tokens(session)
        txs       = await fetch_transactions(session)
        portfolio = await fetch_portfolio(session)

        if sol is not None:
            display_alerts(sol, prev_sol, tokens, prev_tokens)
            display_sol(sol, portfolio)
        else:
            print(f"  {C.RED}⚠ Cannot fetch balance{C.RESET}\n")

        display_tokens(tokens)
        display_transactions(txs)

        print(f"  {C.DIM}{'─'*52}{C.RESET}")
        print(f"  {C.DIM}Next update in {POLL_INTERVAL}s...  Ctrl+C to stop{C.RESET}")

        prev_sol, prev_tokens = sol, tokens
        await asyncio.sleep(POLL_INTERVAL)
```

if **name** == “**main**”:
try:
asyncio.run(main())
except KeyboardInterrupt:
print(f”\n{C.YELLOW}  Monitor stopped. 👋{C.RESET}\n”)
