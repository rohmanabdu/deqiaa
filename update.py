import requests
import os
import re

# ================== CONFIG - EDIT DISINI ==================
SOURCE_URL = "https://liveloveyou.my.id/41c4d6eb/lv.txt"
OUTPUT_FILE = "pl/rama2"

# Logo baru kamu - GANTI DENGAN LOGO KAMU
NEW_LOGO_DEFAULT = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"

# Tulisan yang mau dihapus
REMOVE_TEXTS = ["Gvision TV"]

# Base logo target - cukup tulis base nya, tanpa &bg=
# Semua varian warna otomatis keganti
LOGO_TARGETS = [
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png",
    "https://i.ibb.co.com/d15rKps/20260701-044822.jpg",
    "https://i.ibb.co.com/LXD7m275/20260730-120141.jpg",
    "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2F",
    "https://i.ibb.co.com/",
]
# ==========================================================

def clean_base_url(url):
    """Bersihkan parameter bg dari url"""
    url = re.sub(r'[&?]bg=[A-Fa-f0-9]{3,8}', '', url, flags=re.IGNORECASE)
    return url.strip()

def replace_all_color_variants(playlist, old_base, new_logo):
    """
    Ganti SEMUA varian warna dari 1 base logo
    Contoh:
    old_base = https://wsrv.nl/?url=...png
    Akan ganti:
    - https://wsrv.nl/?url=...png
    - https://wsrv.nl/?url=...png&bg=FFFFFF
    - https://wsrv.nl/?url=...png&bg=00FA9A
    - https://wsrv.nl/?url=...png?bg=FF1493
    - dll semua warna
    """
    old_base = clean_base_url(old_base)
    if not old_base:
        return playlist

    # Pattern: base URL + optional &bg= atau ?bg= + kode hex 3-8 digit
    # flag IGNORECASE biar &BG=, &Bg=, &bg= semua kena
    pattern = re.escape(old_base) + r'(?:[&?]bg=[A-Fa-f0-9]{3,8})?'

    # Hitung berapa yang keganti
    matches = re.findall(pattern, playlist, flags=re.IGNORECASE)
    if matches:
        print(f"[GANTI] {old_base[:60]}... -> {len(set(matches))} varian warna ditemukan")

    playlist = re.sub(pattern, new_logo, playlist, flags=re.IGNORECASE)
    return playlist

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

    # 1. HAPUS TEKS YANG TIDAK DIINGINKAN
    for txt in REMOVE_TEXTS:
        playlist = playlist.replace(txt, "")

    # 2. BERSIHKAN TANDA |
    playlist = playlist.replace("| ", "").replace(" |", "")

    # 3. GANTI SEMUA LOGO + SEMUA WARNA
    print("\n--- Mulai ganti logo ---")
    for target in LOGO_TARGETS:
        playlist = replace_all_color_variants(playlist, target, NEW_LOGO_DEFAULT)

    # 4. CLEANUP FINAL - hapus sisa kode bg yang masih nyangkut dimana saja
    # Ini jaga-jaga kalau ada logo lain yang masih ada &bg=
    playlist = re.sub(r'[&?]bg=[A-Fa-f0-9]{3,8}', '', playlist, flags=re.IGNORECASE)

    # 5. RAPIKAN
    # Hapus baris kosong dan spasi berlebih
    cleaned_lines = []
    for line in playlist.split("\n"):
        line = line.rstrip()
        if line:
            cleaned_lines.append(line)
    playlist = "\n".join(cleaned_lines)

    if not playlist.endswith("\n"):
        playlist += "\n"
    if not playlist.strip().startswith("#EXTM3U"):
        playlist = "#EXTM3U\n" + playlist

    # 6. SIMPAN
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("="*60)
    print(f"SELESAI -> {OUTPUT_FILE}")
    print(f"Total baris akhir: {len(playlist.splitlines())}")
    print(f"Semua logo dengan kode warna sudah diganti ke:\n{NEW_LOGO_DEFAULT}")

if __name__ == "__main__":
    main()
