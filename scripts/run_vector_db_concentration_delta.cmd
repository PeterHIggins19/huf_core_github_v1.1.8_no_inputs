@echo off
setlocal enabledelayedexpansion

REM run_vector_db_concentration_delta.cmd
REM Usage:
REM   scripts\run_vector_db_concentration_delta.cmd 0.02 0.08
REM Optional override input/output:
REM   set IN=cases\vector_db\inputs\retrieval.jsonl
REM   set OUT=out\vector_db_delta

set ROOT=%~dp0..
set PY=%ROOT%\.venv\Scripts\python.exe
if not exist "%PY%" (
  echo [err] Python not found: "%PY%"
  exit /b 1
)

if "%~1"=="" (
  echo [err] Provide tau A as first arg, e.g. 0.02
  exit /b 1
)
if "%~2"=="" (
  echo [err] Provide tau B as second arg, e.g. 0.08
  exit /b 1
)

set IN=%ROOT%\cases\vector_db\inputs\retrieval.jsonl
set OUT=%ROOT%\out\vector_db_delta
if not "%IN%"=="" if defined IN set IN=%ROOT%\%IN%
if not "%OUT%"=="" if defined OUT set OUT=%ROOT%\%OUT%

"%PY%" "%~dp0run_vector_db_concentration_delta.py" --in "%IN%" --out "%OUT%" --tau-a %1 --tau-b %2 --regime-field namespace
