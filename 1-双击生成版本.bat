@echo off
chcp 65001

echo "-----------生成exe文件"
pyinstaller.exe -F main.py
echo "----------拷贝文件"
copy hidapi.dll dist
copy input.wav dist
copy music.wav dist
