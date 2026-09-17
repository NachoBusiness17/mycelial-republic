import fs from 'node:fs';
const dir = 'C:/Users/foste/Documents/projects/local_sovereign_agent/memory/corpus/electronics_canon';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const targets = [
  ['https://www.keysight.com/ch/de/assets/7018-06505/white-papers/5992-3675.pdf', 'Keysight_5992-3675_ADC_Bits_and_EffectiveNumberOfBits.pdf'],
  ['https://www.keysight.com/us/en/assets/701-0680/application-notes/5989-5732.pdf', 'Keysight_5989-5732EN_Evaluating_Oscilloscope_Sample_Quality.pdf'],
  ['https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P6wbSAC', 'NI_cDAQ_EffectiveNumberOfBits_ENOB_KB.html'],
  ['https://learn.sparkfun.com/tutorials/qwiic-12-bit-adc-hookup-guide', 'SparkFun_Qwiic_12Bit_ADC_ADS1015_HookupGuide.html'],
  ['https://learn.sparkfun.com/tutorials/qwiic-mux-hookup-guide', 'SparkFun_Qwiic_Mux_TCA9548A_HookupGuide.html'],
  ['https://www.allaboutcircuits.com/textbook/', 'AAC_Textbook_Index.html'],
  ['https://www.allaboutcircuits.com/textbook/direct-current/', 'AAC_Textbook_Vol1_DirectCurrent_Index.html'],
  ['https://www.allaboutcircuits.com/textbook/semiconductors/', 'AAC_Textbook_Vol3_Semiconductors_Index.html'],
];
for (const [u, name] of targets) {
  try {
    const res = await fetch(u, { headers: { 'user-agent': UA, accept: '*/*' }, redirect: 'follow' });
    const ab = await res.arrayBuffer();
    const buf = Buffer.from(ab);
    const head = buf.subarray(0, 200).toString('ascii', 0, 200);
    const isPdf = buf.subarray(0, 4).toString('ascii') === '%PDF';
    const isHtml = head.includes('<') || head.includes('html');
    console.log(name, res.status, buf.length, 'pdf=' + isPdf, 'final=' + res.url.slice(0, 90));
    if (res.status === 200 && buf.length > 2000 && (isPdf || isHtml)) fs.writeFileSync(dir + '/' + name, buf);
    else console.log('  dropped');
  } catch (e) {
    console.log(name, 'ERR', String(e).slice(0, 120));
  }
}
