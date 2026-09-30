#!/usr/bin/env python3
"""Generate a multi-size favicon.ico (pure stdlib, no Pillow).
Design: forest-green rounded square + white graduation-cap emblem,
matching the site's 'forest' palette and PTIC academic branding.
Writes static/img/favicon.ico and a 256px preview PNG.
"""
import struct, zlib, math, os

OUT = "/storage/Users/currentUser/WorkBuddy/hugo-apero/static/img"
GREEN = (47, 125, 95, 255)     # #2f7d5f
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [CLEAR] * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = c

    def rounded_rect(self, x0, y0, x1, y1, r, c):
        for y in range(int(y0), int(y1) + 1):
            dy = 0
            if y < y0 + r:
                dy = y0 + r - y
            elif y > y1 - r:
                dy = y - (y1 - r)
            for x in range(int(x0), int(x1) + 1):
                dx = 0
                if x < x0 + r:
                    dx = x0 + r - x
                elif x > x1 - r:
                    dx = x - (x1 - r)
                if dx * dx + dy * dy <= r * r:
                    self.px[y * self.w + x] = c

    def poly(self, pts, c):
        ys = [p[1] for p in pts]
        ymin = max(0, int(math.floor(min(ys))))
        ymax = min(self.h - 1, int(math.ceil(max(ys))))
        n = len(pts)
        for y in range(ymin, ymax + 1):
            xs = []
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if y1 == y2:
                    continue
                if (y >= y1 and y < y2) or (y >= y2 and y < y1):
                    t = (y - y1) / (y2 - y1)
                    xs.append(x1 + t * (x2 - x1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(math.ceil(xs[i])), int(math.floor(xs[i + 1])) + 1):
                    self.set(x, y, c)

    def circle(self, cx, cy, rad, c):
        for y in range(int(cy - rad), int(cy + rad) + 1):
            for x in range(int(cx - rad), int(cx + rad) + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad:
                    self.set(x, y, c)


def downsample(src, ss, tw, th):
    out = []
    for y in range(th):
        for x in range(tw):
            r = g = b = a = 0
            for dy in range(ss):
                base = (y * ss + dy) * src.w + x * ss
                for dx in range(ss):
                    pr, pg, pb, pa = src.px[base + dx]
                    r += pr * pa; g += pg * pa; b += pb * pa; a += pa
            cnt = ss * ss
            if a == 0:
                out.append(CLEAR)
            else:
                out.append((round(r / a), round(g / a), round(b / a), a // cnt))
    return out


def png_bytes(w, h, pixels):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        row = y * w
        for x in range(w):
            r, g, b, a = pixels[row + x]
            raw += bytes((r, g, b, a))

    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + \
               struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def draw(S):
    c = Canvas(S, S)
    pad = max(1, int(S * 0.02))
    c.rounded_rect(pad, pad, S - 1 - pad, S - 1 - pad, int(S * 0.22), GREEN)
    cx, cy = S / 2.0, S * 0.46
    a, b = S * 0.34, S * 0.20
    c.poly([(cx, cy - b), (cx + a, cy), (cx, cy + b), (cx - a, cy)], WHITE)      # cap top
    tw_, bw_ = a * 0.60, a * 0.42
    c.poly([(cx - tw_, cy + b * 0.55), (cx + tw_, cy + b * 0.55),
            (cx + bw_, cy + b * 1.35), (cx - bw_, cy + b * 1.35)], WHITE)        # cap base
    c.circle(cx + a * 1.02, cy + b * 0.35, S * 0.028, WHITE)                     # tassel
    return c


def main():
    ss = 4
    sizes = [16, 32, 48, 64, 128, 256]
    pngs = {}
    for s in sizes:
        pngs[s] = png_bytes(s, s, downsample(draw(s * ss), ss, s, s))
    n = len(sizes)
    header = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    entries = b""
    data = b""
    for s in sizes:
        png = pngs[s]
        wb = hb = 0 if s >= 256 else s
        entries += struct.pack("<BBBBHHII", wb, hb, 0, 0, 1, 32, len(png), offset + len(data))
        data += png
    with open(os.path.join(OUT, "favicon.ico"), "wb") as f:
        f.write(header + entries + data)
    with open(os.path.join(OUT, "favicon-preview.png"), "wb") as f:
        f.write(pngs[256])
    print("favicon.ico written:", os.path.getsize(os.path.join(OUT, "favicon.ico")), "bytes; sizes", sizes)


if __name__ == "__main__":
    main()
