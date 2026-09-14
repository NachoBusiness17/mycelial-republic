// B5 packer v2: raw gray frames -> bit-RLE + consecutive-dedup -> base64 embed
// Usage: node pack_frames.mjs < seg.raw  (writes frames_embed.txt, stats to stderr)
// Layout: px = concatenation of per-unique-frame RLE byte strings.
//   Each frame RLE: alternating run lengths of 0-bit then 1-bit, starting with the
//   0-run (may be 0 long), total bits = W*H. Runs are LEB128 varints (7 bits/byte).
import fs from 'fs';

const W = 96, H = 72, FPS = 30;
const STRIDE = W >> 3;
const FPB = STRIDE * H;
const BITS = W * H;

const raw = fs.readFileSync(0);
const nFrames = Math.floor(raw.length / (W * H));

function varint(n, out) {
  while (n >= 0x80) { out.push((n & 0x7f) | 0x80); n >>>= 7; }
  out.push(n);
}
function rleFrame(packed) {
  const out = [];
  let runBit = 0, runLen = 0;
  for (let i = 0; i < BITS; i++) {
    const bit = (packed[i >> 3] >> (7 - (i & 7))) & 1;
    if (bit === runBit) runLen++;
    else { varint(runLen, out); runBit = bit; runLen = 1; }
  }
  varint(runLen, out);
  return Buffer.from(out);
}

const uniq = []; const map = new Map(); const rep = [];
let cur = -1, curCount = 0, lastKey = null;
for (let f = 0; f < nFrames; f++) {
  const off = f * W * H;
  const packed = Buffer.alloc(FPB);
  for (let y = 0; y < H; y++) {
    const ro = y * STRIDE, go = y * W + off;
    for (let xb = 0; xb < STRIDE; xb++) {
      let b = 0;
      for (let k = 0; k < 8; k++) if (raw[go + xb * 8 + k] >= 128) b |= (0x80 >> k);
      packed[ro + xb] = b;
    }
  }
  const key = packed.toString('hex');
  if (key === lastKey) { curCount++; continue; }
  if (cur >= 0) rep.push(cur, curCount);
  let idx = map.get(key);
  if (idx === undefined) { idx = uniq.length; map.set(key, idx); uniq.push(rleFrame(packed)); }
  cur = idx; curCount = 1; lastKey = key;
}
if (cur >= 0) rep.push(cur, curCount);

const px = Buffer.concat(uniq);
const repBuf = Buffer.alloc(rep.length * 2);
for (let i = 0; i < rep.length; i++) repBuf.writeUInt16LE(rep[i], i * 2);

const out = { w: W, h: H, fps: FPS, n: nFrames, uniq: uniq.length, bytes: px.length, px: px.toString('base64'), rep: repBuf.toString('base64') };
fs.writeFileSync(new URL('./frames_embed.txt', import.meta.url), JSON.stringify(out));
console.error(`frames=${nFrames} uniq=${uniq.length} rleBytes=${px.length} px_b64=${Math.ceil(px.length * 4 / 3)} repB64=${Math.ceil(repBuf.length * 4 / 3)}`);
