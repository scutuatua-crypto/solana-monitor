# solana-monitor
# 🌊 Solana Wallet Monitor + Reward System

Monitor real-time SOL balance, SPL tokens, transactions และ reward tiers

## ✅ Features

- 💰 SOL balance แบบ real-time
- 🪙 SPL Token balances ทั้งหมด
- 📋 Recent transactions (5 รายการล่าสุด)
- 🔔 Alerts เมื่อมี asset เข้า/ออก
- 🏆 Reward tiers (Bronze → Diamond)

## 🚀 วิธีรัน (ใน Codespaces terminal)

```bash
# 1. ติดตั้ง dependency
pip install -r requirements.txt

# 2. รัน monitor
python monitor.py
```

## 🏆 Reward Tiers

|Tier      |SOL            |
|----------|---------------|
|🥉 Bronze  |0 - 1 SOL      |
|🥈 Silver  |1 - 10 SOL     |
|🥇 Gold    |10 - 100 SOL   |
|💎 Platinum|100 - 1,000 SOL|
|👑 Diamond |1,000+ SOL     |

## ⚙️ ปรับ config

แก้ในไฟล์ `monitor.py`:

```python
WALLET_ADDRESS = "your_wallet_here"
POLL_INTERVAL = 10  # วินาที
RPC_URL = "https://api.mainnet-beta.solana.com"
```

## 🛑 หยุดโปรแกรม

กด `Ctrl + C`
