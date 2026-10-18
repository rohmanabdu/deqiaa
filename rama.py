import requests, re, os

SOURCE = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/playlist_final.m3u"
OUTPUT = "hasil.m3u"
CATEGORY = "LIVE EVENT"

r = requests.get(SOURCE, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
lines = r.text.splitlines()

out = ["#EXTM3U"]
for line in lines:
    s = line.strip()
    if not s: continue
    if s.startswith("#EXTINF"):
        s = re.sub(r'group-title="[^"]*"', f'group-title="{CATEGORY}"', s)
        if 'group-title=' not in s:
            s = s.replace(',', f' group-title="{CATEGORY}",', 1)
        out.append(s)
    elif s.startswith("http") or s.startswith("#KODIPROP") or s.startswith("#EXTVLCOPT"):
        out.append(s)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
