# 重命名并解压

---

**File Type**: Script (.sh)
**Description**: Shell script for renaming and unpacking files / 用于重命名和解压文件的 Shell 脚本

## Script Content / 脚本内容

```sh
#!/bin/bash

# ==============================================================================
#  File:          rename_and_unpack.sh
#  Author:        NicheGrowNerd (https://nichegrownerd.com/)
#  Description:   Extract all ZIP files in the current directory while avoiding
#                 filename conflicts and handling errors. Moves the ZIP files
#                 to the Trash after successful extraction.
#  描述:          解压当前目录中的所有 ZIP 文件，同时避免文件名冲突并处理错误。
#                 解压成功后将 ZIP 文件移至废纸篓。
#  Version:       1.1
#  Dependencies:  The script is designed to run on macOS.
#                 It requires:
#                   - unzip (installed by default on macOS)
#                   - osascript (installed by default on macOS)
#  依赖项:       此脚本设计为在 macOS 上运行。
#                 需要：
#                   - unzip（macOS 默认安装）
#                   - osascript（macOS 默认安装）
#  Usage:         Copy or move this script to the same directory as the *.zip
#                 files. Make it executable (chmod +x rename_and_unpack.sh)
#                 and run it in a terminal.
#  使用方法:      将此脚本复制或移动到 *.zip 文件所在的同一目录。
#                 使其可执行（chmod +x rename_and_unpack.sh）
#                 然后在终端中运行它。
# ==============================================================================

# Exit on critical errors but allow non-critical errors to show warnings
# 遇到严重错误时退出，但允许非严重错误显示警告
set -e

# Function to move file to macOS Trash
# 将文件移至 macOS 废纸篓的函数
move_to_trash() {
    osascript -e "tell application \"Finder\" to move POSIX file \"$1\" to trash"
}

# Loop through all ZIP files in the current directory
# 遍历当前目录中的所有 ZIP 文件
for f in *.zip; do
    # Check if no ZIP files are found
    # 检查是否未找到 ZIP 文件
    if [ ! -f "$f" ]; then
        echo "No .zip files found in this directory."
        echo "此目录中未找到 .zip 文件。"
        break
    fi

    originalFile="$f"
    baseName="${f%.zip}"  # File name without extension / 不带扩展名的文件名
    extension="${f##*.}"  # File extension (should be "zip") / 文件扩展名（应为 "zip"）

    # Remove specific problematic characters: [ ] ( )
    # 移除特定的有问题的字符：[ ] ( )
    cleanBaseName=$(echo "$baseName" | tr -d '[]()')

    # Rename the file if necessary
    # 如有必要，重命名文件
    if [ "$baseName" != "$cleanBaseName" ]; then
        newFileName="$cleanBaseName.$extension"
        if [ -e "$newFileName" ]; then
            echo "Warning: The file '$newFileName' already exists. Skipping rename of '$originalFile'."
            echo "警告：文件 '$newFileName' 已存在。跳过 '$originalFile' 的重命名。"
        else
            mv "$originalFile" "$newFileName"
            echo "Renamed: '$originalFile' to '$newFileName'."
            echo "已重命名：'$originalFile' 为 '$newFileName'。"
            originalFile="$newFileName"
        fi
    fi

    # Define the extraction directory (same as ZIP file name)
    # 定义解压目录（与 ZIP 文件名相同）
    zipDir="${originalFile%.zip}"

    echo "Processing file: '$originalFile'"
    echo "正在处理文件：'$originalFile'"
    echo "Target directory: '$zipDir'"
    echo "目标目录：'$zipDir'"

    # Check if the ZIP file still exists
    # 检查 ZIP 文件是否仍然存在
    if [ -f "$originalFile" ]; then
        # Only unzip if the target directory does not already exist
        # 仅当目标目录不存在时才解压
        if [ ! -d "$zipDir" ]; then
            unzip -o "$originalFile" -d "$zipDir" || { echo "Error: Extraction failed for '$originalFile'."; echo "错误：'$originalFile' 解压失败。"; rm -rf "$zipDir"; exit 1; }
            echo "Successfully unpacked: '$originalFile' to '$zipDir'."
            echo "成功解压：'$originalFile' 到 '$zipDir'。"

            # Move ZIP file to the Trash
            # 将 ZIP 文件移至废纸篓
            echo "Moving '$originalFile' to Trash..."
            echo "正在将 '$originalFile' 移至废纸篓..."
            if ! move_to_trash "$originalFile"; then
                echo "Warning: Could not move '$originalFile' to Trash."
                echo "警告：无法将 '$originalFile' 移至废纸篓。"
            else
                echo "File '$originalFile' successfully moved to Trash."
                echo "文件 '$originalFile' 已成功移至废纸篓。"
            fi
        else
            echo "Warning: The directory '$zipDir' already exists. Skipping the ZIP file '$originalFile'."
            echo "警告：目录 '$zipDir' 已存在。跳过 ZIP 文件 '$originalFile'。"
        fi
    else
        echo "Error: The file '$originalFile' does not exist."
        echo "错误：文件 '$originalFile' 不存在。"
    fi
done

echo "Processing complete."
echo "处理完成。"
exit 0
```
