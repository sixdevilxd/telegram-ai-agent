import re


def _find_floats(text):
    return [float(x) for x in re.findall(r"\d+\.?\d*", text.replace(",", ".")) if x]


def parse_signal(text: str) -> dict:
    data = {
        "pair": None, "side": None, "leverage": None,
        "entry": [], "tps": [], "sl": None,
    }
    if not text:
        return data

    pair = re.search(r"([A-Z0-9]{2,15}\s*/\s*[A-Z]{2,6})", text)
    if pair:
        data["pair"] = pair.group(1).replace(" ", "")

    low = text.lower()
    if "short" in low or "sell" in low:
        data["side"] = "SHORT"
    elif "long" in low or "buy" in low:
        data["side"] = "LONG"

    lev = re.search(r"(\d+)\s*x", low)
    if lev:
        data["leverage"] = int(lev.group(1))

    for line in text.splitlines():
        ll = line.lower()
        if "entry" in ll:
            data["entry"] = _find_floats(line)
        elif "tp" in ll or "target" in ll:
            data["tps"].extend(_find_floats(line))
        elif "sl" in ll or "stop" in ll:
            vals = _find_floats(line)
            if vals:
                data["sl"] = vals[0]
    return data


def analyze_signal(text: str) -> str:
    s = parse_signal(text)
    if not s["entry"] and not s["tps"]:
        return "Tidak terbaca sebagai sinyal. Pastikan ada Entry, TP, dan SL."

    entry = sum(s["entry"]) / len(s["entry"]) if s["entry"] else None
    side = s["side"] or "?"
    lev = s["leverage"]
    sl = s["sl"]

    lines = ["Analisa Sinyal (objektif, bukan saran finansial):\n"]
    lines.append(f"Pair: {s['pair'] or '-'}")
    lines.append(f"Arah: {side}")
    lines.append(f"Leverage: {str(lev) + 'X' if lev else '-'}")
    lines.append(f"Entry (rata-rata): {entry if entry else '-'}")
    lines.append(f"SL: {sl if sl else '-'}")

    # SL distance
    sl_pct = None
    if entry and sl:
        sl_pct = abs(entry - sl) / entry * 100
        lines.append(f"\nJarak SL: {sl_pct:.2f}% dari entry")
        if lev:
            loss_at_sl = sl_pct * lev
            lines.append(f"Estimasi rugi margin saat kena SL: ~{loss_at_sl:.0f}%")
            liq_pct = 100 / lev
            lines.append(f"Estimasi jarak likuidasi: ~{liq_pct:.2f}% dari entry")
            if sl_pct >= liq_pct:
                lines.append("PERINGATAN: SL lebih jauh dari titik likuidasi. Posisi bisa terlikuidasi SEBELUM kena SL.")

    # Risk/Reward per TP
    if entry and sl and s["tps"]:
        risk = abs(entry - sl)
        lines.append("\nRisk/Reward per TP:")
        for i, tp in enumerate(s["tps"], 1):
            reward = abs(tp - entry)
            rr = reward / risk if risk else 0
            lines.append(f"- TP{i} {tp}: R/R = {rr:.2f}")

    # Risk score
    score = 0
    notes = []
    if lev:
        if lev >= 50: score += 4; notes.append("Leverage sangat tinggi (>=50X), risiko likuidasi ekstrem.")
        elif lev >= 20: score += 3; notes.append("Leverage tinggi (>=20X).")
        elif lev >= 10: score += 2
        else: score += 1
    if sl_pct is not None and sl_pct < 5:
        score += 2; notes.append("Jarak SL sempit (<5%), mudah tersapu volatilitas.")
    if "register" in text.lower() or "vipcode" in text.lower() or "ref" in text.lower():
        notes.append("Ada link referral: penyebar sinyal kemungkinan dapat komisi dari volume trading kamu (conflict of interest).")

    level = "RENDAH"
    if score >= 6: level = "EKSTREM"
    elif score >= 4: level = "TINGGI"
    elif score >= 2: level = "SEDANG"

    lines.append(f"\nSkor risiko: {level}")
    for n in notes:
        lines.append(f"- {n}")

    lines.append("\nIni analisis risiko objektif, bukan saran beli/jual. DYOR dan kelola risiko sendiri.")
    return "\n".join(lines)
