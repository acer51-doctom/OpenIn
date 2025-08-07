@echo off
set ID=com.example.openurl
set HOST_PATH=%~dp0native_app.py

:: Write manifest to APPDATA
set MANIFEST_PATH=%APPDATA%\Google\Chrome\NativeMessagingHosts\%ID%.json
mkdir "%APPDATA%\Google\Chrome\NativeMessagingHosts" >nul 2>&1

(
echo {
echo     "name": "%ID%",
echo     "description": "Open URLs in external browsers",
echo     "path": "%HOST_PATH:\=\\%",
echo     "type": "stdio",
echo     "allowed_origins": [
echo         "chrome-extension://__EXTENSION_ID__/"
echo     ]
echo }
) > "%MANIFEST_PATH%"

echo Done. Remember to replace __EXTENSION_ID__ in the manifest!
pause
