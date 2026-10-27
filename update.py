import requests
import os
import re

# ================== CONFIG - EDIT DISINI ==================
SOURCE_URL = "https://liveloveyou.my.id/41c4d6eb/lv.txt"
OUTPUT_FILE = "pll/rama2"

# KATEGORI BARU - GANTI DISINI
# Semua channel akan jadi 1 kategori ini
CATEGORY_BARU = "LIVE EVENT" 

# Logo baru kamu - GANTI DENGAN LOGO KAMU
NEW_LOGO_DEFAULT = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"

# Tulisan yang mau dihapus
REMOVE_TEXTS = ["Gvision TV"]

# Base logo target
LOGO_TARGETS = [
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png",
    "https://i.ibb.co.com/d15rKps/20260701-044822.jpg",
    "https://i.ibb.co.com/LXD7m275/20260730-120141.jpg",
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2F",
    "https://i.ibb.co.com/",
]
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
    """Set semua EXTINF jadi 1 kategori yang sama"""
    if "#EXTINF" not in line:
        return line
    
    # Kalau sudah ada group-title, ganti isinya
    if re.search(r'group-title\s*=\s*"[^"]*"', line, re.IGNORECASE):
        line = re.sub(r'group-title\s*=\s*"[^"]*"', f'group-title="{new_category}"', line, flags=re.IGNORECASE)
    else:
        # Kalau belum ada group-title, tambahkan sebelum koma terakhir
        # Format: #EXTINF:-1 tvg-logo="..." ,Nama Channel
        # Kita selipkan group-title sebelum koma
        if "," in line:
            parts = line.rsplit(",", 1)
            # cek kalau di bagian depan belum ada group-title
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

    # 1. HAPUS TEKS
    for txt in REMOVE_TEXTS:
        playlist = playlist.replace(txt, "")

    # 2. BERSIHKAN TANDA |
    playlist = playlist.replace("| ", "").replace(" |", "")

    # 3. GANTI SEMUA LOGO
    print("\n--- Mulai ganti logo ---")
    for target in LOGO_TARGETS:
        playlist = replace_all_color_variants(playlist, target, NEW_LOGO_DEFAULT)

    # 4. CLEANUP sisa bg=
    playlist = re.sub(r'[&?]bg=[A-Fa-f0-9]{3,8}', '', playlist, flags=re.IGNORECASE)

    # 5. JADIKAN 1 KATEGORI SAMA - BAGIAN BARU
    print(f"--- Set kategori jadi: {CATEGORY_BARU} ---")
    final_lines = []
    for line in playlist.split("\n"):
        line = line.rstrip()
        if not line:
            continue
        
        # Proses hanya baris EXTINF
        if "#EXTINF" in line.upper():
            line = set_same_category(line, CATEGORY_BARU)
        
        final_lines.append(line)
    
    playlist = "\n".join(final_lines)

    if not playlist.endswith("\n"):
        playlist += "\n"
    if not playlist.strip().startswith("#EXTM3U"):
        playlist = "#EXTM3U\n" + playlist

    # 6. SIMPAN
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("="*60)
    print(f"SELESAI -> {OUTPUT_FILE}")
    print(f"Kategori semua channel: {CATEGORY_BARU}")
    print(f"Logo diganti ke: {NEW_LOGO_DEFAULT}")

if __name__ == "__main__":
    main()
