# auto_playlist.py - VERSI PINTER (upcoming vs live)
import requests, json

SOURCE = "https://bandeltv.xyz/2026/vid/New.php"
VIDEO_TUNGGU_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/awal.mp4"
VIDEO_TUNGGU_LAMA = "waitng_event_gemini.mp4"

def get_source():
    r = requests.get(SOURCE, timeout=15, headers={
        "User-Agent":"Mozilla/5.0", "Referer":"https://bandeltv.xyz/"
    })
    return r.text

def process():
    text = get_source()
    
    # CEK STATUS DARI LINK TUJUAN
    is_upcoming = VIDEO_TUNGGU_LAMA in text or "waitng_event" in text
    
    if is_upcoming:
        print("[STATUS] BELUM MULAI - pakai video tunggu custom")
        final_text = text.replace(
            f"https://bandeltv.xyz/film/{VIDEO_TUNGGU_LAMA}", VIDEO_TUNGGU_CUSTOM
        ).replace(VIDEO_TUNGGU_LAMA, VIDEO_TUNGGU_CUSTOM)
        # pastikan juga yang https://bandeltv.xyz/film/waitng_event_gemini.mp4
        final_text = final_text.replace(
            "https://bandeltv.xyz/film/waitng_event_gemini.mp4", VIDEO_TUNGGU_CUSTOM
        )
    else:
        print("[STATUS] SUDAH MULAI - pakai link siaran asli dari New.php")
        final_text = text # JANGAN DI GANTI, pakai link live asli dari tujuan

    # Simpan 2 versi
    with open("playlist_final.json", "w", encoding="utf-8") as f:
        # kalau source JSON, kita simpan apa adanya (sudah diganti jika upcoming)
        try:
            data = json.loads(final_text)
            json.dump(data, f, indent=2, ensure_ascii=False)
        except:
            # kalau M3U, bungkus jadi JSON info
            json.dump({"status": "upcoming" if is_upcoming else "live", "raw": final_text}, f, indent=2)

    with open("playlist_final.m3u", "w", encoding="utf-8") as f:
        f.write(final_text if final_text.strip().startswith("#EXTM3U") else final_text)

    print(f"[✓] Selesai. Status: {'UPCOMING' if is_upcoming else 'LIVE'}")

if __name__ == "__main__":
    process()
