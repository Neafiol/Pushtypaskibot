@echo off
set executable=C:\Users\Administrator\Downloads\Postupaski_bot\Postupashky\telsent.exe
set executable1=C:\Users\Administrator\Downloads\Postupaski_bot\Postupashky\Sender.exe
set executable2=C:\Users\Administrator\Downloads\Postupaski_bot\Postupashky\battle.exe
set process=telsent.exe
set process1=Sender.exe
set process2=battle.exe


:begin
tasklist |>nul findstr /b /l /i /c:%process% || start "" "%executable%"
tasklist |>nul findstr /b /l /i /c:%process1% || start "" "%executable1%"
tasklist |>nul findstr /b /l /i /c:%process1% || start "" "%executable2%"
timeout /t 3 /nobreak >nul
goto :begin