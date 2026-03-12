@ECHO OFF
setlocal enabledelayedexpansion

set "FOLDER_NAME=C:\Users\mokin\Documents\Scripts\Test folder"
set "LOCK_DIR=%FOLDER_NAME%_Locked"
set "PASSWORD_FILE=password.txt"

if not exist "%PASSWORD_FILE%" (
    echo Creating new lock: Enter Password
    set /p "password=apple123"
    echo %password% > %PASSWORD_FILE%
    md "%LOCK_DIR%"
    attrib +h +s "%LOCK_DIR%"
    echo Folder created and locked. Place files in %FOLDER_NAME% [8].
) else (
    set /p "input_password=Enter Password to Unlock: "
    for /f "delims=" %%a in (%PASSWORD_FILE%) do set stored_password=%%a
    if "%input_password%"=="%stored_password%" (
        ren "%LOCK_DIR%" "%FOLDER_NAME%"
        attrib -h -s "%FOLDER_NAME%"
        echo Folder Unlocked [8].
    ) else (
        echo Invalid Password. Locking folder again.
        ren "%FOLDER_NAME%" "%LOCK_DIR%"
        attrib +h +s "%LOCK_DIR%"
        echo Folder locked [8].
    )
)
timeout /t 3 > nul
exit /b
