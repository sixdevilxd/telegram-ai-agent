from urllib.parse import quote_plus

PLATFORMS = {
    "x": "https://x.com/search?q={query}&src=typed_query",
    "twitter": "https://x.com/search?q={query}&src=typed_query",
    "linkedin": "https://www.linkedin.com/search/results/all/?keywords={query}",
    "reddit": "https://www.reddit.com/search/?q={query}",
    "facebook": "https://www.facebook.com/search/top?q={query}",
    "youtube": "https://www.youtube.com/results?search_query={query}",
    "tiktok": "https://www.tiktok.com/search?q={query}",
    "instagram": "https://www.instagram.com/explore/search/keyword/?q={query}",
}


def social_search(platform: str, query: str) -> str:
    platform = platform.lower().strip()
    query = query.strip()

    if not platform or not query:
        return "Contoh: /social reddit groq api"

    if platform not in PLATFORMS:
        return (
            "Platform belum didukung.\n"
            "Pilihan: x, twitter, linkedin, reddit, facebook, youtube, tiktok, instagram"
        )

    url = PLATFORMS[platform].format(query=quote_plus(query))
    return f"Search {platform} untuk: {query}\n\n{url}"


def social_prompt(platform: str, topic: str) -> str:
    platform = platform.lower().strip()
    topic = topic.strip()
    if not topic:
        return "Contoh: /socialprompt linkedin AI agent untuk bisnis"

    style = {
        "x": "pendek, tajam, thread-friendly, maksimal 280 karakter per poin",
        "twitter": "pendek, tajam, thread-friendly, maksimal 280 karakter per poin",
        "linkedin": "profesional, insight-driven, cocok untuk personal branding",
        "reddit": "natural, jujur, diskusi komunitas, tidak terlalu promosi",
        "facebook": "santai, engaging, mudah dipahami publik umum",
        "instagram": "caption singkat, visual-first, dengan hook kuat",
        "tiktok": "script video pendek dengan hook 3 detik pertama",
        "youtube": "judul, deskripsi, dan outline video yang SEO-friendly",
    }.get(platform, "sesuaikan dengan platform sosial media")

    return (
        f"Buat konten untuk {platform} tentang: {topic}\n"
        f"Gaya: {style}.\n"
        "Berikan versi siap posting, hook, CTA, dan hashtag relevan."
    )


def platform_guide(platform: str) -> str:
    platform = platform.lower().strip()
    guides = {
        "x": "X/Twitter cocok untuk opini singkat, thread, breaking news, dan networking cepat.",
        "twitter": "X/Twitter cocok untuk opini singkat, thread, breaking news, dan networking cepat.",
        "linkedin": "LinkedIn cocok untuk personal branding, karier, B2B, insight profesional, dan studi kasus.",
        "reddit": "Reddit cocok untuk diskusi komunitas, feedback jujur, riset pain point, dan niche audience.",
        "facebook": "Facebook cocok untuk komunitas, grup, jualan lokal, storytelling, dan audience umum.",
        "instagram": "Instagram cocok untuk visual branding, reels, carousel edukasi, dan lifestyle content.",
        "tiktok": "TikTok cocok untuk short video, edukasi cepat, trend, dan growth awareness.",
        "youtube": "YouTube cocok untuk konten panjang, tutorial, review, SEO, dan audience evergreen.",
    }
    if not platform:
        return "Contoh: /platform linkedin"
    return guides.get(platform, "Platform belum dikenal. Coba: x, linkedin, reddit, facebook, instagram, tiktok, youtube")
