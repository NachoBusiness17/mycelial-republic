$ProgressPreference = 'SilentlyContinue'
$dir = 'C:/Users/foste/Documents/projects/local_sovereign_agent/memory/corpus/electronics_canon'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

$targets = @(
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf'; o='ADI_MT-001_SNR_6.02N_plus_1.76dB.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-032.pdf'; o='ADI_MT-032_IdealVoltageFeedbackOpAmp.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf'; o='ADI_MT-033_VoltageFeedbackOpAmpBasics.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-060.pdf'; o='ADI_MT-060_InstrumentationAmplifier.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-061.pdf'; o='ADI_MT-061_InAmpDCErrors.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/tutorials/MT-062.pdf'; o='ADI_MT-062_InAmpNoise.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/Op-Amp-Applications/Section1.pdf'; o='ADI_OpAmpApplicationsHandbook_Sec1_OpAmpBasics_Jung.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/Op-Amp-Applications/Section2.pdf'; o='ADI_OpAmpApplicationsHandbook_Sec2_SpecialtyAmplifiers_Jung.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/basic-linear-design/chapter1.pdf'; o='ADI_BasicLinearDesign_Ch1_TheOpAmp.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/Practical-Design-Techniques-Sensor-Signal/Outline.PDF'; o='ADI_SensorSignalConditioning_Outline.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/Practical-Design-Techniques-Sensor-Signal/Section2.PDF'; o='ADI_SensorSignalConditioning_Sec2_BridgeCircuits.pdf'},
  @{u='https://www.analog.com/media/en/training-seminars/design-handbooks/Practical-Design-Techniques-Sensor-Signal/Section3.PDF'; o='ADI_SensorSignalConditioning_Sec3_Amplifiers.pdf'}
)

foreach ($t in $targets) {
  $out = Join-Path $dir $t.o
  try {
    Invoke-WebRequest -Uri $t.u -OutFile $out -TimeoutSec 120 -UserAgent $ua
    $bytes = [System.IO.File]::ReadAllBytes($out)[0..3]
    $sig = [System.Text.Encoding]::ASCII.GetString($bytes)
    $len = (Get-Item $out).Length
    Write-Host ($t.o + ' OK ' + $len + ' sig=' + $sig)
    if ($sig -ne '%PDF') { Remove-Item $out -Force; Write-Host ('  dropped (not PDF)') }
  } catch {
    Write-Host ($t.o + ' FAIL ' + $_.Exception.Message)
    if (Test-Path $out) { Remove-Item $out -Force }
  }
}
