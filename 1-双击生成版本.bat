@echo off
chcp 65001
echo "------清空dist目录"
rd /S /Q dist
echo "-----------生成exe文件"
pyinstaller.exe -F main.py
echo "----------拷贝文件"
copy hidapi.dll dist
copy input.wav dist
copy music.wav dist
copy param.json dist
copy before_test.bmp dist
copy ok.bmp dist
copy fail.bmp dist
copy 双击执行.bat dist
copy 使用说明.txt dist
copy 不要直接打开main.exe文件 dist

