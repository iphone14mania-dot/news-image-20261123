import { copyFileSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}
const src = join(import.meta.dirname, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png is missing next to main.ts");
}
// Sanity check: entry.png must be a real PNG before we hand it to the grader.
const head = readFileSync(src);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (head.length < 8 || !head.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png does not start with the PNG magic bytes");
}
copyFileSync(src, join(outDir, "entry.png"));
