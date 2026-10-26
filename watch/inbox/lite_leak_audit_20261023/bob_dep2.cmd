@echo off
scp -i %USERPROFILE%\.ssh\pixel_lane -P 8022 -o BatchMode=yes -o IdentitiesOnly=yes %TEMP%\lkm_body.py %TEMP%\t90_scan.sh u0_a235@100.72.38.3:/data/data/com.termux/files/usr/tmp/
ssh -i %USERPROFILE%\.ssh\pixel_lane -p 8022 -o BatchMode=yes -o IdentitiesOnly=yes u0_a235@100.72.38.3 "chmod 700 $PREFIX/tmp/lkm_body.py $PREFIX/tmp/lkm_scan.sh; mv -f $PREFIX/tmp/t90_scan.sh $PREFIX/tmp/lkm_scan.sh"
