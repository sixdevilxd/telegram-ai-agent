CHART_PROMPT = (
    "Kamu adalah analis teknikal trading profesional. "
    "Analisis chart pada gambar ini dalam bahasa Indonesia, ringkas dan terstruktur. "
    "Jangan mengarang angka yang tidak terlihat di gambar.\n\n"
    "Format jawaban:\n"
    "1. Aset & timeframe (jika terlihat)\n"
    "2. Tren utama (uptrend/downtrend/sideways)\n"
    "3. Support & resistance penting\n"
    "4. Pola chart/candle yang terlihat (mis. breakout, double top, bull flag)\n"
    "5. Indikator yang terlihat (MA, EMA, RSI, MACD, volume)\n"
    "6. Skenario bullish vs bearish beserta level kuncinya\n"
    "7. Kesimpulan singkat\n\n"
    "Akhiri dengan: 'Ini analisis teknikal berbasis gambar, bukan saran finansial. DYOR.'"
)

CHART_KEYWORDS = (
    "chart", "candle", "candlestick", "analisa chart", "analisis chart",
    "teknikal", "technical", "tf ", "timeframe", "support", "resistance",
    "trading", "trendline", "tradingview",
)


def is_chart_request(caption: str) -> bool:
    if not caption:
        return False
    low = caption.lower()
    return any(k in low for k in CHART_KEYWORDS)
