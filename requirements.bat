@echo off
setlocal

REM Function to download a file using PowerShell
:download
powershell -Command "& {Invoke-WebRequest -Uri %1 -OutFile %2}"
goto :eof

REM Check if Python is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing the latest version of Python...
    
    REM Download the latest Python installer (for 64-bit systems)
    set "python_url=https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
    set "python_installer=python-installer.exe"
    
    call :download %python_url% %python_installer%

    REM Install Python silently and add it to PATH
    %python_installer% /quiet InstallAllUsers=1 PrependPath=1

    REM Wait a moment to ensure Python is fully installed
    timeout /t 5 /nobreak >nul

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

REM Install required Python libraries for the Music Controller
echo Installing required Python libraries...
python -m pip install keyboard plyer pycaw comtypes

REM Note: 'ctypes' and 'json' are built-in Python modules, no need to install them
echo Note: 'ctypes' and 'json' are already included with Python.

echo Installation completed successfully.
pause
