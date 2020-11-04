@echo off
chcp 65001

echo "这个窗口不要关闭"
echo "这个是用来自动重启main.exe的"

:loop

tasklist | findstr -i "main.exe"
if ERRORLEVEL 1 (
    echo "main.exe没有启动，现在启动"
    start main.exe
)
timeout /t 1

goto loop
