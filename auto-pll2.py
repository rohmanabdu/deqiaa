import requests
import os

# --- CONFIG ---
SOURCE = "https://bandeltv.xyz/sc1980/2025/Kvision/LIVE22.php"
VIDEO_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/upcoming.mp4"
VIDEO_LAMA = "waitng_event_gemini.mp4"
# Folder tempat simpan, ganti nama folder disini kalau mau
FOLDER_TUJUAN = "pll"

# Bikin folder kalau belum ada biar gak error
if not os.path.exists(FOLDER_TUJUAN):
    os.makedirs(FOLDER_TUJUAN)
    print(f"[+] Folder '{FOLDER_TUJUAN}' dibuat")

try:
    r = requests.get(SOURCE, timeout=15, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://bandeltv.xyz/"
    })
    raw = r.text

    print(f"Panjang source: {len(raw)}")
    print(f"Apakah upcoming? {VIDEO_LAMA in raw}")

    # JANGAN PARSE JSON, LANGSUNG GANTI STRING SAJA
    final = raw.replace(
        "https://bandeltv.xyz/film/waitng_event_gemini.mp4", VIDEO_CUSTOM
    ).replace(
        "https://bandeltv.xyz/film/waitng_event_gemini.mp4".replace("https","http"), VIDEO_CUSTOM
    ).replace(VIDEO_LAMA, VIDEO_CUSTOM)

    # Simpan ke dalam folder
    path_json = os.path.join(FOLDER_TUJUAN, "ramaa2.json")
    path_no_ext = os.path.join(FOLDER_TUJUAN, "ramaa2")

    with open(path_json, "w", encoding="utf-8") as f:
        f.write(final)

    with open(path_no_ext, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"[✓] Berhasil disimpan di:")
    print(f" - {path_json}")
    print(f" - {path_no_ext}")

except Exception as e:
    print(f"[X] Error: {e}")
