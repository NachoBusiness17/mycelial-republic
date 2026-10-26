@echo off
ssh -i %USERPROFILE%\.ssh\pixel_lane -p 8022 -o BatchMode=yes -o IdentitiesOnly=yes u0_a235@100.72.38.3 "bash $PREFIX/tmp/lkm_scan.sh"
