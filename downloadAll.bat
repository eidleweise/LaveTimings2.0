@echo off

rem Install dependencies listed in requirements.txt
pip install -r requirements.txt

if exist "%errorlevel%" (
  echo Failed to install dependencies. Exit code: %errorlevel%
  exit /b %errorlevel%
)

rem Execute the Python script
python DownloadAll.py

if exist "%errorlevel%" (
  echo Script execution failed. Exit code: %errorlevel%
  exit /b %errorlevel%
)

echo Download process completed successfully!

pause