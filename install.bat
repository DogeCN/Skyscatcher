@echo off
set bin="dist\Skyscatcher\bin\main.exe"
set ins=dist\installed\main.exe
pyinstaller main.spec --noconfirm
echo 99997 INFO: Updating %bin%
del >nul 2>nul /f %bin%
copy >nul %ins% %bin%
echo 99998 INFO: Compressing %bin%
dist\upx >nul --force %bin%
echo 99999 INFO: Completed.
