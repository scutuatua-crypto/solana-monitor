REWARD_TIERS = [
    {"min": 0,    "max": 1,    "label": "🥉 Bronze Holder"},
    {"min": 1,    "max": 10,   "label": "🥈 Silver Holder"},
    {"min": 10,   "max": 100,  "label": "🥇 Gold Holder"},
    {"min": 100,  "max": 1000, "label": "💎 Platinum Holder"},
    {"min": 1000, "max": 9e18, "label": "👑 Diamond Holder"},
]


def get_tier(sol: float) -> str:
    for t in REWARD_TIERS:
        if t["min"] <= sol < t["max"]:
            return t["label"]
    return "👑 Diamond Holder"


def get_next_tier(sol: float) -> str:
    for i, t in enumerate(REWARD_TIERS):
        if t["min"] <= sol < t["max"]:
            if i + 1 < len(REWARD_TIERS):
                next_t = REWARD_TIERS[i + 1]
                needed = next_t["min"] - sol
                return f"ต้องการอีก {needed:.4f} SOL → {next_t['label']}"
    return "🏆 Max tier แล้ว!"
