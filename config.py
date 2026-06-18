import os

# ─── Global ────────────────────────────────────────────────
POLL_INTERVAL = 15

# ─── Solana Config ─────────────────────────────────────────
SOL_WALLET = "4b2Zkq2Lvt15v9PXeNmbkwMZbDfUXbgdmXd4x2j6cWxX"
SOLSCAN_API_KEY = os.environ.get("SOLSCAN_API_KEY")
SOLSCAN_BASE = "https://pro-api.solscan.io/v2.0"

# ─── Bitcoin Config ────────────────────────────────────────
BTC_WALLET = "bc1qtruve79ssu0ncnd99hma4734qnjqpfsr9g4ut0"
UNISAT_API_KEY = os.environ.get("UNISAT_API_KEY") # อย่าลืมไปตั้งใน GitHub Secrets
UNISAT_BASE = "https://open-api.unisat.io/v1"
