#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 文件批量翻译脚本
将英文 Markdown 文件翻译成中文
"""

import os
import re
import json
import time
from pathlib import Path

# 专有名词列表（不翻译的词）
PROPER_NOUNS = {
    # Pinterest 相关
    'Pinterest', 'Pin', 'Pins', 'Board', 'Boards', 'SOP', 'SOPs',
    'KW', 'KWs', 'Keyword', 'Keywords', 'Annotations', 'Annotation',
    'Make.com', 'make.com', 'Blueprint', 'blueprint', 'JSON', 'json',
    
    # 技术相关
    'API', 'URL', 'HTML', 'CSS', 'JavaScript', 'PHP', 'SQL', 'CSV',
    'VPN', 'Proxy', 'IP', 'VPN/Proxy', 'WP', 'WordPress',
    'SEO', 'RPM', 'CTR', 'FAQ', 'FAQs', 'Q4',
    
    # 工具和服务
    'Midjourney', 'Ideogram', 'Grok', 'ChatGPT', 'Claude',
    'Google Drive', 'Google', 'Gmail', 'WordPress',
    
    # 网站和品牌
    'NicheGrowNerd', 'NGN', 'PinClicks', 'MoneyVipProgram', 'BestBlackHatForum',
    'Scout Pins', 'Pin Scale System', 'PinScale', 'Pin Scale',
    
    # 其他专有名词
    'SaaS', 'B2B', 'B2C', 'DIY', 'VS', 'vs', 'AI', 'LLM',
    'PDF', 'DOCX', 'MD', 'markdown', 'MD',
    'bash', 'bat', 'sh', 'zip', 'ZIP',
    
    # 文件名和路径相关
    'blueprint.json', 'blueprint', 'json',
    'images', 'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg',
}

# 需要保留原样的常见术语对（英文-中文映射，但某些情况保留英文）
TERM_PRESERVATION = {
    # 保持不变的词
}

# 翻译词典 - 常见术语
TRANSLATION_DICT = {
    # 基础词汇
    'Step': '步骤',
    'Profile': '个人资料',
    'Optimization': '优化',
    'Setup': '设置',
    'Account': '账户',
    'Accounts': '账户',
    'Business': '商业',
    'Board': '版块',
    'Boards': '版块',
    'Pin': 'Pin',
    'Pins': 'Pin',
    'Description': '描述',
    'Descriptions': '描述',
    'Keyword': '关键词',
    'Keywords': '关键词',
    'KW': '关键词',
    'KWs': '关键词',
    'Niche': '细分领域',
    'Research': '研究',
    'Article': '文章',
    'Articles': '文章',
    'SOP': 'SOP',  # 标准操作流程
    'Standard Operating Procedure': '标准操作流程',
    'Automation': '自动化',
    'Tool': '工具',
    'Tools': '工具',
    'Image': '图片',
    'Images': '图片',
    'Design': '设计',
    'Traffic': '流量',
    'Click': '点击',
    'Clicks': '点击',
    'Conversion': '转化',
    'Analytics': '分析',
    'Performance': '表现',
    'Algorithm': '算法',
    'Content': '内容',
    'Creation': '创建',
    'Upload': '上传',
    'Delete': '删除',
    'Download': '下载',
    'Website': '网站',
    'Websites': '网站',
    'Site': '站点',
    'Sites': '站点',
    'Blog': '博客',
    'Domain': '域名',
    'Email': '邮箱',
    'Address': '地址',
    'Username': '用户名',
    'Password': '密码',
    'Settings': '设置',
    'Configuration': '配置',
    'Script': '脚本',
    'Scripts': '脚本',
    'Folder': '文件夹',
    'File': '文件',
    'Files': '文件',
    'Directory': '目录',
    'Link': '链接',
    'Links': '链接',
    'URL': 'URL',
    'Title': '标题',
    'Titles': '标题',
    'Text': '文本',
    'Photo': '照片',
    'Logo': '标志',
    'Name': '名称',
    'About': '关于',
    'Home': '主页',
    'Decor': '装饰',
    'Interior': '室内',
    'Design': '设计',
    'Management': '管理',
    'Personal': '个人',
    'Information': '信息',
    'Brand': '品牌',
    'Data': '数据',
    'Database': '数据库',
    'System': '系统',
    'Workflow': '工作流',
    'Process': '流程',
    'Task': '任务',
    'Tasks': '任务',
    'Listicle': '列表文章',
    'Listicles': '列表文章',
    'Recipe': '食谱',
    'Recipes': '食谱',
    'Product': '产品',
    'Products': '产品',
    'Template': '模板',
    'Templates': '模板',
    'Stock': '素材',
    'Real': '真实',
    'Human': '人工',
    'Human-Editing': '人工编辑',
    'Filter': '过滤器',
    'Filters': '过滤器',
    'Connection': '连接',
    'Module': '模块',
    'Modules': '模块',
    'Parameter': '参数',
    'Parameters': '参数',
    'Variable': '变量',
    'Variables': '变量',
    'Version': '版本',
    'Metadata': '元数据',
    'Method': '方法',
    'Headers': '请求头',
    'Response': '响应',
    'Request': '请求',
    'Error': '错误',
    'Errors': '错误',
    'Success': '成功',
    'Failed': '失败',
    'Notification': '通知',
    'Log': '日志',
    'Login': '登录',
    'Logout': '登出',
    'Register': '注册',
    'Sign': '签名',
    'In': '在',
    'Out': '出',
    'Up': '上',
    'Down': '下',
    'Left': '左',
    'Right': '右',
    'Top': '顶部',
    'Bottom': '底部',
    'Page': '页面',
    'Pages': '页面',
    'Post': '帖子',
    'Posts': '帖子',
    'Category': '分类',
    'Categories': '分类',
    'Tag': '标签',
    'Tags': '标签',
    'Search': '搜索',
    'Feed': '信息流',
    'Feeds': '信息流',
    'Trend': '趋势',
    'Trends': '趋势',
    'Interest': '兴趣',
    'Interests': '兴趣',
    'Audience': '受众',
    'Engagement': '互动',
    'Impression': '展示',
    'Impressions': '展示',
    'Reach': '触达',
    'Follower': '关注者',
    'Followers': '关注者',
    'Following': '关注中',
    'Save': '保存',
    'Saved': '已保存',
    'Like': '点赞',
    'Likes': '点赞',
    'Comment': '评论',
    'Comments': '评论',
    'Share': '分享',
    'Report': '报告',
    'Export': '导出',
    'Import': '导入',
    'Edit': '编辑',
    'Update': '更新',
    'Create': '创建',
    'Remove': '移除',
    'Add': '添加',
    'Get': '获取',
    'Set': '设置',
    'Enable': '启用',
    'Disable': '禁用',
    'Active': '活跃',
    'Inactive': '非活跃',
    'Status': '状态',
    'Type': '类型',
    'Format': '格式',
    'Size': '大小',
    'Width': '宽度',
    'Height': '高度',
    'Quality': '质量',
    'Resolution': '分辨率',
    'Color': '颜色',
    'Colors': '颜色',
    'Background': '背景',
    'Foreground': '前景',
    'Font': '字体',
    'Style': '样式',
    'Theme': '主题',
    'Layout': '布局',
    'Position': '位置',
    'Alignment': '对齐',
    'Margin': '边距',
    'Padding': '填充',
    'Border': '边框',
    'Shadow': '阴影',
    'Effect': '效果',
    'Effects': '效果',
    'Animation': '动画',
    'Transition': '过渡',
    'Transform': '变换',
    'Duration': '持续时间',
    'Delay': '延迟',
    'Easing': '缓动',
    'Speed': '速度',
    'Performance': '性能',
    'Optimization': '优化',
    'Loading': '加载',
    'Response': '响应',
    'Time': '时间',
    'Date': '日期',
    'Year': '年',
    'Month': '月',
    'Week': '周',
    'Day': '日',
    'Hour': '小时',
    'Minute': '分钟',
    'Second': '秒',
    'Today': '今天',
    'Yesterday': '昨天',
    'Tomorrow': '明天',
    'Current': '当前',
    'Previous': '上一个',
    'Next': '下一个',
    'Last': '最后',
    'First': '第一',
    'Second': '第二',
    'Third': '第三',
    'Number': '数字',
    'Count': '计数',
    'Total': '总计',
    'Average': '平均',
    'Maximum': '最大',
    'Minimum': '最小',
    'Range': '范围',
    'Limit': '限制',
    'Offset': '偏移',
    'Order': '顺序',
    'Sort': '排序',
    'Filter': '筛选',
    'Group': '分组',
    'Search': '搜索',
    'Query': '查询',
    'Result': '结果',
    'Results': '结果',
    'Item': '项目',
    'Items': '项目',
    'Element': '元素',
    'Elements': '元素',
    'Component': '组件',
    'Components': '组件',
    'Feature': '功能',
    'Features': '功能',
    'Option': '选项',
    'Options': '选项',
    'Selection': '选择',
    'Choice': '选择',
    'Default': '默认',
    'Custom': '自定义',
    'Advanced': '高级',
    'Basic': '基础',
    'Simple': '简单',
    'Complex': '复杂',
    'Easy': '简单',
    'Difficult': '困难',
    'Fast': '快速',
    'Slow': '缓慢',
    'Quick': '快速',
    'Efficient': '高效',
    'Effective': '有效',
    'Automatic': '自动',
    'Manual': '手动',
    'Public': '公开',
    'Private': '私密',
    'Local': '本地',
    'Remote': '远程',
    'Online': '在线',
    'Offline': '离线',
    'Available': '可用',
    'Unavailable': '不可用',
    'Enabled': '已启用',
    'Disabled': '已禁用',
    'Required': '必填',
    'Optional': '可选',
    'Yes': '是',
    'No': '否',
    'True': '是',
    'False': '否',
    'None': '无',
    'All': '全部',
    'Some': '一些',
    'Any': '任何',
    'Each': '每个',
    'Every': '每个',
    'Both': '两者',
    'Either': '任一',
    'Neither': '两者都不',
    'Through': '通过',
    'With': '使用',
    'Without': '不使用',
    'From': '从',
    'To': '到',
    'At': '在',
    'On': '在...上',
    'In': '在...里',
    'Of': '的',
    'For': '为了',
    'By': '通过',
    'About': '关于',
    'Between': '之间',
    'Among': '之中',
    'Within': '之内',
    'Without': '没有',
    'During': '期间',
    'Before': '之前',
    'After': '之后',
    'While': '当...时',
    'When': '当...时',
    'Where': '哪里',
    'Why': '为什么',
    'How': '如何',
    'What': '什么',
    'Which': '哪个',
    'Who': '谁',
    'Whose': '谁的',
    'This': '这',
    'That': '那',
    'These': '这些',
    'Those': '那些',
    'Here': '这里',
    'There': '那里',
    'Now': '现在',
    'Then': '那时',
    'Always': '总是',
    'Never': '从不',
    'Sometimes': '有时',
    'Often': '经常',
    'Rarely': '很少',
    'Usually': '通常',
    'Generally': '一般',
    'Specifically': '具体来说',
    'Especially': '特别是',
    'Particularly': '特别',
    'Mainly': '主要',
    'Mostly': '大多',
    'Only': '只有',
    'Just': '只是',
    'Also': '也',
    'Too': '也',
    'Very': '非常',
    'Quite': '相当',
    'Rather': '相当',
    'Pretty': '相当',
    'Really': '真正',
    'Actually': '实际上',
    'In fact': '事实上',
    'Indeed': '确实',
    'Certainly': '当然',
    'Definitely': '肯定',
    'Probably': '可能',
    'Possibly': '可能',
    'Maybe': '也许',
    'Perhaps': '或许',
    'Please': '请',
    'Thank': '谢谢',
    'Thanks': '谢谢',
    'Welcome': '欢迎',
    'Note': '注意',
    'Notice': '通知',
    'Warning': '警告',
    'Error': '错误',
    'Tip': '提示',
    'Pro Tip': '专业提示',
    'Important': '重要',
    'Caution': '注意',
    'Danger': '危险',
    'Success': '成功',
    'Info': '信息',
    'Help': '帮助',
    'Example': '示例',
    'Examples': '示例',
    'Screenshot': '截图',
    'Figure': '图',
    'Table': '表格',
    'List': '列表',
    'Code': '代码',
    'Command': '命令',
    'Terminal': '终端',
    'Console': '控制台',
    'Shell': 'Shell',
    'Script': '脚本',
    'Program': '程序',
    'Application': '应用程序',
    'App': '应用',
    'Service': '服务',
    'Server': '服务器',
    'Client': '客户端',
    'User': '用户',
    'Admin': '管理员',
    'Administrator': '管理员',
    'Guest': '访客',
    'Member': '成员',
    'Team': '团队',
    'Group': '组',
    'Organization': '组织',
    'Company': '公司',
    'Business': '商业',
    'Enterprise': '企业',
    'Project': '项目',
    'Repository': '仓库',
    'Branch': '分支',
    'Commit': '提交',
    'Merge': '合并',
    'Pull': '拉取',
    'Push': '推送',
    'Release': '发布',
    'Version': '版本',
    'Update': '更新',
    'Upgrade': '升级',
    'Install': '安装',
    'Uninstall': '卸载',
    'Download': '下载',
    'Upload': '上传',
    'Transfer': '传输',
    'Copy': '复制',
    'Paste': '粘贴',
    'Cut': '剪切',
    'Move': '移动',
    'Rename': '重命名',
    'Delete': '删除',
    'Restore': '恢复',
    'Backup': '备份',
    'Archive': '归档',
    'Extract': '解压',
    'Compress': '压缩',
    'Encrypt': '加密',
    'Decrypt': '解密',
    'Lock': '锁定',
    'Unlock': '解锁',
    'Protect': '保护',
    'Secure': '安全',
    'Permission': '权限',
    'Permissions': '权限',
    'Role': '角色',
    'Roles': '角色',
    'Access': '访问',
    'Security': '安全',
    'Privacy': '隐私',
    'Policy': '政策',
    'Terms': '条款',
    'Conditions': '条件',
    'Agreement': '协议',
    'License': '许可',
    'Copyright': '版权',
    'Trademark': '商标',
    'Patent': '专利',
}

def is_proper_noun(word):
    """检查是否是专有名词"""
    word_upper = word.upper()
    # 检查精确匹配
    if word in PROPER_NOUNS:
        return True
    # 检查大写匹配
    if word_upper in [n.upper() for n in PROPER_NOUNS]:
        return True
    return False

def is_code_block(text):
    """检查是否是代码块"""
    # 检查是否在代码块中
    if text.strip().startswith('```'):
        return True
    if text.strip().startswith('~~~'):
        return True
    return False

def is_inline_code(text):
    """检查是否是内联代码"""
    return bool(re.match(r'^`.+`$', text.strip()))

def is_image_link(text):
    """检查是否是图片链接"""
    return bool(re.match(r'^!\[.*?\]\(.*?\)$', text.strip()))

def is_markdown_link(text):
    """检查是否是 Markdown 链接"""
    return bool(re.match(r'^\[.*?\]\(.*?\)$', text.strip()))

def is_html_tag(text):
    """检查是否是 HTML 标签"""
    return bool(re.match(r'^<[^>]+>$', text.strip()))

def translate_text_segment(segment, preserve_urls=True):
    """
    翻译文本片段
    保留图片路径、链接、代码块等格式
    """
    # 跳过空行
    if not segment.strip():
        return segment
    
    # 检查是否是代码块行
    if segment.strip().startswith('```') or segment.strip().startswith('~~~'):
        return segment
    
    # 检查是否是 JSON 代码块
    if segment.strip().startswith('```json'):
        return segment
    
    # 检查是否是代码块内容（简单判断：包含大量特殊字符）
    if re.search(r'^[\s\{\}\[\]\(\),;:]*$', segment) and len(segment.strip()) > 0:
        # 可能是代码
        return segment
    
    # 处理包含代码或链接的行
    result = segment
    
    # 保护图片链接
    image_links = []
    def protect_image(match):
        image_links.append(match.group(0))
        return f"__IMAGE_{len(image_links)-1}__"
    
    result = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', protect_image, result)
    
    # 保护 Markdown 链接
    md_links = []
    def protect_link(match):
        md_links.append((match.group(1), match.group(2)))
        return f"__LINK_{len(md_links)-1}__"
    
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', protect_link, result)
    
    # 保护内联代码
    inline_codes = []
    def protect_inline_code(match):
        inline_codes.append(match.group(1))
        return f"__CODE_{len(inline_codes)-1}__"
    
    result = re.sub(r'`([^`]+)`', protect_inline_code, result)
    
    # 保护 HTML 标签
    html_tags = []
    def protect_html(match):
        html_tags.append(match.group(0))
        return f"__HTML_{len(html_tags)-1}__"
    
    result = re.sub(r'<[^>]+>', protect_html, result)
    
    # 现在翻译纯文本内容
    result = translate_english_text(result)
    
    # 恢复 HTML 标签
    for i, tag in enumerate(html_tags):
        result = result.replace(f"__HTML_{i}__", tag)
    
    # 恢复内联代码
    for i, code in enumerate(inline_codes):
        result = result.replace(f"__CODE_{i}__", f"`{code}`")
    
    # 恢复 Markdown 链接
    for i, (text, url) in enumerate(md_links):
        # 翻译链接文本但保留 URL
        translated_text = translate_english_text(text)
        result = result.replace(f"__LINK_{i}__", f"[{translated_text}]({url})")
    
    # 恢复图片链接
    for i, link in enumerate(image_links):
        result = result.replace(f"__IMAGE_{i}__", link)
    
    return result

def translate_english_text(text):
    """
    翻译英文文本为中文
    使用词典和规则进行翻译
    """
    if not text or not text.strip():
        return text
    
    result = text
    
    # 按优先级处理翻译
    
    # 1. 先处理多词短语（长词优先）
    sorted_phrases = sorted([(k, v) for k, v in TRANSLATION_DICT.items()], 
                           key=lambda x: len(x[0]), reverse=True)
    
    for eng, chn in sorted_phrases:
        # 使用正则表达式进行单词边界匹配
        pattern = r'\b' + re.escape(eng) + r'\b'
        result = re.sub(pattern, chn, result, flags=re.IGNORECASE)
    
    # 2. 处理专有名词（保留原样）
    for noun in sorted(PROPER_NOUNS, key=len, reverse=True):
        # 确保专有名词不被翻译
        if noun.lower() in [k.lower() for k in TRANSLATION_DICT.keys()]:
            # 这个词在翻译词典中，跳过
            continue
        # 保留专有名词的大小写
        pattern = r'\b' + re.escape(noun) + r'\b'
        # 专有名词保持原样
    
    # 3. 处理一些常见的短语和句型
    
    # 处理 "Step X: " 格式
    result = re.sub(r'\bStep\s+(\d+):', r'步骤 \1:', result)
    result = re.sub(r'\bStep\s+(\d+)', r'步骤 \1', result)
    
    # 处理 "Phase X: " 格式
    result = re.sub(r'\bPhase\s+(\d+):', r'阶段 \1:', result)
    result = re.sub(r'\bPHASE\s+(\d+)', r'阶段 \1', result)
    
    # 处理编号格式
    result = re.sub(r'\bNo\.\s*', '编号 ', result)
    
    # 处理日期格式
    result = re.sub(r'\bAdded\s+(\w+)\s+(\d+)', r'添加于 \2年\1', result)
    result = re.sub(r'\(Added\s+(\w+)\s+(\d+)\)', r'(添加于\2年\1)', result)
    result = re.sub(r'\(Added\s+in\s+(\w+)\s+(\d+)\)', r'(添加于\2年\1)', result)
    result = re.sub(r'\(added\s+(\w+)\s+(\d+)\)', r'(添加于\2年\1)', result)
    result = re.sub(r'\(Added\s+([A-Za-z]+)\s+(\d+)\)', lambda m: f'(添加于{m.group(2)}年{month_to_zh(m.group(1))})', result)
    result = re.sub(r'\(Added\s+in\s+([A-Za-z]+)\s+(\d+)\)', lambda m: f'(添加于{m.group(2)}年{month_to_zh(m.group(1))})', result)
    
    # 处理月份缩写
    for mon, mon_zh in [('Jan', '1月'), ('Feb', '2月'), ('Mar', '3月'), ('Apr', '4月'), 
                         ('May', '5月'), ('Jun', '6月'), ('Jul', '7月'), ('Aug', '8月'),
                         ('Sep', '9月'), ('Sept', '9月'), ('Oct', '10月'), ('Nov', '11月'), ('Dec', '12月')]:
        result = re.sub(r'\b' + mon + r'\b', mon_zh, result)
    
    # 处理一些常见句型
    result = result.replace('...', '…')
    
    # 处理 "How to" 
    result = re.sub(r'\bHow\s+to\s+', '如何', result)
    
    # 处理 "What is/are"
    result = re.sub(r'\bWhat\s+is\b', '什么是', result)
    result = re.sub(r'\bWhat\s+are\b', '什么是', result)
    
    # 处理 "Why"
    result = re.sub(r'\bWhy\s+', '为什么', result)
    
    # 处理 "When"
    result = re.sub(r'\bWhen\s+', '何时', result)
    
    # 处理 "Where"
    result = re.sub(r'\bWhere\s+', '哪里', result)
    
    # 处理 "The ... of ..." 结构
    # result = re.sub(r'\bThe\s+(.+?)\s+of\s+(.+?)\b', r'\2的\1', result)
    
    # 处理冠词
    result = re.sub(r'\bThe\b', '', result)
    
    # 处理一些常见的前缀和后缀
    result = re.sub(r'\bNon-', '非', result)
    result = re.sub(r'\bPre-', '预', result)
    result = re.sub(r'\bRe-', '重新', result)
    result = re.sub(r'\bAuto-', '自动', result)
    result = re.sub(r'\bSelf-', '自', result)
    result = re.sub(r'\bMulti-', '多', result)
    result = re.sub(r'\bOver-', '过度', result)
    result = re.sub(r'\bUnder-', '不足', result)
    result = re.sub(r'\bSuper-', '超级', result)
    result = re.sub(r'\bAnti-', '反', result)
    result = re.sub(r'\bBi-', '双', result)
    result = re.sub(r'\bCo-', '协作', result)
    result = re.sub(r'\bCross-', '跨', result)
    result = re.sub(r'\bExtra-', '额外', result)
    result = re.sub(r'\bHyper-', '超', result)
    result = re.sub(r'\bInter-', '相互', result)
    result = re.sub(r'\bIntra-', '内部', result)
    result = re.sub(r'\bMacro-', '宏观', result)
    result = re.sub(r'\bMicro-', '微观', result)
    result = re.sub(r'\bMid-', '中间', result)
    result = re.sub(r'\bMini-', '迷你', result)
    result = re.sub(r'\bMis-', '误', result)
    result = re.sub(r'\bMono-', '单', result)
    result = re.sub(r'\bOver-', '过度', result)
    result = re.sub(r'\bPost-', '后', result)
    result = re.sub(r'\bPre-', '预', result)
    result = re.sub(r'\bPro-', '专业', result)
    result = re.sub(r'\bSub-', '子', result)
    result = re.sub(r'\bSuper-', '超级', result)
    result = re.sub(r'\bTrans-', '跨', result)
    result = re.sub(r'\bUltra-', '超', result)
    result = re.sub(r'\bUn-', '不', result)
    
    # 处理连字符连接的词
    # result = re.sub(r'\b(\w+)-(\w+)\b', r'\1-\2', result)
    
    # 清理多余的空格
    result = re.sub(r'\s+', ' ', result)
    
    return result.strip()

def month_to_zh(month):
    """月份转中文"""
    month_map = {
        'January': '1月', 'February': '2月', 'March': '3月', 'April': '4月',
        'May': '5月', 'June': '6月', 'July': '7月', 'August': '8月',
        'September': '9月', 'October': '10月', 'November': '11月', 'December': '12月',
        'Jan': '1月', 'Feb': '2月', 'Mar': '3月', 'Apr': '4月',
        'May': '5月', 'Jun': '6月', 'Jul': '7月', 'Aug': '8月',
        'Sep': '9月', 'Sept': '9月', 'Oct': '10月', 'Nov': '11月', 'Dec': '12月'
    }
    return month_map.get(month, month)

def translate_markdown_file(file_path, output_path=None):
    """
    翻译 Markdown 文件
    """
    if output_path is None:
        output_path = file_path
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        translated_lines = []
        in_code_block = False
        code_block_type = None
        
        for line in lines:
            stripped = line.strip()
            
            # 检测代码块开始/结束
            if stripped.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_type = stripped[3:].strip() or 'code'
                else:
                    in_code_block = False
                    code_block_type = None
                translated_lines.append(line)
                continue
            
            # 如果在代码块中，不翻译
            if in_code_block:
                translated_lines.append(line)
                continue
            
            # 检测 JSON 内容块（JSON 不翻译）
            if stripped.startswith('{') or stripped.startswith('['):
                # 可能是 JSON，检查整行
                if line.count('{') > line.count('}') or line.count('[') > line.count(']'):
                    # 可能是多行 JSON 的开始
                    translated_lines.append(line)
                    continue
            
            # 检查是否是标题行
            if stripped.startswith('#'):
                translated_lines.append(translate_text_segment(line))
                continue
            
            # 检查是否是水平线
            if stripped.startswith('---') or stripped.startswith('***'):
                translated_lines.append(line)
                continue
            
            # 检查是否是列表项
            if stripped.startswith('-') or stripped.startswith('*') or re.match(r'^\d+\.', stripped):
                translated_lines.append(translate_text_segment(line))
                continue
            
            # 检查是否是表格行
            if stripped.startswith('|') and stripped.endswith('|'):
                translated_lines.append(translate_text_segment(line))
                continue
            
            # 检查是否是引用行
            if stripped.startswith('>'):
                translated_lines.append(translate_text_segment(line))
                continue
            
            # 检查是否是元数据字段（如 **Key**: Value）
            if re.match(r'^\*\*[^*]+\*\*:', stripped):
                translated_lines.append(translate_text_segment(line))
                continue
            
            # 普通文本行
            translated_lines.append(translate_text_segment(line))
        
        # 写入翻译后的内容
        translated_content = '\n'.join(translated_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return True
    except Exception as e:
        print(f"翻译文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    base_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted_zh"
    
    # 需要翻译的目录和文件
    dirs_to_translate = [
        "10-Docx_Files",
        "11-Blueprint_Json", 
        "12-Scripts_Configs",
    ]
    
    # 00-Index.md 文件单独处理
    index_file = os.path.join(base_dir, "00-Index.md")
    
    print("=" * 60)
    print("开始翻译 Markdown 文件...")
    print("=" * 60)
    
    total_files = 0
    success_count = 0
    
    # 翻译指定目录中的所有 .md 文件
    for dir_name in dirs_to_translate:
        dir_path = os.path.join(base_dir, dir_name)
        
        if not os.path.exists(dir_path):
            print(f"目录不存在: {dir_path}")
            continue
        
        print(f"\n处理目录: {dir_name}")
        
        # 查找所有 .md 文件
        for filename in os.listdir(dir_path):
            if filename.endswith('.md'):
                file_path = os.path.join(dir_path, filename)
                total_files += 1
                
                print(f"  翻译中: {filename}...", end=" ")
                if translate_markdown_file(file_path):
                    success_count += 1
                    print(f"完成")
                else:
                    print(f"失败")
    
    # 翻译索引文件
    print(f"\n处理索引文件: 00-Index.md")
    if os.path.exists(index_file):
        print(f"  翻译中: 00-Index.md...", end=" ")
        if translate_markdown_file(index_file):
            success_count += 1
            total_files += 1
            print(f"完成")
        else:
            print(f"失败")
    
    print("\n" + "=" * 60)
    print(f"翻译完成! 成功: {success_count}/{total_files}")
    print("=" * 60)

if __name__ == "__main__":
    main()
