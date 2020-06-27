@ECHO OFF
REM echo %~dp0

del /Q /S build
python.exe -m PyInstaller q1a2b.spec

move /y dist\q1a2b.exe .