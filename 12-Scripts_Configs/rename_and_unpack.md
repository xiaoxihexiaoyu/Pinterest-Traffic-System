# 重命名并解压

---

**File Type**: Script (.bat)
**Description**: Batch script for renaming and unpacking files / 用于重命名和解压文件的批处理脚本

## Script Content / 脚本内容

```bat
@echo off
REM ==============================================================================
REM  File:          rename_and_unpack.bat
REM  Author:        NicheGrowNerd (https://nichegrownerd.com/)
REM  Created:       2025
REM  Description:   Extracting all ZIP files in the current directory while avoiding filename conflicts and handling errors.
REM  描述:          解压当前目录中的所有 ZIP 文件，同时避免文件名冲突并处理错误。
REM  Version:       1.0
REM  Dependencies:  The script is designed to run in Windows Command Prompt (cmd.exe) and requires a Windows environment.
REM					It requires PowerShell 5.0 or later, which is available by default on Windows 10 and later.
REM  依赖项:       此脚本设计为在 Windows 命令提示符（cmd.exe）中运行，需要 Windows 环境。
REM					需要 PowerShell 5.0 或更高版本，Windows 10 及更高版本默认安装。
REM  Usage:         Copy batch file to the same directory where the *.zip-files lay and then just start it
REM  使用方法:      将批处理文件复制到 *.zip 文件所在的目录，然后直接运行
REM ==============================================================================

setlocal enabledelayedexpansion

rem Set the path to the current directory
rem 设置当前目录路径
set "currentDir=%cd%"

rem Loop through all ZIP files in the current directory
rem 遍历当前目录中的所有 ZIP 文件
for /f "delims=" %%f in ('dir /b /a-d "*.zip"') do (
    rem Original file name
    rem 原始文件名
    set "originalFile=%%f"

    rem Extract the file name without extension
    rem 提取不带扩展名的文件名
    set "fileName=%%~nf"
    set "fileExt=%%~xf"

    rem Remove [ and ] from the file name
    rem 从文件名中移除 [ 和 ]
    set "cleanName=!fileName:[=!"
    set "cleanName=!cleanName:]=!"

    rem Optional: Remove other problematic characters, e.g. ( and )
    rem 可选：移除其他有问题的字符，例如 ( 和 )
    set "cleanName=!cleanName:(=!"
    set "cleanName=!cleanName:)=!"

    rem Check whether the name has been changed
    rem 检查名称是否已更改
    if "!fileName!" NEQ "!cleanName!" (
        rem New complete file name
        rem 新的完整文件名
        set "newFileName=!cleanName!!fileExt!"

        rem Check whether the new file already exists
        rem 检查新文件是否已存在
        if exist "!currentDir!\!newFileName!" (
            echo Error: The file "!newFileName!" already exists. Skip the renaming of "!originalFile!".
            echo 错误：文件 "!newFileName!" 已存在。跳过 "!originalFile!" 的重命名。
        ) else (
            rem Rename the file
            rem 重命名文件
            ren "!originalFile!" "!newFileName!"
            if errorlevel 1 (
                echo Error when renaming "!originalFile!" to "!newFileName!".
                echo 重命名 "!originalFile!" 为 "!newFileName!" 时出错。
            ) else (
                echo Renamed: "!originalFile!" to "!newFileName!".
                echo 已重命名："!originalFile!" 为 "!newFileName!"。
                set "originalFile=!newFileName!"
            )
        )
    )

    rem Set the name for the target directory (without extension)
    rem 设置目标目录名称（不带扩展名）
    set "zipFile=!originalFile:~0,-4!"

    rem Debugging: Show the paths to be processed
    rem 调试：显示要处理的路径
    echo Process file: "!originalFile!"
    echo 处理文件："!originalFile!"
    echo Target directory: "!currentDir!\!zipFile!"
    echo 目标目录："!currentDir!\!zipFile!"

    rem Check whether the ZIP file exists
    rem 检查 ZIP 文件是否存在
    if exist "!currentDir!\!originalFile!" (
        if not exist "!currentDir!\!zipFile!\" (
            rem Unzip the ZIP file into the target directory with corrected inverted commas
            rem 将 ZIP 文件解压到目标目录，修正引号问题
            powershell -NoLogo -NoProfile -Command "Expand-Archive -LiteralPath '!currentDir!\!originalFile!' -DestinationPath '!currentDir!\!zipFile!' -Force"

            if errorlevel 1 (
                echo Error when unpacking "!originalFile!".
                echo 解压 "!originalFile!" 时出错。
                rem Optional: Remove the directory if unpacking fails
                rem 可选：如果解压失败，删除目录
                rd /s /q "!currentDir!\!zipFile!\" >nul 2>&1
            ) else (
                echo Successfully unpacked: "!originalFile!" to "!currentDir!\!zipFile!\".
                echo 成功解压："!originalFile!" 到 "!currentDir!\!zipFile!\"。
            )
        ) else (
            echo The directory "!currentDir!\!zipFile!\" already exists. Skip the ZIP file "!originalFile!".
            echo 目录 "!currentDir!\!zipFile!\" 已存在。跳过 ZIP 文件 "!originalFile!"。
        )
    ) else (
        echo The file "!currentDir!\!originalFile!" does not exist.
        echo 文件 "!currentDir!\!originalFile!" 不存在。
    )
)

endlocal
pause
```
