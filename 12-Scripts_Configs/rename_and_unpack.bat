@echo off
REM ==============================================================================
REM  File:          rename_and_unpack.bat
REM  Author:        NicheGrowNerd (https://nichegrownerd.com/)
REM  Created:       2025
REM  Description:   Extracting all ZIP files in the current directory while avoiding filename conflicts and handling errors.
REM  Version:       1.0
REM  Dependencies:  The script is designed to run in Windows Command Prompt (cmd.exe) and requires a Windows environment.
REM					It requires PowerShell 5.0 or later, which is available by default on Windows 10 and later.
REM  Usage:         Copy batch file to the same directory where the *.zip-files lay and then just start it
REM ==============================================================================

setlocal enabledelayedexpansion

rem Set the path to the current directory
set "currentDir=%cd%"

rem Loop through all ZIP files in the current directory
for /f "delims=" %%f in ('dir /b /a-d "*.zip"') do (
    rem Original file name
    set "originalFile=%%f"

    rem Extract the file name without extension
    set "fileName=%%~nf"
    set "fileExt=%%~xf"

    rem Remove [ and ] from the file name
    set "cleanName=!fileName:[=!"
    set "cleanName=!cleanName:]=!"

    rem Optional: Remove other problematic characters, e.g. ( and )
    set "cleanName=!cleanName:(=!"
    set "cleanName=!cleanName:)=!"

    rem Check whether the name has been changed
    if "!fileName!" NEQ "!cleanName!" (
        rem New complete file name
        set "newFileName=!cleanName!!fileExt!"

        rem Check whether the new file already exists
        if exist "!currentDir!\!newFileName!" (
            echo Error: The file "!newFileName!" already exists. Skip the renaming of "!originalFile!".
        ) else (
            rem Rename the file
            ren "!originalFile!" "!newFileName!"
            if errorlevel 1 (
                echo Error when renaming "!originalFile!" to "!newFileName!".
            ) else (
                echo Renamed: "!originalFile!" to "!newFileName!".
                set "originalFile=!newFileName!"
            )
        )
    )

    rem Set the name for the target directory (without extension)
    set "zipFile=!originalFile:~0,-4!"

    rem Debugging: Show the paths to be processed
    echo Process file: "!originalFile!"
    echo Target directory: "!currentDir!\!zipFile!"

    rem Check whether the ZIP file exists
    if exist "!currentDir!\!originalFile!" (
        if not exist "!currentDir!\!zipFile!\" (
            rem Unzip the ZIP file into the target directory with corrected inverted commas
            powershell -NoLogo -NoProfile -Command "Expand-Archive -LiteralPath '!currentDir!\!originalFile!' -DestinationPath '!currentDir!\!zipFile!' -Force"

            if errorlevel 1 (
                echo Error when unpacking "!originalFile!".
                rem Optional: Remove the directory if unpacking fails
                rd /s /q "!currentDir!\!zipFile!\" >nul 2>&1
            ) else (
                echo Successfully unpacked: "!originalFile!" to "!currentDir!\!zipFile!\".
            )
        ) else (
            echo The directory "!currentDir!\!zipFile!\" already exists. Skip the ZIP file "!originalFile!".
        )
    ) else (
        echo The file "!currentDir!\!originalFile!" does not exist.
    )
)

endlocal
pause