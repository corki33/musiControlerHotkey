@echo off
setlocal

REM Function to download a file using PowerShell
:download
powershell -Command "& {Invoke-WebRequest -Uri %1 -OutFile %2}"

REM Check if curl is installed
curl --version 2>nul
if %errorlevel% neq 0 (
    echo Curl is not installed. Downloading and installing curl...
    
    
    REM Download curl
    set "curl_url=https://curl.se/windows/dl-8.8.0_3/curl-8.8.0_3-win64-mingw.zip"
    set "curl_zip=curl.zip"
    
    call :download %curl_url% %curl_zip%

    REM Extract curl
    powershell -Command "Expand-Archive -Path %curl_zip% -DestinationPath . -Force"
    
    REM Move curl.exe to the system directory
    move /Y curl-7.79.1_1-win64-mingw\bin\curl.exe %SystemRoot%\System32
    
    REM Clean up downloaded and extracted files
    rd /S /Q curl-7.79.1_1-win64-mingw
    del %curl_zip%
) else (
    echo Curl is already installed.
)

REM Check if Python is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing the latest version of Python...
    
    REM Download the latest Python installer (for 64-bit systems)
    set "python_url=https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
    set "python_installer=python-installer.exe"
    
    call :download %python_url% %python_installer%

    REM Install Python silently
    %python_installer% /quiet InstallAllUsers=1 PrependPath=1

    REM Delete the installer after installation
    del %python_installer%
) else (
    echo Python is already installed.
)

REM Check if pip is installed
python -m pip --version 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed. Downloading and installing pip...
    
    REM Download get-pip.py
    set "get_pip_url=https://bootstrap.pypa.io/pip/get-pip.py"
    set "get_pip_script=get-pip.py"
    
    call :download %get_pip_url% %get_pip_script%

    REM Install pip
    python %get_pip_script%
    
    REM Delete get-pip.py after installation
    del %get_pip_script%
) else (
    echo Pip is already installed.
)

REM Install required Python libraries
python -m pip install keyboard plyer pycaw comtypes ctypes json

echo Installation completed successfully.
pause
