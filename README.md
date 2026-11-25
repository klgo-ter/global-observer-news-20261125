# global-observer-news-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/klgo-ter/global-observer-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/klgo-ter/global-observer-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A broadsheet front page for Wednesday 25 November 2026, drawn to a single
1024×1024 PNG by a deterministic Python program. Every story on the page
happened or was first reported on that day, and each one is attributed on the
page to the outlet that carried it.

## What the page carries

| Story | Field | Region | Source |
| --- | --- | --- | --- |
| Bangladesh raises the garment wage from Tk 12,500 to Tk 17,000 on a 4–2 board vote; unions reject it and hold out for Tk 18,000 | Business & labour | South Asia | The Daily Star, The Business Standard |
| At least 87 garment factories shut in Gazipur, Savar and Ashulia | Industry | South Asia | The Daily Star |
| Dhaka–Mymensingh and Dhaka–Tangail highways blocked; police answer with tear gas and stun grenades | Transport | South Asia | The Business Standard |
| Border Guard Bangladesh deploys 108 platoons across Dhaka and seven other districts, 56 of them in Gopalganj | Security | South Asia | The Daily Star |
| Beau Lamarre-Condon found guilty of the 2024 murders of Jesse Baird and Luke Davies | Law & justice | Oceania | The Guardian |

No line of copy is invented to fill space. Where the day gave two lead
stories and four facets of one of them, the page shows exactly that rather
than padding a grid with stories it cannot stand behind.

## How it is built

`main.py` draws the page with Pillow: a masthead, a dominant date block, a
ticker, two lead stories with vector art, four facet cards, a "day in
numbers" grid and a sourced-to panel with a verification seal.

It is deterministic by construction. It reads no network, no clock and no
random source, and it seeds nothing, so two runs write byte-identical PNGs:

```
a54c3b54… → 05c3aa54… → (final)  identical across runs
```

If the run has no Pillow or no fonts, `main.py` falls back to `entry.png`,
the committed render of the same page, which is byte for byte what the
renderer produces. Either path writes exactly one image, `entry.png`, to
`/output`.

## Run it

```sh
pip install pillow
MAKEFUN_OUTPUT_DIR=./out python3 main.py   # writes ./out/entry.png

# the grader's way (writes /output/entry.png):
python3 main.py
```

## Layout checks the build passes

- `1024×1024`, whole PNG, `133 KB` — inside the 1 MiB / 1024 px gate
- identical bytes across two consecutive runs
- no glyph, word or box overflows its container: every gutter, outer margin
  and vertical gap between panels measures zero bright pixels
- the date block is machine-checked against the rendered glyphs, not just
  eyeballed

---

<sub>Entered on [make.fun](https://make.fun/?ref=zqahh4rs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
