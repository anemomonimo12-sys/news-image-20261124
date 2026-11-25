// Entry for make.fun's "Sum up 24 November's world news in one image".
//
// The picture is entry.png next to this file: a front page of Tuesday
// 24 November 2026, drawn by render.py (kept in this repository so the
// image can be reproduced from its source). This program only has to
// deliver those exact bytes to the output directory, unchanged.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

// Fail loudly if the source is not a PNG at all, before copying anything.
const magic = readFileSync(source).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!magic.equals(pngMagic)) {
  throw new Error('entry.png does not start with the PNG signature');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// The gate accepts a whole PNG of at most 1 MiB. Refuse to hand over a
// file that is not the same size as the source, or that is too large.
const delivered = statSync(target).size;
if (delivered !== statSync(source).size || delivered > 1_048_576) {
  throw new Error(
    `entry.png copy is ${delivered} bytes, expected the source size within 1 MiB`,
  );
}
