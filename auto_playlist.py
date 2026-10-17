import requests, json, datetime

SOURCE = "https://bandeltv.xyz/2026/vid/New.php"
VIDEO_TUNGGU_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/awal.mp4"
VIDEO_TUNGGU_LAMA = "waitng_event_gemini.mp4"

# NAMA KATEGORI CUSTOM - TAPI KUNCINYA TETAP NGIKUT TARGET
KATEGORI_MAP = {
    "upcoming": "UPCOMING EVENT",
    "live": "LIVE NOW",
    "bola": "SPORT | BOLA",
    "movie": "BIOSKOP",
    "default": "BANDEL TV"
}

def get_source():
    r = requests.get(SOURCE, timeout=15, headers={"User-Agent":"Mozilla/5.0","Referer":"https://bandeltv.xyz/"})
    r.raise_for_status()
    return r.text

def detect_kategori(title, url, is_upcoming):
    t = (title + " " + url).lower()
    if is_upcoming:
        return "upcoming"
    if "bola" in t or "champion" in t or "league" in t or "sport" in t:
        return "bola"
    if "movie" in t or "film" in t or "bioskop" in t:
        return "movie"
    if ".m3u8" in t or "live" in t:
        return "live"
    return "default"

def main():
    raw = get_source()
    is_upcoming = VIDEO_TUNGGU_LAMA in raw or "waitng_event" in raw

    print(f"[CHECK] Target: {'UPCOMING' if is_upcoming else 'SUDAH LIVE'}")

    # Parse JSON dari New.php
    try:
        data = json.loads(raw)
        channels = data if isinstance(data, list) else data.get('data', data.get('channels', [data]))
    except:
        # fallback M3U
        channels = [{"title":"Channel","url":l} for l in raw.splitlines() if l.startswith("http")]

    final_list = []
    final_m3u = "#EXTM3U\n"

    for i, ch in enumerate(channels, 1):
        title = ch.get('title') or ch.get('name') or f"Channel {i}"
        url = ch.get('url') or ch.get('file') or ""
        logo = ch.get('logo') or ""

        # 1. VIDEO LOGIC
        if is_upcoming and VIDEO_TUNGGU_LAMA in url:
            url = VIDEO_TUNGGU_CUSTOM
            print(f" -> {title}: Belum mulai, pakai video tunggu kamu")
        else:
            print(f" -> {title}: Sudah mulai, pakai link asli target: {url}")

        # 2. KATEGORI LOGIC - OTOMATIS NGIKUT TARGET
        kat_key = detect_kategori(title, url, is_upcoming and VIDEO_TUNGGU_LAMA in raw)
        group_name = KATEGORI_MAP.get(kat_key, KATEGORI_MAP["default"])

        final_m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group_name}",{title}\n{url}\n'
        final_list.append({
            "id": i,
            "title": title,
            "url": url,
            "logo": logo,
            "category_key": kat_key,  # kunci asli dari target
            "group": group_name,       # nama custom kamu
            "status": "upcoming" if kat_key == "upcoming" else "live"
        })

    # Simpan
    with open("playlist_final.json", "w", encoding="utf-8") as f:
        json.dump({
            "last_update": datetime.datetime.utcnow().isoformat()+"Z",
            "target_status": "upcoming" if is_upcoming else "live",
            "channels": final_list
        }, f, indent=2, ensure_ascii=False)

    with open("playlist_final.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)

    print(f"\n[✓] Selesai. Kategori akan auto berubah sesuai target.")

if __name__ == "__main__":
    main()
