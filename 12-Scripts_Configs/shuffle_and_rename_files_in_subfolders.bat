@echo off
REM ==============================================================================
REM  File:          shuffle_and_rename_files_in_subfolders.bat
REM  Author:        NicheGrowNerd (https://nichegrownerd.com/)
REM  Created:       2025
REM  Description:   This script recursively processes all subdirectories and renames all files within them. 
REM  Version:       1.0
REM  Dependencies:  The script is designed to run in Windows Command Prompt (cmd.exe) and requires a Windows environment.
REM					It requires PowerShell 5.0 or later, which is available by default on Windows 10 and later.
REM  Usage:         Copy batch file to the same directory where the subfolders with the images lay and then just start it
REM ==============================================================================

setlocal enabledelayedexpansion

:: Exclude this script from processing
set "master_script=%~nx0"

:: Recursive run through all subdirectories
echo Start processing all subdirectories...

:: Use 'dir /ad /b /s' to list all subdirectories
for /f "delims=" %%d in ('dir /ad /b /s') do (
    echo Process subdirectory: %%d
    pushd "%%d" >nul
    call :RenameFiles
    popd >nul
)

:: Also edit the current directory
call :RenameFiles

echo.
echo All subdirectories have been processed.
pause

:: Function for renaming files in a directory
:RenameFiles
    echo.
    echo Verarbeite Verzeichnis: %cd%
    
    :: Get the name of the script and exclude it from processing
    set "script_name=%master_script%"
    
    :: Determine the current folder name
    for %%a in ("%cd%") do set "folder_name=%%~nxa"
    
    :: Create a temporary file to save the file names
    set "temp_file=%temp%\file_list_%RANDOM%.txt"
    
    :: Empty the temporary file without adding an empty line
    > "%temp_file%" (
        rem Leere die Datei
    )
    
    :: Iterate over all files in the current directory and save the names in the temporary file
    echo Search for files to rename...
    set "file_count=0"
    for %%f in (*) do (
        if /I not "%%~nxf"=="%script_name%" (
            echo %%f>>"%temp_file%"
            set /a file_count+=1
        )
    )
    
    echo Files found for renaming: !file_count!
    
    :: Check whether files are available for renaming
    if !file_count! EQU 0 (
        echo No files to rename in this directory.
        goto :EndRename
    )
    
    :: Optional: Show list of files to be edited
    echo Files:
    type "%temp_file%"
    echo.
    
    :: Use PowerShell to merge the file names and write them to a temporary file
    powershell -command "if (Test-Path '%temp_file%') { Get-Content '%temp_file%' | Get-Random -Count (Get-Content '%temp_file%').Count | Set-Content '%temp_file%_shuffled' }"
    
    :: Check whether the mixed file has been created
    if not exist "%temp_file%_shuffled" (
        echo Error: The mixed file list was not created.
        goto :EndRename
    )
    
    :: Counter for new file names
    set "count=1"
    
    :: Iterate over the mixed file names and rename them
    echo Start renaming the files...
    for /f "usebackq delims=" %%i in ("%temp_file%_shuffled") do (
        set "old_name=%%i"
        set "ext=%%~xi"
        set "new_name=!folder_name! !count!!ext!"
        echo Rename from "!old_name!" to "!new_name!"
        ren "!old_name!" "!new_name!"
        set /a count+=1
    )
    
    :: Delete the temporary files
    del "%temp_file%"
    del "%temp_file%_shuffled"
    
    echo Files have been successfully renamed in this directory.
    goto :EOF

:EndRename
    goto :EOF
