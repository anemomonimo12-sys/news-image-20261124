# The World Today — Tuesday, 24 November 2026

A newspaper-style front page summing up the world news of Tuesday
24 November 2026 in a single 1024×1024 image, drawn with PIL.

Lead story: a US jury finds Huawei guilty of trade-secret theft and bank
fraud. Also covered: the Houthi drone strike on Riyadh's PIF tower,
Ukraine's drone strikes on Russian ships, fourteen nations affirming the
ICJ's Myanmar genocide ruling, Nvidia reinstating Jensen Huang and the
market rally, and Iran's claim of four tankers hitting mines in the
Strait of Hormuz — plus four more stories in the "Also today" strip.

## How to run

    python3 render.py        # writes entry.png (1024x1024, < 1 MiB)
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/

`main.ts` (Node 22, standard library only) is the entrypoint: it copies
`entry.png` unchanged to the output directory.
