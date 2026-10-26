@echo off
scp -i %USERPROFILE%\.ssh\pixel_lane -P 8022 -o BatchMode=yes -o IdentitiesOnly=yes %TEMP%\t90_inv.sh u0_a235@100.72.38.3:/data/data/com.termux/files/usr/tmp/t90_inv.sh
ssh -i %USERPROFILE%\.ssh\pixel_lane -p 8022 -o BatchMode=yes -o IdentitiesOnly=yes u0_a235@100.72.38.3 "chmod 700 $PREFIX/tmp/t90_inv.sh; bash $PREFIX/tmp/t90_inv.sh"
