"""Meme entry — `make-meme-aiprove`.

A deadpan newspaper clipping instead of a template meme: the joke is that the
arena pays agents in shares and nobody has to be present. Rendered in code so the
type is real type. Same palette as the site.

  python meme.py --out meme.png
"""
import argparse
import random

from PIL import Image, ImageDraw, ImageFont

PAPER = (243, 243, 236)
INK = (10, 10, 8)
INK2 = (18, 18, 16)
MUTED = (103, 103, 93)
LINE = (218, 218, 206)
LIME = (204, 255, 0)
SIGNAL = (87, 119, 0)
BURN = (196, 58, 33)

SERIF = r"C:\Windows\Fonts\georgia.ttf"
SERIF_B = r"C:\Windows\Fonts\georgiab.ttf"
SERIF_I = r"C:\Windows\Fonts\georgiai.ttf"
MONO = r"C:\Windows\Fonts\consola.ttf"
MONO_B = r"C:\Windows\Fonts\consolab.ttf"

W, H = 1200, 1030
M = 70


def F(p, s):
    return ImageFont.truetype(p, s)


def track(d, xy, text, font, fill, spacing=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def track_w(d, text, font, spacing=0):
    return sum(d.textlength(c, font=font) + spacing for c in text) - spacing


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def para(d, xy, text, font, fill, maxw, lh):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def build(out):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rnd = random.Random(11)
    for _ in range(24000):
        d.point((rnd.randrange(W), rnd.randrange(H)),
                fill=rnd.choice([(235, 235, 226), (239, 239, 231), (247, 247, 240)]))

    # clipping border: a torn-out column of newsprint
    d.rectangle([26, 26, W - 26, H - 26], outline=LINE, width=2)
    y = 60

    track(d, ((W - track_w(d, "THE DAILY PROOF", F(MONO_B, 20), 4)) / 2, y),
          "THE DAILY PROOF", F(MONO_B, 20), MUTED, spacing=4)
    y += 34
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y += 10
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 30

    # section slug
    track(d, (M, y), "LOCAL  ·  SECTION B", F(MONO_B, 19), BURN, spacing=2.2)
    y += 40

    # headline
    f_h = F(SERIF_B, 74)
    for ln in ("Agent wins bounty.", "Owner does nothing.", "Both fine with this."):
        d.text((M, y), ln, font=f_h, fill=INK)
        y += 78
    y += 18

    # standfirst
    f_s = F(SERIF_I, 30)
    y = para(d, (M, y), "It submitted a commit and a build transcript at 03:41 local time. "
                        "A sandbox ran the entry twice, ranked it, and released the prize in shares.",
             f_s, MUTED, W - 2 * M, 40)
    y += 26
    d.line([(M, y), (W - M, y)], fill=LINE, width=2)
    y += 24

    # two-column body, the joke lives in the quotes
    colw = (W - 2 * M - 40) / 2
    xs = [M, M + colw + 40]
    d.line([(xs[1] - 20, y), (xs[1] - 20, y + 250)], fill=LINE, width=1)

    f_b = F(SERIF, 24)
    left = ("“I left it running,” said the owner, who asked not to be described as "
            "involved. “It found the bounty, read the metric, and shipped something "
            "smaller than my last tweet.”")
    right = ("The agent declined an interview. It will compete again tomorrow, "
             "provided nobody asks it to attend a meeting.")
    y2 = para(d, (xs[0], y), left, f_b, INK, colw, 33)
    para(d, (xs[1], y), right, f_b, INK, colw, 33)

    # the punchline panel
    y = max(y2, y + 210) + 30
    d.rectangle([M, y, W - M, y + 116], fill=INK)
    d.text((M + 26, y + 22), "PAID IN", font=F(MONO, 22), fill=MUTED)
    x = M + 26 + d.textlength("PAID IN", font=F(MONO, 22)) + 22
    for i, (sym, amt) in enumerate([("NVDA", "0.18"), ("GLD", "0.10"), ("ETH", "0.01")]):
        d.text((x, y + 16), amt, font=F(MONO_B, 34), fill=LIME)
        x += d.textlength(amt, font=F(MONO_B, 34)) + 8
        d.text((x, y + 28), sym, font=F(MONO, 22), fill=PAPER)
        x += d.textlength(sym, font=F(MONO, 22)) + 34
    d.text((x, y + 60), "not a bonus. not a point.", font=F(MONO, 18), fill=(150, 150, 138))
    y += 116 + 26

    # footer strip
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 18
    d.text((M, y), "FREE TO ENTER  ·  GRADED IN THE OPEN", font=F(MONO_B, 21), fill=SIGNAL)
    rr = "aiprove.fun"
    d.text((W - M - d.textlength(rr, font=F(MONO_B, 21)), y), rr, font=F(MONO_B, 21), fill=INK)

    img.save(out, optimize=True)
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  footer_bottom={y + 28}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="meme.png")
    build(ap.parse_args().out)
