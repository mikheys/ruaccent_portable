@echo off
setlocal

echo Downloading Python...
if not exist python-3.11.9-embed-amd64.zip (
    bitsadmin /transfer myDownloadJob /download /priority normal https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip %cd%\python-3.11.9-embed-amd64.zip
)

echo Unpacking Python...
if not exist python (
    tar -xf python-3.11.9-embed-amd64.zip -C python
)

echo Creating virtual environment...
if not exist .venv (
    python\python.exe -m venv .venv
)

echo Installing dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo Installation complete.
pause