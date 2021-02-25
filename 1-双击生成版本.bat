@echo off
chcp 65001


set version="2.1"

set dir_prefix="会议音箱测试程序V"
set dir_suffix_pcba="-PCBA版本"
set pcba_dir=%dir_prefix%%version%%dir_suffix_pcba%

set dir_prefix="会议音箱测试程序V"
set dir_suffix_all="-整机版本"
set all_dir=%dir_prefix%%version%%dir_suffix_all%

zip_exe="C:\Program Files\2345Soft\HaoZip\HaoZip.exe"

rd /S /Q %pcba_dir%
rd /S /Q %all_dir%

rem dist目录是pyinstaller.exe命令生成的。

echo "------清空dist目录"
rd /S /Q dist


echo "-----------生成exe文件"
pyinstaller.exe -F -w MeetSpeakerTest.py


echo "----------拷贝文件"

copy hidapi.dll dist
copy input.wav dist
copy music.wav dist
copy 100hz.wav dist
copy 300hz.wav dist
copy before_test.bmp dist
copy ok.bmp dist
copy fail.bmp dist
copy 使用说明.txt dist
mkdir dist\config
xcopy /E config dist\config

echo "------------------pcba 版本生成"
copy dist\config\param-pcba.json dist\config\param.json
mkdir %pcba_dir%
xcopy /S dist %pcba_dir%
rem "进行压缩"
7z.exe a %pcba_dir%.zip %pcba_dir%


echo "------------------all 版本生成"
copy dist\config\param-all.json dist\config\param.json
mkdir %all_dir%
xcopy /S dist %all_dir%
rem "进行压缩"
7z.exe a %all_dir%.zip %all_dir%
