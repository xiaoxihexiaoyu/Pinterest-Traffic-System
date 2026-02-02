---
title: 无限滚动（提高 RPM 的最有效方法）
source: 92-Infinity_Scroll_(Most_Effective_Way_to_Increase_Your_RPMs)_(Added_Aug_25).pdf
category: Website Building
---

## 第 1 页

在过去的几个月里，我尝试了很多"infinite scroll"插件。唯一在所有主题上都能正常工作的设置是 **Ajax Load More** + **Single Posts** 插件。
它的年费是 49 美元，但这是唯一在我的网站上实际有效的组合。
（如果你找到了免费的设置方案，请联系我。我愿意接受更好的方案——但这是唯一对我来说可靠有效的方案。）

### 什么是无限滚动：

当你的读者阅读到文章末尾时，**下一篇博客文章**会自动加载到下方——包括标题、特色图片、分类、标签，全部内容。URL 和页面标题会即时更新，所以分析和分享仍然有意义。

因为有了无限滚动，你的读者会滚动更多内容，在你的网站上停留更长时间，我们通常能看到 **RPM 提高 30-60%**——这只需要一次设置！这是一个非常棒的机会，所以我强烈建议花时间设置它。

### 你需要什么：

1. **Ajax Load More** – WordPress 的免费插件
2. **Single Posts Add-on** – 付费插件（年度许可证）

你只需要 **Single Posts** 插件来实现"下一篇文章加载到下方"。**Next Page** 插件只有在你还想在单篇文章内部使用分页符进行分页时才需要。

### 我的快速简便 10 分钟设置：

#### 步骤 1：安装插件

在你的 WordPress 仪表板 → **Plugins** → **Add New** → 安装并激活 **Ajax Load More**。
上传并激活你购买的 **Single Posts** 插件 ZIP 文件。
转到 **Ajax Load More** → **Licenses** 并粘贴你的许可证密钥（应该会变成绿色）。

#### 步骤 2：告诉 ALM 要定位哪些内容

我们这里保持通用设置：

打开 **Ajax Load More** → **Shortcode Builder**
切换到 **Single Posts** 模式（有时在"Add-ons"选项下）
只需填写这些字段：

- **Post ID**：留空（它会自动检测当前文章）
- **Target**：这是包含文章内容的 HTML 包装器。从 `article` 开始。
- 如果你的主题没有在 `<article>` 内显示 hero/标题，将 Target 切换为 `#main`。
- 各种主题的其他良好备选：`.site-main`、`main.site-main`、`.entry-content`（只使用一个）。

---

## 第 2 页

现在设置核心的 Single Posts 选项：

- **Enable Single Posts**: On（或者在 shortcode 中使用 `single_post="true"`）
- **Pause Override**: On（允许在滚动时自动加载）
- **（可选）Order**：保持默认，或者如果你想显示较新的文章而不是之前的文章，设置为"next"

**进度条（可选，看起来很专业）**：
通过添加参数来开启阅读栏：
`single_post_progress_bar="top:8:#a89777"`

- `top|bottom` = 位置
- `8` = 高度（像素）
- `#a89777` = 你的颜色（确保是 6 位十六进制）

#### 步骤 3 - 无需修改模板即可使用

两种超简单的方法——选择一种：

**A) Automatic（最简单）**：
在 **Ajax Load More** → **Settings** → **Single Posts** 中，启用你的文章类型（通常是 `post`）。
ALM 会自动在文章内容后注入自己。

💡 有时这个功能会出现问题，无法保存设置——在这种情况下，我建议使用选项 B）。

**B) Manual（仍然简单，与主题无关）**：
添加一个 PHP 代码片段（使用像 'WP Code' 这样的插件）

1. 转到 **Snippets** → **Add New** → **PHP snippet**。
2. 给它起个名字，比如"ALM Single Post Infinity"。
3. 设置为仅在前端运行。
4. 粘贴此代码：

---

## 第 3 页

```php
// Wraps the post content and appends Ajax Load More shortcode
// so the next single post auto-loads on scroll.
add_filter('the_content', function ($content) {
    if (is_singular('post') && in_the_loop() && is_main_query()) {
        // 👇 choose the right shortcode version for your theme
        $shortcode = '[ajax_load_more single_post="true"
        single_post_target="article"
        post_type="post"
        pause_override="true"
        single_post_progress_bar="top:8:#a89777"]';
        return '<div id="alm-post-wrap">' . $content . '</div>' .
        do_shortcode($shortcode);
    }
    return $content;
}, 20);
```

如果加载的文章没有显示标题/特色图片，将 `single_post_target` 更改为 `#main` 并再次测试。

💡 这部分是你的 shortcode：你可以随时添加、扩展或更改它：

```
[ajax_load_more single_post="true"
single_post_target="article"
post_type="post"
pause_override="true"
single_post_progress_bar="top:8:#a89777"]
```

例如，如果你不想要进度条，只需删除最后一行。

#### 步骤 4 - 测试

1. 打开你网站上的任何单篇文章
2. 滚动到底部
3. 下一篇文章应该会自动弹出；当你滚动到它时，URL 和页面标题会更新
4. 进度条应该在你阅读时填充（如果你添加了它）

### 快速故障排除：

- **进度条显示但不填充**：你的颜色代码必须是 6 位数字（例如 `#a89777`），你的 **Target** 必须指向一个实际滚动的包装器（如果 `article` 没有起作用，试试 `#main`）。
- **什么都没有加载**：缓存/优化插件喜欢"延迟"JavaScript。临时禁用"Delay/Defer JS"（Autoptimize、Perfmatters、WP Rocket、Cloudflare），或者为 Ajax Load More 脚本添加排除项。然后硬刷新并再次测试。
- **安全插件阻止了它（403/503）**：检查你的防火墙/Wordfence "Live Traffic" 并将被阻止的 REST 请求加入白名单。ALM 使用正常的 WordPress REST 路由，所以加入白名单可以修复它。

---

## 第 4 页

💡 根据你的广告提供商，你需要告诉他们你已经设置了无限滚动，并要求他们检查兼容性——这样广告也能在额外加载的文章上正确显示。

就这样。这正是我推荐的设置，因为它快速、可靠，并且不强迫你编辑主题文件或编写代码。
