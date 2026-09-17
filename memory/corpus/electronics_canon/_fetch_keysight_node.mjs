import fs from 'node:fs';
const dir = 'C:/Users/foste/Documents/projects/local_sovereign_agent/memory/corpus/electronics_canon';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const targets = [
  ['https://www.keysight.com/us/en/assets/701-0680/application-notes/5989-5732.pdf', 'Keysight_5989-5732EN_Evaluating_Oscilloscope_Sample_Quality.pdf'],
  ['https://www.keysight.com/ch/de/assets/7018-06505/white-papers/5992-3675.pdf', 'Keysight_5992-3675_ADC_Bits_ENOB.pdf'],
];
for (const [u, name] of targets) {
  try {
    const res = await fetch(u, { headers: { 'user-agent': UA, accept: 'application/pdf,application/octet-stream,*/*', 'accept-language': 'en-US,en;q=0.9' }, redirect: 'follow' });
    const buf = Buffer.from(await res.arrayBuffer());
    const sig = buf.subarray(0, 4).toString('ascii');
    console.log(name, res.status, buf.length, 'sig=' + sig);
    if (res.status === 200 && sig === '%PDF') fs.writeFileSync(dir + '/' + name, buf);
  } catch (e) { console.log(name, 'ERR', String(e).slice(0, 100)); }
}
