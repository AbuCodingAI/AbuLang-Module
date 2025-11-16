@echo off
echo Cleaning up test files...

REM Delete test .abu files
del /Q test_*.abu 2>nul
del /Q game_*.abu 2>nul

REM Delete test data files
del /Q test_*.txt 2>nul
del /Q test_*.yaml 2>nul
del /Q test_*.json 2>nul
del /Q test_*.csv 2>nul
del /Q test_*.log 2>nul
del /Q test_*.py 2>nul

REM Delete v_ files
del /Q v_*.txt 2>nul
del /Q v_*.yaml 2>nul
del /Q v_*.json 2>nul
del /Q v_*.csv 2>nul

REM Delete other test files
del /Q mydata.abudata 2>nul
del /Q mylog.abulog 2>nul

echo Done! All test files deleted.
pause
