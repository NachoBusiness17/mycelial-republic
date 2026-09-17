import fs from 'node:fs';
const dir = 'C:/Users/foste/Documents/projects/local_sovereign_agent/memory/corpus/electronics_canon';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const targets = [
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf', 'ADI_MT-001_SNR_6.02N_plus_1.76dB.pdf'],
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-032.pdf', 'ADI_MT-032_IdealVoltageFeedbackOpAmp.pdf'],
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf', 'ADI_MT-033_VoltageFeedbackOpAmpBasics.pdf'],
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-060.pdf', 'ADI_MT-060_InstrumentationAmplifier.pdf'],
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-061.pdf', 'ADI_MT-061_InAmpDCErrors.pdf'],
  ['https://www.analog.com/media/en/training-seminars/tutorials/MT-062.pdf', 'ADI_MT-062_InAmpNoise.pdf'],
  ['https://www.analog.com/media/en/training-seminars/design-handbooks/Op-Amp-Applications/Section1.pdf', 'ADI_OpAmpApplicationsHandbook_Sec1_OpAmpBasics_Jung.pdf'],
  ['https://www.analog.com/media/en/training-seminars/design-handbooks/Op-Amp-Applications/Section2.pdf', 'ADI_OpAmpApplicationsHandbook_Sec2_SpecialtyAmplifiers_Jung.pdf'],
  ['https://www.analog.com/media/en/training-seminars/design-handbooks/basic-linear-design/chapter1.pdf', 'ADI_BasicLinearDesign_Ch1_TheOpAmp.pdf'],
  ['https://www.analog.com/media/en/training-seminars/design-handbooks/Practical-Design-Techniques-Sensor-Signal/Section2.PDF', 'ADI_SensorSignalConditioning_Sec2_BridgeCircuits.pdf'],
  ['https://www.analog.com/media/en/training-seminars/design-handbooks/Practical-Design-Techniques-Sensor-Signal/Section3.PDF', 'ADI_SensorSignalConditioning_Sec3_Amplifiers.pdf'],
];
for (const [u, name] of targets) {
  try {
    const res = await fetch(u, { headers: { 'user-agent': UA, accept: 'application/pdf,*/*' }, redirect: 'follow' });
    const ab = await res.arrayBuffer();
    const buf = Buffer.from(ab);
    const sig = buf.subarray(0, 4).toString('ascii');
    console.log(name, res.status, buf.length, 'sig=' + sig);
    if (res.status === 200 && sig === '%PDF') fs.writeFileSync(dir + '/' + name, buf);
  } catch (e) {
    console.log(name, 'ERR', String(e).slice(0, 120));
  }
}
