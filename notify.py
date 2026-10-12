#!/usr/bin/env python3
"""Telegram notifications for new records.

Configuration lives in telegram.json next to this file (ignored by Git,
mode 600): {"token": "<bot token>", "chat_id": <id>}. Without it, send() does
nothing. Standard library only, so the coordinator can call it directly.

  notify.py --setup TOKEN   save the token, find the chat that last messaged
                            the bot (send it /start first), send a test message
  notify.py --test          send a test message
  notify.py --test-photo N  send a test image of the installed packing nN.txt
  notify.py "text"          send a message
"""
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

CONFIG = Path(__file__).resolve().parent/"telegram.json"


def _api(token, method, **params):
    data = urllib.parse.urlencode(params).encode() if params else None
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/{method}", data=data, timeout=10) as r:
        return json.load(r)


def send(text):
    """Send text to the configured chat; never raises. Returns True on success."""
    try:
        config = json.loads(CONFIG.read_text())
        return bool(_api(config["token"], "sendMessage", chat_id=config["chat_id"], text=text,
                         disable_web_page_preview="true").get("ok"))
    except Exception:
        return False


def render_png(packing, out, title, size=1000):
    """Draw a packing file (x y theta per line, box [0, s]) as a PNG with Pillow:
    axis-aligned squares blue, tilted ones orange (darker = larger tilt)."""
    import math
    from PIL import Image, ImageDraw, ImageFont
    rows = [tuple(map(float, l.split()[:3])) for l in Path(packing).read_text().splitlines()
            if l.strip() and not l.startswith("#")]
    side = max(max(x, y)+(abs(math.cos(t))+abs(math.sin(t)))/2 for x, y, t in rows)
    k, pad, head = 2, 24, 64                      # supersample, then downscale
    W, H = (size+2*pad)*k, (size+2*pad+head)*k
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    scale = size*k/side
    ox, oy = pad*k, (pad+head)*k
    def P(x, y):
        return (ox+x*scale, oy+(side-y)*scale)
    d.rectangle([P(0, side), P(side, 0)], outline="black", width=2*k)
    for x, y, t in rows:
        tilt = math.degrees(abs(((t+math.pi/4) % (math.pi/2))-math.pi/4))
        c, s = math.cos(t), math.sin(t)
        pts = [P(x+c*a-s*b, y+s*a+c*b) for a, b in ((-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5))]
        if tilt < 1e-4:
            fill = (157, 195, 230)
        else:
            f = min(1.0, tilt/45)
            fill = (int(253-30*f), int(184-90*f), int(99-60*f))
        d.polygon(pts, fill=fill, outline=(51, 51, 51), width=max(1, k))
    try:
        font = ImageFont.load_default(size=26*k)
    except TypeError:
        font = ImageFont.load_default()
    d.text((pad*k, (pad//2)*k), title, fill="black", font=font)
    img.resize((W//k, H//k), Image.LANCZOS).save(out, optimize=True)
    return out


def send_photo(png, caption):
    """Send a PNG with a caption; never raises. Returns True on success."""
    import uuid
    try:
        config = json.loads(CONFIG.read_text())
        boundary = uuid.uuid4().hex
        parts = []
        for name, value in (("chat_id", str(config["chat_id"])), ("caption", caption[:1024])):
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="{Path(png).name}"\r\n'
                      "Content-Type: image/png\r\n\r\n").encode() + Path(png).read_bytes() + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        request = urllib.request.Request(f"https://api.telegram.org/bot{config['token']}/sendPhoto",
                                         data=b"".join(parts),
                                         headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        with urllib.request.urlopen(request, timeout=30) as r:
            return bool(json.load(r).get("ok"))
    except Exception:
        return False


def log(kind, ok, text):
    """One JSON line per send attempt in experiments/forever/notify.log."""
    import time
    try:
        with (CONFIG.parent/"experiments/forever/notify.log").open("a") as f:
            f.write(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                "kind": kind, "ok": ok, "text": text})+"\n")
    except OSError:
        pass


def send_record(text, packing, title):
    """Photo of the packing with the text as caption; plain text if that fails."""
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as d:
            png = render_png(packing, Path(d)/"packing.png", title)
            if send_photo(png, text):
                log("photo", True, text)
                return True
    except Exception:
        pass
    ok = send(text)
    log("text", ok, text)
    return ok


def setup(token):
    me = _api(token, "getMe")
    if not me.get("ok"):
        raise SystemExit("Telegram rejected the token")
    updates = _api(token, "getUpdates").get("result", [])
    chats = [u["message"]["chat"]["id"] for u in updates if "message" in u]
    if not chats:
        raise SystemExit(f"No messages to @{me['result']['username']} yet: send it /start, then run --setup again")
    CONFIG.write_text(json.dumps({"token": token, "chat_id": chats[-1]})+"\n")
    os.chmod(CONFIG, 0o600)
    print(f"saved {CONFIG} for chat {chats[-1]} (bot @{me['result']['username']})")
    print("test message sent" if send("Square packing: notifications for new records are on.") else "test message FAILED")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--setup":
        setup(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "--test-photo":
        n = int(sys.argv[2])
        f = CONFIG.parent/f"n{n}.txt"
        s = next(float(l.split("=")[1]) for l in f.read_text().splitlines() if l.startswith("# s ="))
        print("sent" if send_record(f"Square packing: test image for n={n}.", f, f"n = {n}   s = {s:.12f}") else "FAILED")
    elif sys.argv[1:] == ["--test"]:
        print("sent" if send("Square packing: test notification.") else "FAILED (is telegram.json configured?)")
    elif len(sys.argv) == 2:
        print("sent" if send(sys.argv[1]) else "FAILED")
    else:
        raise SystemExit(__doc__)
