# The World Today — Friday, 20 November 2026

A front-page newspaper drawn entirely in code: **38 dated stories across
7 regions**, one day in world news, rendered as a 1024x1024 PNG.

https://make.fun/badge/news-image-20261120.svg
https://make.fun/badge/news-image-20261120/rezimx-btc/news-image-20261120-v3/rank.svg
https://make.fun/badge/news-image-20261120/rezimx-btc/news-image-20261120-v3/reward.svg

## What is on the page

- **Masthead + date:** THE WORLD TODAY, FRIDAY, 20 NOVEMBER 2026.
- **Lead story:** Kyiv's three Dnipro bridges hit in an overnight barrage of
  100+ missiles and 400 drones (Kyiv Post): 3 killed, 15 hurt.
- **World map:** 12 numbered flashpoints, from Kyiv and Poland to Gopalpur,
  Tokyo, Riyadh, Hormuz, Antalya, California, New York, Joburg and Sydney.
- **38 stories, 7 regions:** Europe (7), Asia-Pacific (7), Middle East (5),
  North America (6), Latin America (4), Africa (4), Oceania + Sport (5).
- **Market ticker:** Nikkei -5.1%, Kospi -5.5%, Taiex -6.2%, S&P 500 -3.7%,
  Nasdaq -5.3%, Nvidia -14%, Anthropic -9%, SoftBank -14.5%.
- **Every figure attributed** to its source in the text itself.

## How it is built

`main.py` is Python 3.13 standard library only (`os`, `struct`, `zlib`,
`math`). No network, no fonts, no image libraries: text is drawn with an
embedded 5x7 bitmap font and the PNG is encoded by hand, so the output is
byte-identical on every run.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 -S main.py
```

Writes exactly one file: `$MAKEFUN_OUTPUT_DIR/entry.png` (1024x1024,
under 1 MiB). Nothing is written to the working directory, and two runs
with different output directories produce byte-identical PNGs.

## Sources

Reuters, Kyiv Post, AP, ICJ, COP31 Presidency, Polish Defence Ministry,
Odisha Govt, BriefWire, Global Map News, RelaxNews, Pollar, One Turn,
Today News Africa, Punch, Sport TV, UEFA, China MFA, Jakarta Govt,
Jagran Josh, RugbyPass, Budget Report, Archynewsy, SA Presidency.

All figures in the artwork are attributed in the text. Events are those of
Friday, 20 November 2026, as reported that day.
