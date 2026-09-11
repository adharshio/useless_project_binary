@echo off
echo Closing any running instances of Windows-De-fender.exe and Anti-Antivirus.exe...
taskkill /F /IM Windows-De-fender.exe 2>nul
taskkill /F /IM Anti-Antivirus.exe 2>nul
echo Building Windows-De-fender.exe with PyInstaller...
python -m PyInstaller --clean Anti-Antivirus.spec
if %ERRORLEVEL% equ 0 (
    echo.
    echo ===============================================
    echo [SUCCESS] Build completed!
    echo New executable is in: dist\Windows-De-fender.exe
    echo ===============================================
) else (
    echo.
    echo [ERROR] Build failed. Check errors above.
)
pause
