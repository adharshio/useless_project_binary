@echo off
echo Building Anti-Antivirus.exe with PyInstaller...
python -m PyInstaller --clean Anti-Antivirus.spec
if %ERRORLEVEL% equ 0 (
    echo.
    echo ===============================================
    echo [SUCCESS] Build completed!
    echo New executable is in: dist\Anti-Antivirus.exe
    echo ===============================================
) else (
    echo.
    echo [ERROR] Build failed. Check errors above.
)
pause
