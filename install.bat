@echo off
setlocal

echo =================================================================
echo Step 1: Downloading portable Python 3.11.9
echo =================================================================
if not exist python-3.11.9-embed-amd64.zip (
    bitsadmin /transfer pythonDownloadJob /download /priority normal https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip %cd%\python-3.11.9-embed-amd64.zip
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
echo Step 3: Configuring Python to find its standard library
echo =================================================================
(echo python311.zip) > python\python311._pth
(echo .) >> python\python311._pth
(echo import site) >> python\python311._pth
echo Python configured successfully.

echo.
echo =================================================================
echo Step 4: Downloading and installing pip (package manager)
echo =================================================================
if not exist get-pip.py (
    bitsadmin /transfer pipDownloadJob /download /priority normal https://bootstrap.pypa.io/get-pip.py %cd%\get-pip.py
) else (
    echo get-pip.py already downloaded.
)
echo Installing pip...
python\python.exe get-pip.py

echo.
echo =================================================================
echo Step 5: Installing required libraries from requirements.txt
echo =================================================================
python\Scripts\pip.exe install -r requirements.txt

echo.
echo =================================================================
echo Step 6: Cleaning up installation files
echo =================================================================
del get-pip.py
del python-3.11.9-embed-amd64.zip
echo Cleanup complete.

echo.
echo =================================================================
echo Installation complete! You can now run the application using run.bat
echo =================================================================
pause