@echo off
setlocal enabledelayedexpansion

REM run_print_huf_summary.cmd
REM Optional arg: output folder (default: out\planck70)

set ROOT=%~dp0..
set PY=%ROOT%\.venv\Scripts\python.exe
if not exist "%PY%" (
  echo [err] Python not found: "%PY%"
  exit /b 1
)

set OUT=%ROOT%\out\planck70
if not "%~1"=="" set OUT=%~1

"%PY%" "%~dp0print_huf_summary.py" --out "%OUT%"
