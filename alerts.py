def check_alerts(sol, prev_sol, tokens, prev_tokens) -> list:
alerts = []

```
# SOL เปลี่ยน
if prev_sol is not None:
    diff = sol - prev_sol
    if abs(diff) > 0.000001:
        d = f"+{diff:.6f}" if diff > 0 else f"{diff:.6f}"
        icon = "📈" if diff > 0 else "📉"
        alerts.append(f"{icon} SOL {d}")

# SPL token เปลี่ยน
if prev_tokens:
    prev_map = {t["mint"]: t["amount"] for t in prev_tokens}
    for t in tokens:
        prev_amt = prev_map.get(t["mint"], 0)
        if t["amount"] > prev_amt + 0.0001:
            diff = t["amount"] - prev_amt
            alerts.append(f"📈 {t['symbol']} เข้า +{diff:.4f}")
        elif t["amount"] < prev_amt - 0.0001:
            diff = prev_amt - t["amount"]
            alerts.append(f"📉 {t['symbol']} ออก -{diff:.4f}")

return alerts
```
