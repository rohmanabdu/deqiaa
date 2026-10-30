import requests
import os
import re

# ================== CONFIG - EDIT DISINI ==================
SOURCE_URL = "https://liveloveyou.my.id/41c4d6eb/lv.txt"
OUTPUT_FILE = "pll/rama2"

CATEGORY_BARU = "LIVE EVENT" 

NEW_LOGO_DEFAULT = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"

REMOVE_TEXTS = ["Gvision TV"]

LOGO_TARGETS = [
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png",
    "https://i.ibb.co.com/d15rKps/20260701-044822.jpg",
    "https://i.ibb.co.com/LXD7m275/20260730-120141.jpg",
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2F",
    "https://i.ibb.co.com/",
]

# PLAYLIST TAMBAHAN DI AWAL - EDIT DISINI
TOP_PLAYLIST = '#EXTINF:-1 tvg-id="" tvg-name="Donasi ++" tvg-logo="https://static.vecteezy.com/system/resources/previews/054/224/335/non_2x/charity-icon-colored-outline-icon-style-hand-giving-money-icon-related-to-donation-and-charity-donation-elements-illustration-vector.jpg" group-title="LIVE EVENT",Donasi ++\nhttps://github.com/rohmanabdu/cloudd/raw/refs/heads/main/awal.mp4'
# ==========================================================

def clean_base_url(url):
    url = re.sub(r'[&?]bg=[A-Fa-f0-9]{3,8}', '', url, flags=re.IGNORECASE)
    return url.strip()

def replace_all_color_variants(playlist, old_base, new_logo):
    old_base = clean_base_url(old_base)
    if not old_base:
        return playlist
    pattern = re.escape(old_base) + r'(?:[&?]bg=[A-Fa-f0-9]{3,8})?'
    playlist = re.sub(pattern, new_logo, playlist, flags=re.IGNORECASE)
    return playlist

def set_same_category(line, new_category):
    if "#EXTINF" not in line:
        return line
    if re.search(r'group-title\s*=\s*"[^"]*"', line, re.IGNORECASE):
        line = re.sub(r'group-title\s*=\s*"[^"]*"', f'group-title="{new_category}"', line, flags=re.IGNORECASE)
    else:
        if "," in line:
            parts = line.rsplit(",", 1)
            line = f'{parts[0]} group-title="{new_category}",{parts[1]}'
    return line

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE) or "playlist", exist_ok=True)

    print("="*60)
    print(f"Ambil playlist: {SOURCE_URL}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/plain,*/*"
        }
        r = requests.get(SOURCE_URL, headers=headers, timeout=30)
        r.raise_for_status()
        playlist = r.text
    except Exception as e:
        print(f"GAGAL ambil playlist: {e}")
        return

    print(f"Awal: {len(playlist)} char, {len(playlist.splitlines())} baris")

    for txt in REMOVE_TEXTS:
        playlist = playlist.replace(txt, "")
    playlist = playlist.replace("| ", "").replace(" |", "")

    print("\n--- Mulai ganti logo ---")
    for target in LOGO_TARGETS:
        playlist = replace_all_color_variants(playlist, target, NEW_LOGO_DEFAULT)

    playlist = re.sub(r'[&?]bg=[A-Fa-f0-9]{3,8}', '', playlist, flags=re.IGNORECASE)

    print(f"--- Set kategori jadi: {CATEGORY_BARU} ---")
    final_lines = []
    for line in playlist.split("\n"):
        line = line.rstrip()
        if not line:
            continue
        if "#EXTINF" in line.upper():
            line = set_same_category(line, CATEGORY_BARU)
        final_lines.append(line)
    
    playlist = "\n".join(final_lines)

    if not playlist.strip().startswith("#EXTM3U"):
        playlist = "#EXTM3U\n" + playlist

    # TAMBAHKAN PLAYLIST DI AWAL - SETELAH #EXTM3U
    if TOP_PLAYLIST:
        # Hapus #EXTM3U dulu biar tidak dobel, lalu susun ulang
        temp = playlist.replace("#EXTM3U", "", 1).lstrip()
        playlist = f"#EXTM3U\n{TOP_PLAYLIST}\n{temp}"

    if not playlist.endswith("\n"):
        playlist += "\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("="*60)
    print(f"SELESAI -> {OUTPUT_FILE}")
    print(f"Channel Donasi di urutan #1")
    print(f"Kategori semua channel: {CATEGORY_BARU}")

if __name__ == "__main__":
    main()
