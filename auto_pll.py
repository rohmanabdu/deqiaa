import requests

SOURCE = "https://bandeltv.xyz/2026/vid/Newabah.php"
VIDEO_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/upcoming.mp4"
VIDEO_LAMA = "waitng_event_gemini.mp4"

r = requests.get(SOURCE, timeout=15, headers={
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://bandeltv.xyz/"
})
raw = r.text

print(f"Panjang source: {len(raw)}")
print(f"Apakah upcoming? {VIDEO_LAMA in raw}")

# JANGAN PARSE JSON, LANGSUNG GANTI STRING SAJA
# Biar struktur 100% sama kayak target
final = raw.replace(
    "https://bandeltv.xyz/film/waitng_event_gemini.mp4", VIDEO_CUSTOM
).replace(
    "https://bandeltv.xyz/film/waitng_event_gemini.mp4".replace("https","http"), VIDEO_CUSTOM
).replace(VIDEO_LAMA, VIDEO_CUSTOM)

# Simpan persis sama
with open("finall.json", "w", encoding="utf-8") as f:
    f.write(final)

with open("finall", "w", encoding="utf-8") as f:
    f.write(final)

print("[✓] playlist_final.json disimpan TANPA UBAH STRUKTUR")
