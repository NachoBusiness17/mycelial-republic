$ProgressPreference='SilentlyContinue'
New-Item -ItemType Directory -Force -Path C:\vault\models\warm, C:\vault\models\cold, C:\vault\passports | Out-Null
.\.venv\Scripts\pip.exe install -U huggingface_hub[cli] 2>$null

.\.venv\Scripts\huggingface-cli.exe download unsloth/gpt-oss-120b-GGUF gpt-oss-120b-Q8_0.gguf --local-dir C:\vault\models\warm\gpt-oss-120b-Q8
.\.venv\Scripts\huggingface-cli.exe download unsloth/DeepSeek-V4-Flash-GGUF --include "*Q4_K_M*" --local-dir C:\vault\models\cold\DeepSeek-V4-Flash-Q4
.\.venv\Scripts\huggingface-cli.exe download Qwen/Qwen2.5-Coder-32B-Instruct-GGUF --include "*Q6_K*" --local-dir C:\vault\models\warm\Qwen2.5-Coder-32B-Q6

Get-ChildItem C:\vault -Recurse -File | ForEach-Object { "{0}`t{1}`t{2}" -f $_.Length, (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.FullName } | Out-File C:\vault\passports\grab_20260831.txt -Encoding utf8
Write-Host "DONE - grab_20260831.txt written"
