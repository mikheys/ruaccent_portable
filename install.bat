@echo off
setlocal

echo =================================================================
echo Step 1: Downloading portable Python 3.11.9
echo =================================================================
if not exist python-3.11.9-embed-amd64.zip (
    bitsadmin /transfer myDownloadJob /download /priority normal https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip %cd%\python-3.11.9-embed-amd64.zip
) else (
    echo Python archive already downloaded.
)

echo.
echo =================================================================
echo Step 2: Unpacking Python
echo =================================================================
if not exist python (
    echo Creating 'python' directory...
    mkdir python
    echo Extracting files from the archive...
    tar -xf python-3.11.9-embed-amd64.zip -C python
) else (
    echo Python directory already exists.
)

echo.
echo =================================================================
echo Step 3: Configuring Python to enable venv and pip
echo =================================================================
(echo python311.zip) > python\python311._pth
(echo .) >> python\python311._pth
(echo import site) >> python\python311._pth
echo Python configured.

echo.
echo =================================================================
echo Step 4: Creating a virtual environment in .venv
echo =================================================================
if not exist .venv (
    python\python.exe -m venv .venv
) else (
    echo Virtual environment '.venv' already exists.
)

echo.
echo =================================================================
echo Step 5: Installing required libraries from requirements.txt
echo =================================================================
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo =================================================================
echo Installation complete! You can now run the application using run.bat
echo =================================================================
pause