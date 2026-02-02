# 子文件夹中文件打乱并重命名

---

**File Type**: Script (.sh)
**Description**: Shell script for shuffling and renaming files in subfolders / 用于在子文件夹中打乱并重命名文件的 Shell 脚本

## Script Content / 脚本内容

```sh
#!/bin/bash

# ==============================================================================
#  File:          shuffle_and_rename_files_in_subfolders.sh
#  Author:        NicheGrowNerd (https://nichegrownerd.com/)
#  Created:       2025
#  Description:   This script recursively processes all subdirectories and
#				  renames all files within them.
#  版本说明:     此脚本递归处理所有子目录并重命名其中的所有文件。
#  Version:       1.1
#  Dependencies:  This script is designed to run in a macOS terminal (bash).
#                 It requires macOS with AppleScript support for moving files
#				  to Trash. The 'unzip' command must be available
#				  (pre-installed on macOS).
#  依赖项:       此脚本设计为在 macOS 终端（bash）中运行。
#                 需要 macOS 配合 AppleScript 支持来将文件移至废纸篓。
#				  需要 'unzip' 命令可用（macOS 预装）。
#  Usage:         Copy this script to the directory containing the image folders,
#                 Make it executable (chmod +x shuffle_and_rename_files_in_subfolders.sh)
#                 and run it in a terminal.
#  使用方法:      将此脚本复制到包含图片文件夹的目录中，
#                 使其可执行（chmod +x shuffle_and_rename_files_in_subfolders.sh）
#                 然后在终端中运行它。
# ==============================================================================

# Exclude this script from processing
# 从处理中排除此脚本本身
MASTER_SCRIPT=$(basename "$0")

# Function for renaming files in a directory
# 重命名目录中文件的函数
rename_files() {
    echo
    echo "Processing directory: $(pwd)"
    echo "正在处理目录：$(pwd)"

    # Get the current folder name
    # 获取当前文件夹名称
    FOLDER_NAME=$(basename "$(pwd)")

    # Create a temporary file to save the file names
    # 创建一个临时文件来保存文件名
    TEMP_FILE=$(mktemp)

    # Find all files in the current directory, excluding the script itself
    # 查找当前目录中的所有文件，排除脚本本身
    FILES=(*)
    FILE_COUNT=0

    for FILE in "${FILES[@]}"; do
        if [[ "$FILE" != "$MASTER_SCRIPT" && -f "$FILE" ]]; then
            echo "$FILE" >> "$TEMP_FILE"
            ((FILE_COUNT++))
        fi
    done

    echo "Files found for renaming: $FILE_COUNT"
    echo "找到待重命名的文件：$FILE_COUNT"

    # Check if there are files to rename
    # 检查是否有需要重命名的文件
    if [[ "$FILE_COUNT" -eq 0 ]]; then
        echo "No files to rename in this directory."
        echo "此目录中没有需要重命名的文件。"
        return
    fi

    # Shuffle file names using sort -R
    # 使用 sort -R 打乱文件名
    SHUFFLED_FILE="${TEMP_FILE}_shuffled"
    sort -R "$TEMP_FILE" > "$SHUFFLED_FILE"

    # Counter for new file names
    # 新文件名计数器
    COUNT=1

    # Iterate over the shuffled file names and rename them
    # 遍历打乱后的文件名并重命名
    echo "Start renaming the files..."
    echo "开始重命名文件..."
    while IFS= read -r OLD_NAME; do
        EXT="${OLD_NAME##*.}"
        NEW_NAME="${FOLDER_NAME} ${COUNT}.${EXT}"

        echo "Rename from '$OLD_NAME' to '$NEW_NAME'"
        echo "重命名：'$OLD_NAME' -> '$NEW_NAME'"
        mv "$OLD_NAME" "$NEW_NAME"

        ((COUNT++))
    done < "$SHUFFLED_FILE"

    # Delete the temporary files
    # 删除临时文件
    rm -f "$TEMP_FILE" "$SHUFFLED_FILE"

    echo "Files have been successfully renamed in this directory."
    echo "此目录中的文件已成功重命名。"
}

# Recursive run through all subdirectories
# 递归遍历所有子目录
echo "Start processing all subdirectories..."
echo "开始处理所有子目录..."

find . -type d | while IFS= read -r DIR; do
    echo "Processing subdirectory: $DIR"
    echo "正在处理子目录：$DIR"
    cd "$DIR" || continue
    rename_files
    cd - > /dev/null || exit
done

# Also edit the current directory
# 同时处理当前目录
rename_files

echo
echo "All directories have been processed."
echo "所有目录已处理完成。"
read -p "Press [Enter] to exit..."
read -p "按 [Enter] 键退出..."

```
