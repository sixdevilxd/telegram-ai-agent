import os
import textwrap


def render_chart_card(data: dict, out_path: str) -> str | None:
    """Render a technical-analysis summary card image. Returns path or None if Pillow unavailable."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None

    W, H = 1000, 1100
    bg = (15, 18, 26)
    panel = (24, 28, 40)
    accent_up = (38, 194, 129)
    accent_down = (235, 77, 75)
    text_color = (230, 234, 242)
    muted = (150, 158, 175)

    bias = (data.get("bias") or "netral").lower()
    accent = accent_up if bias == "bullish" else accent_down if bias == "bearish" else (90, 130, 220)

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    def font(size, bold=False):
        paths = [
            "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        return ImageFont.load_default()

    y = 40
    d.rectangle([0, 0, W, 16], fill=accent)
    asset = str(data.get("asset") or "Chart")
    tf = str(data.get("timeframe") or "-")
    d.text((40, y), f"{asset}", font=font(54, True), fill=text_color); y += 70
    d.text((40, y), f"Timeframe: {tf}  |  Bias: {bias.upper()}  |  Confidence: {data.get('confidence','-')}", font=font(26), fill=muted); y += 60

    def section(title, body, color=text_color):
        nonlocal y
        d.rectangle([40, y, W - 40, y + 4], fill=panel)
        y += 20
        d.text((40, y), title, font=font(30, True), fill=accent); y += 44
        for line in textwrap.wrap(str(body), width=70) or ["-"]:
            d.text((50, y), line, font=font(26), fill=color); y += 36
        y += 14

    section("Tren", data.get("trend", "-"))
    sup = ", ".join(map(str, data.get("supports", []) or [])) or "-"
    res = ", ".join(map(str, data.get("resistances", []) or [])) or "-"
    section("Support", sup, accent_up)
    section("Resistance", res, accent_down)
    section("Pola", data.get("pattern", "-"))
    section("Indikator", data.get("indicators", "-"))
    section("Skenario Bullish", data.get("bullish_scenario", "-"), accent_up)
    section("Skenario Bearish", data.get("bearish_scenario", "-"), accent_down)

    d.text((40, H - 60), "Analisis berbasis gambar, bukan saran finansial. DYOR.", font=font(22), fill=muted)

    img.save(out_path, "PNG")
    return out_path
