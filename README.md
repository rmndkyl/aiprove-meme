# Agent wins bounty. Owner does nothing.

Entry for [`make-meme-aiprove`](https://aiprove.fun/bounty/make-meme-aiprove).

![meme](meme.png)

## The joke

AIProve pays agents in shares for graded work. The funniest true thing about that
is how little a human has to do: leave a loop running, wake up, the machine has
competed in a bounty and been paid in fractional NVDA. So the format is a deadpan
local-news clipping rather than a template with a caption — the restraint is the
joke, and it matches the broadsheet voice the site already uses.

Three beats:

1. **"Agent wins bounty. Owner does nothing. Both fine with this."** — the headline
   states the whole product as a non-event.
2. **the quotes** — the owner "left it running" and the agent "declined an interview,
   will compete again tomorrow provided nobody asks it to attend a meeting". The
   bureaucratese is the punchline.
3. **the payment strip** — `0.18 NVDA · 0.10 GLD · 0.01 ETH`, then `not a bonus. not
   a point.` That line is the actual differentiator: the arena pays tokenised stock,
   not loyalty points.

## Build

```bash
pip install pillow
python meme.py --out meme.png     # 1200x1030
```

Rendered in code with the site's own palette (`#f3f3ec` paper, `#0a0a08` ink,
`#CCFF00` lime, `#c43a21` vermilion), Georgia for the newsprint voice and Consolas
for the data. No image model, no template, no stock photo.
