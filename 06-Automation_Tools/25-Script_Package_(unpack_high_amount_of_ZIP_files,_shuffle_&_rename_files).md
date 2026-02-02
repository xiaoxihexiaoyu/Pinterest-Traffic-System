# 处理批量 AI 图像下载并组织以获得更好的效果

---

## 文档摘要

**Source File**: 25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files).pdf
**Converted**: 2026-02-02 07:04:33

## 内容预览

- 处理批量 AI 图像下载并组织以获得更好的效果...
- Apple 用户：向下滚动到底部...
- 1. 一次性解压多个 .zip 文件...

---

# 内容

处理批量 AI 图像下载并组织以获得更好的效果

### Apple 用户：向下滚动到底部

### 1. 一次性解压多个 .zip 文件

当你下载大量 AI 生成的图像时 - 特别是来自 Midjourney - 你最终会得到许多需要管理的 .zip 文件。

以下脚本会一次性自动解压同一文件夹中的所有 .zip 文件 - 这会为你节省大量时间。

### Windows: rename_and_unpack.bat (3.37 KB)
### MacOS: renameandunpack.sh (3.14 KB)

工作原理：

### 下载批处理文件 "rename_and_unpack.bat"

将其复制到存储所有 ZIP 文件的同一文件夹中（例如，C:/Temp）

运行批处理文件。第一次运行时你可能会收到警告，点击"更多信息"。

### 点击"仍然运行"

### 批处理文件将：

- 重命名所有 .ZIP 文件，删除特殊字符（以防止错误）
- 自动解压所有 ZIP 文件

过程完成后，你将在命令行窗口中看到确认消息。

### 清理：

你现在可以删除所有 ZIP 文件和 rename_and_unpack.bat 文件，因为它们不再需要了。
如果以后需要，你可以在回收站中找到它们。

### 整理图像：

如有必要，将图像按 overview sheet 中各自关键词命名的文件夹进行分类。

### 下载和存储 ZIP 文件：

将所有 ZIP 文件收集到一个位置。

提示：我建议使用 C:/Temp 以保持一致性，但你也可以选择其他位置。

### 2. 随机排序和重命名文件

AI 生成的图像通常根据创建顺序具有连续的时间戳。
由于 Midjourney 每个 Prompt 生成四个图像，它们通常按顺序出现，这使得它们很容易被识别为 AI 生成的。

为了避免这种模式，最好在同一关键词文件夹内随机排列图像。

### 以下脚本自动执行此过程：

- 进入每个子文件夹
- 随机排列所有现有图像
- 使用子文件夹名称（= 关键词）重命名它们
- 重新编号以创建更自然和随机的外观

Windows: shuffle_and_rename_files_in_subfolders.bat (3.6 KB)
MacOS: shuffle_and_rename_files_in_subfolders.sh (2.75 KB)

工作原理：

下载批处理文件 "shuffle_and_rename_files_in_subfolders.bat" 并将其放在存储所有 ZIP 文件的同一文件夹中（例如，C:/Temp）。

运行批处理文件，第一次运行时你可能会收到警告，点击"更多信息"。

### 然后点击"仍然运行"

现在你有了极好的结果，准备好上传到 Pinterest。

### 对于 MacOS：

根据授权的不同，脚本可能无法在 MacOS 上直接执行。
但不用担心，我会向你展示如何自己创建它以及如何使其可执行！

这些调整应该使程序在 Apple 设备上运行。并非所有步骤都对所有设备必要，在某些情况下，这取决于特定设备或用户设置。
### 这就是为什么一些条目重复的原因。

在这个例子中，脚本被称为"renameandunpack.sh"。你当然可以随意命名它。在我写"renameandunpack.sh"的地方，你应该输入你选择的名称，以便程序知道应该访问哪个脚本。

这个过程适用于解压脚本和随机排序重命名脚本。

确保程序和你想访问的图像在同一文件夹中。为了简单起见，我将路径称为 PATH/FOLDER。

1. 创建文件并插入脚本 - 根据设置，程序可能无法打开。为此，我们只需自己创建脚本（通过"Terminal"）。输入以下内容：

```
~ % touch renameandunpack.sh
~ % nano renameandunpack.sh
```

-> 在那里插入脚本并确保没有行滑落。之后，将脚本保存在保存图像等的完全相同的文件夹中。

2. 使脚本可执行并授予文件夹访问权限：

```
~ % chmod +x renameandunpack.sh
~ % sudo chmod -R 777 PATH/FOLDER
```

### FOLDER % sudo chmod -R 755 PATH/FOLDER
### FOLDER % ./renameandunpack.sh open -a PATH/FOLDER
### FOLDER % open -a PATH/FOLDER

3. 在相应的文件夹中使脚本可执行：

### FOLDER % chmod +x renameandunpack.sh
### FOLDER % touch renameandunpack.sh
### FOLDER % nano renameandunpack.sh

4. 运行程序：

### FOLDER % bash renameandunpack.sh

如前所述：列出的一些步骤并不是绝对必要的，但它们也不会造成任何伤害。如果脚本在较少步骤下已经运行，那就更好了！

如果还有任何问题，请随时联系我！

## 文档图像

![Figure from page 1](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page1_img1.png)

![Figure from page 1](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page1_img2.png)

![Figure from page 2](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page2_img1.png)

![Figure from page 2](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page2_img2.png)

![Figure from page 2](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page2_img3.png)

![Figure from page 3](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page3_img1.png)

![Figure from page 3](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page3_img2.png)

![Figure from page 4](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page4_img1.png)

![Figure from page 4](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page4_img2.png)

![Figure from page 5](assets/06-Automation_Tools/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)/25-Script_Package_(unpack_high_amount_of_ZIP_files,_shuffle_&_rename_files)_page5_img1.png)
