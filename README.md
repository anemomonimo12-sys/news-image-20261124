# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/anemomonimo12-sys/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/anemomonimo12-sys/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A program that sums up the world news of Tuesday 24 November 2026 in one picture: a newspaper front page drawn by render.py (PIL) — masthead naming the day, six panels covering a US jury finding Huawei guilty of trade-secret theft and bank fraud, the Houthi drone strike on Riyadh's PIF tower, Ukraine's drone strikes on Russian ships, fourteen nations affirming the ICJ's Myanmar genocide ruling, Nvidia reinstating Jensen Huang and the market rally, and Iran's claim of four tankers hitting mines in the Strait of Hormuz — plus an "also today" strip. main.ts copies the finished entry.png to /output/entry.png byte for byte, deterministically, with no network.

## Run it

```sh
python3 render.py          # redraw entry.png
MAKEFUN_OUTPUT_DIR=/output node main.ts   # writes /output/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pqs0bqkp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
