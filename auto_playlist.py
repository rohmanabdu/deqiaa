# -*- coding: utf-8 -*-
# Auto Event - BandelTV Playlist Updater
# Source: https://bandeltv.xyz/2026/vid/New.php
import requests
import json
import re

SOURCE_URL = "https://bandeltv.xyz/2026/vid/New.php"
# GANTI DISINI VIDEO BARU KAMU
NEW_UPCOMING_VIDEO = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/awal.mp4" 
OLD_VIDEO_KEYWORD = "waitng_event_gemini.mp4"
OUTPUT_FILE = "playlist_final.m3u"
OUTPUT_JSON = "playlist_final.json"

def get_playlist():
    print(f"[+] Ambil playlist dari: {SOURCE_URL}")
    r = requests.get(SOURCE_URL, timeout=15, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://bandeltv.xyz/"
    })
    r.raise_for_status()
    return r.text

def process_content(text):
    # Cek apakah JSON atau M3U
    # Kalau ada OLD_VIDEO, ganti semua
    if OLD_VIDEO_KEYWORD in text:
        print(f"[!] Ditemukan upcoming video lama, ganti ke {NEW_UPCOMING_VIDEO}")
        text = text.replace(
            "https://bandeltv.xyz/film/waitng_event_gemini.mp4", 
            NEW_UPCOMING_VIDEO
        )
        text = text.replace(
            "/film/waitng_event_gemini.mp4", 
            NEW_UPCOMING_VIDEO
        )
        text = text.replace(OLD_VIDEO_KEYWORD, NEW_UPCOMING_VIDEO)
    
    # Kalau JSON, proses lebih rapi
    try:
        data = json.loads(text)
        # ubah di dalam json juga
        json_str = json.dumps(data).replace(OLD_VIDEO_KEYWORD, NEW_UPCOMING_VIDEO)
        json_str = json_str.replace("https://bandeltv.xyz/film/waitng_event_gemini.mp4", NEW_UPCOMING_VIDEO)
        data = json.loads(json_str)
        print(f"[+] {len(data) if isinstance(data, list) else 1} siaran ditemukan (JSON)")
        return json.dumps(data, indent=2), data
    except:
        # anggap M3U
        upcoming_count = text.count(NEW_UPCOMING_VIDEO)
        print(f"[+] Playlist M3U terdeteksi, {upcoming_count} upcoming diganti")
        return text, None

def save_files(m3u_content, json_content):
    # Simpan versi M3U untuk player
    if not m3u_content.strip().startswith("#EXTM3U"):
        # kalau source JSON, kita convert ke M3U
        if json_content:
            m3u = "#EXTM3U\n"
            for item in json_content if isinstance(json_content, list) else [json_content]:
                title = item.get('title') or item.get('name') or item.get('channel') or "Upcoming Event"
                logo = item.get('logo') or item.get('poster') or ""
                url = item.get('url') or item.get('file') or item.get('src') or NEW_UPCOMING_VIDEO
                if OLD_VIDEO_KEYWORD in url:
                    url = NEW_UPCOMING_VIDEO
                m3u += f'#EXTINF:-1 tvg-logo="{logo}",{title}\n{url}\n'
            m3u_content = m3u

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"[✓] Disimpan: {OUTPUT_FILE}")

    if json_content is None:
        # simpan raw juga sebagai json info
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            f.write(m3u_content)
    else:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(json_content, f, indent=2)

if __name__ == "__main__":
    raw = get_playlist()
    final_m3u, final_json = process_content(raw)
    save_files(final_m3u, final_json)
