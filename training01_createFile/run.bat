@echo off
cl /Zi /Od /INCREMENTAL:NO /DEBUG:Yes create_file_win32.c user32.lib
if %ERRORLEVEL% == 0 (
  create_file_win32.exe
)