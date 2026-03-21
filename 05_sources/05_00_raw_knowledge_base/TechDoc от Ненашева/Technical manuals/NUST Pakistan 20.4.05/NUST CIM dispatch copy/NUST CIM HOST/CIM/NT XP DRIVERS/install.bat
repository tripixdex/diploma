@echo off
echo.
echo About to install SoftLokII NT dongle drivers
echo.
echo Press CTRL-C to abort or
pause
echo.
copy softlok.sys c:\winnt\system32\drivers
regini softlok.ini
echo.
echo You must restart your computer in order for this new driver to become active
echo.
pause