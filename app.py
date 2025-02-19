from flask import Flask, request, jsonify, render_template_string
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)


# 加载环境变量
load_dotenv()
# API 配置
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
AI_MODEL = os.getenv('AI_MODEL')
SearxNG_URL = os.getenv('SearxNG_URL')

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# HTML 模板修改
# 在文件开头添加 markdown 解析器
from markdown import markdown


# 在 HTML_TEMPLATE 中修改样式和结构
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Lokyshin Deep Search🔍</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
    <style>
        /* 响应式布局调整 */
        .search-container { 
            max-width: 800px;
            width: 95%; 
            margin: 30px auto 0;
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 20px;
            box-sizing: border-box; /* 添加这行，确保 padding 和 border 包含在宽度内 */
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: transparent;
        }
        
        /* Logo 响应式调整 */
        .logo {
            max-width: min(200px, 60%);
            height: auto;
        }
        
        /* 搜索表单响应式调整 */
        .search-form {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 12px;
            width: 100%;
            max-width: 584px;
            margin: 0 auto 32px;
        }
        
        @media (max-width: 768px) {
            .search-form {
                flex-direction: column;
                gap: 16px;
            }
            
            .search-input {
                width: 100%;
                margin-right: 0;
            }
            
            .search-button {
                width: 100%;
                max-width: none;
            }
        }
        
        /* AI 总结区域响应式调整 */
        .ai-summary {
            padding: 20px;
            margin: 20px 0;
        }
        
        /* 搜索结果响应式调整 */
        .result-item {
            padding: 15px;
        }
        
        /* 文字大小响应式调整 */
        @media (max-width: 480px) {
            .search-input {
                font-size: 16px;
                padding: 12px 20px; /* 增大的点击区域 */
                width: 100%; /* 使用可用宽度 */
            }
            
            .search-button {
                padding: 10px 20px; /* 缩小按钮尺寸 */
                max-width: 80px; /* 限制最大宽度 */
                font-size: 14px; /* 适当缩小字号 */
                margin-left: 0; /* 移除左侧边距 */
            }
            
            .search-form {
                gap: 8px; /* 缩小元素间距 */
            }
        }
        
        /* 平板设备优化 */
        @media (min-width: 769px) and (max-width: 1024px) {
            .search-container {
                width: 95%;
                padding: 25px;
            }
            
            .search-form {
                max-width: 700px;
            }
            
            .result-item {
                padding: 18px;
            }
        }
        
        /* 触摸设备交互优化 */
        @media (hover: none) {
            .search-button:hover {
                transform: none;
            }
            
            .result-item:hover {
                transform: none;
            }
            
            .think-header:hover {
                background: rgba(30, 41, 59, 0.5);
            }
        }
        
        /* 确保内容不会溢出容器 */
        img, video, iframe {
            max-width: 100%;
            height: auto;
        }
        
        /* 优化长 URL 显示 */
        .result-url {
            word-break: break-all;
        }
        
        /* 优化代码块显示 */
        .markdown-body pre {
            background-color: rgba(0, 0, 0, 0.25); /* 黑色背景，透明度为 0.25 */
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        /* 全局文字颜色 */
        :root {
            --background-gradient-start:rgb(37, 6, 60);
            --background-gradient-middle:rgb(7, 3, 40);
            --background-gradient-end: #1F2937;
            --text-color: #e9e9e9;
        }

        body {
            background: linear-gradient(
                135deg,
                var(--background-gradient-start) 0%,
                var(--background-gradient-middle) 50%,
                var(--background-gradient-end) 100%
            );
            color: var(--text-color);
            background-size: 200% 200%;
            animation: gradientBG 6s ease-in-out infinite;
            min-height: 100vh;
        }

        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* 添加 logo 样式 */
        .logo-container {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo {
            max-width: 200px;
            height: auto;
        }
        
        input[type="text"] { width: 80%; padding: 10px; margin-right: 10px; }
        button { padding: 10px 20px; }
        .result-item { margin: 20px 0; padding: 10px; border-bottom: 1px solid #eee; }
        .result-item a { color: #1a0dab; text-decoration: none; }
        .result-item a:hover { text-decoration: underline; }
        .ai-summary { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* 删除第一个 .ai-summary 定义 */
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .ai-summary { 
            /* 基础样式 */
            padding: 35px;
            margin: 25px 0;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
            
            /* 背景和模糊效果 */
            background: linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.3) 0%,
                rgba(59, 130, 246, 0.1) 50%,  /* 添加蓝色调 */
                rgba(30, 41, 59, 0.3) 100%
            );
            background-size: 400% 400%;  /* 扩大背景尺寸使动画更明显 */
            backdrop-filter: blur(8px);
            
            /* 边框和阴影效果 */
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 
                0 0 20px rgba(255, 255, 255, 0.1),  /* 增加外发光 */
                inset 0 0 30px rgba(59, 130, 246, 0.1);  /* 增加内发光并添加蓝色调 */
            
            /* 动画效果 */
            animation: gradientBG 5s ease-in-out infinite;  /* 放慢动画速度 */
        }

        /* 为文字添加渐变动画 */
        .ai-summary .markdown-body {
            background: linear-gradient(
                90deg,
                rgba(229, 231, 235, 0.7) 0%,
                rgba(229, 231, 235, 0.9) 50%,
                rgba(229, 231, 235, 0.7) 100%
            );
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            animation: textGradient 6s ease-in-out infinite;
        }

        @keyframes textGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 搜索框样式 */
        .search-form {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 12px;
            max-width: 584px;
            margin: 0 auto 32px;
        }
        
        .search-input {
            flex: 1;
            padding: 12px 16px;
            font-size: 14px;
            color: rgba(229, 231, 235, 0.9);
            background: transparent; /* 移除背景色 */
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            transition: all 0.3s ease;
            outline: none;
            backdrop-filter: blur(8px)        }

        .search-input::placeholder {
            color: rgba(229, 231, 235, 0.5);
        }
        
        .search-input:focus {
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(30, 41, 59, 0.6);
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
        }
        
        /* 搜索按钮样式 */
        .search-button {
            height: 42px;
            width: 80px; /* 改为固定宽度 */
            padding: 0 20px;
            font-size: 14px;
            font-weight: 500;
            color: rgba(229, 231, 235, 0.9);
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(8px);
        }
        
        /* 移除之前的响应式样式中关于搜索按钮宽度的设置 */
        @media (max-width: 480px) {
            .search-input {
                font-size: 16px;
                padding: 12px 20px;
                width: 100%;
            }
            
            .search-button {
                padding: 10px 20px;
                font-size: 14px;
                margin-left: 0;
            }
            
            .search-form {
                gap: 8px;
            }
        }
        
        .search-button:hover {
            background: rgba(59, 130, 246, 0.25);
            border-color: rgba(59, 130, 246, 0.3);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* markdown 样式 */
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: rgba(229, 231, 235, 0.9);
            background: transparent;
        }
        
        .markdown-body h3 {
            margin-top: 28px;
            margin-bottom: 18px;
            font-weight: 600;
            color: rgba(229, 231, 235, 0.9);
            font-size: 16px;
            letter-spacing: -0.02em;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 8px;
        }
        
        .markdown-body ul {
            padding-left: 1.8em;
            margin: 16px 0;
            color: rgba(229, 231, 235, 0.7);
        }
        
        .markdown-body li {
            margin: 8px 0;
            color: rgba(229, 231, 235, 0.7);
            line-height: 1.6;
        }
        
        .markdown-body strong {
            color: rgba(255, 165, 0, 0.9); /* 修改为亮黄色 */
            font-weight: 700; /* 加粗程度增加 */
            text-shadow: 0 0 8px rgba(255, 255, 0, 0.3); /* 添加发光效果 */
        }
        
        .markdown-body a {
            color: rgba(102, 217, 239, 0.9); /* 默认亮蓝色 */
            text-decoration: none; /* 移除下划线 */
            transition: all 0.3s ease;
            border-bottom: 1px solid rgba(102, 217, 239, 0.3); /* 添加底部边框 */
            padding-bottom: 1px; /* 为底部边框添加一点间距 */
        }
        
        .markdown-body a:hover {
            color: rgba(102, 217, 239, 1); /* 悬停时更亮 */
            border-bottom-color: rgba(102, 217, 239, 0.8); /* 悬停时边框更明显 */
            text-shadow: 0 0 8px rgba(102, 217, 239, 0.3); /* 添加发光效果 */
        }
        
        .markdown-body a:visited {
            color: rgba(128, 90, 213, 0.9); /* 点击后紫色 */
        }
        
        .markdown-body p {
            color: rgba(229, 231, 235, 0.7);
            margin: 16px 0;
            line-height: 1.6;
        }

        /* 删除所有重复的样式定义 */
        /*
        .result-item {
            padding: 20px;
            margin: 16px 0;
            background: #fff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
            overflow: hidden;
        }
        
        .result-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
        }
        
        .result-title {
            font-size: 16px;
            margin: 0 0 12px 0;
        }
        
        .result-title a {
            color: #2563eb;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .result-title a:hover {
            color: #1d4ed8;
        }
        
        .result-content {
            font-size: 14px;
            line-height: 1.6;
            color: #475569;
            margin: 8px 0;
        }
        
        .result-url {
            font-size: 12px;
            color: #64748b;
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 100%;
        }
        */
        .result-item {
            padding: 20px;
            margin: 16px 0;
            background: rgba(30, 41, 59, 0.4);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.3s ease;
            overflow: hidden;
            backdrop-filter: blur(8px);
            background: transparent; /* 移除背景色 */
        }
        
        .result-item:hover {
            transform: translateY(-1px);
            background: rgba(30, 41, 59, 0.5);
            border-color: rgba(255, 255, 255, 0.12);
            /* 移除阴影效果 */
        }
        
        .result-title {
            font-size: 16px;
            margin: 0 0 12px 0;
            color: rgba(229, 231, 235, 0.9);
        }
        
        .result-title a {
            color: rgba(229, 231, 235, 0.9);
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .result-title a:hover {
            color: #ffffff;
        }
        
        .result-content {
            font-size: 14px;
            line-height: 1.6;
            color: rgba(229, 231, 235, 0.7);
            margin: 8px 0;
        }
        
        .result-url {
            font-size: 12px;
            color: rgba(229, 231, 235, 0.5);
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 100%;
        }

        /* 推理样式 */
        .think-block {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            margin: 16px 0;
            overflow: hidden;
            backdrop-filter: blur(8px);
        }
        
        .think-header {
            padding: 12px 16px;
            background: rgba(30, 41, 59, 0.5);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            user-select: none;
            color: rgba(229, 231, 235, 0.9);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        .think-header:hover {
            background: rgba(30, 41, 59, 0.6);
        }
         
        /* 确保推理内容的颜色设置和布局 */
        .think-content .markdown-body,
        .think-content .markdown-body * {
            color: rgba(144, 164, 174, 0.85) !important; /* 温暖的低饱和度橙色 */
            margin: 10px; /* 添加上下左右内边距 */
        }
        
        .think-toggle {
            color: rgba(229, 231, 235, 0.6);
            font-size: 12px;
        }
        
        /* 修改 markdown 中的横线样式 */
        .markdown-body hr {
            display: none;
        }
        
        /* 亮白色居中线为半透明渐变图层 */
        .center-line {
            width: 100%;
            height: 30px; /* 调整高度以实现图层效果 */
            position: fixed;
            bottom: 0;
            left: 0;
            background: linear-gradient(to top, rgba(0, 0, 0, 0.5), transparent);
            backdrop-filter: blur(10px); /* 添加模糊毛玻璃效果 */
            z-index: 1000; /* 确保在最上层 */
        }

        /* 修改文字样式 */
        .powered-by {
            text-align: center;
            color: white;
            font-size: 10px;
            position: fixed;
            bottom: 10px; /* 距离窗口底部的距离 */
            left: 50%;
            transform: translateX(-50%);
            z-index: 1001; /* 确保在图层之上 */
        }
        
    </style>
</head>
<body>
    <div class="search-container">
        <!-- 添加 logo -->
        <div class="logo-container">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" class="logo">
        </div>
        <form action="/search" method="get" class="search-form">
            <input type="text" name="query" placeholder="请输入搜索内容..." value="{{ query }}" class="search-input">
            <button type="submit" class="search-button">搜索</button>
        </form>
        
        <div id="ai-summary-section">
            <div class="loading">
                <div class="loading-spinner"></div>
                <p class="loading-text">AI 正在分析结果，请稍候...</p>
            </div>
            <div class="ai-summary" style="display: none;">
                <h4 class="summary-title">深度搜索分析总结</h4>
                <div id="ai-summary-content" class="markdown-body">
                    {{ ai_summary_content | safe }}
                </div>
            </div>
        </div>

        {% if results %}
        <div class="results">
            <h2 class="results-title">搜索结果</h2>
            {% for result in results %}
            <div class="result-item">
                <h3 class="result-title"><a href="{{ result.url }}" target="_blank">{{ result.title }}</a></h3>
                <p class="result-content">{{ result.content }}</p>
                <small class="result-url">{{ result.url }}</small>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>

    {% if query %}
    <script>
        $(document).ready(function() {
            $('.loading').show();
            let content = '';
            let hasError = false;
            
            // 配置 marked
            marked.use({
                breaks: true,
                gfm: true
            });
            
            // 在调用 EventSource 时，确保包含 c 参数
            const eventSource = new EventSource(`/analyze?query={{ query | urlencode }}&c={{ request.args.get('c', '1') }}`);
            
            eventSource.onmessage = function(event) {
                try {
                    if (event.data === '[DONE]') {
                        eventSource.close();
                        return;
                    }
            
                    const data = JSON.parse(event.data);
                    if (data.error) {
                        hasError = true;
                        $('.loading').hide();
                        $('#ai-summary-content').html('AI 分析出现错误：' + data.error);
                        $('.ai-summary').show();
                        eventSource.close();
                        return;
                    }
                    
                    if (data.content !== undefined) {
                        content += data.content;
                        $('.loading').hide();
                        $('.results').addClass('shifted');
                        
                        // 处理推理内容
                        let parsedContent = content;
                        if (content.includes('<think>')) {
                            const thinkContent = content.match(/<think>([\s\S]*?)<\/think>/);
                            if (thinkContent) {
                                // 保存当前展开状态和内容
                                const existingBlock = $('.think-block');
                                const isExpanded = existingBlock.length ? existingBlock.hasClass('expanded') : false;
                                const existingContent = existingBlock.length ? existingBlock.find('.think-content .markdown-body').html() : '';
                                
                                const thinkHtml = `
                                    <div class="think-block${isExpanded ? ' expanded' : ''}" data-content-length="${thinkContent[1].length}">
                                        <div class="think-header">
                                            <span>推理过程</span>
                                            <span class="think-toggle">${isExpanded ? '收起' : '展开'}</span>
                                        </div>
                                        <div class="think-content">
                                            <div class="markdown-body">
                                                ${marked.parse(thinkContent[1])}
                                            </div>
                                        </div>
                                    </div>
                                `;
                                parsedContent = content.replace(/<think>[\s\S]*?<\/think>/, '');
                                parsedContent = thinkHtml + marked.parse(parsedContent);
                            }
                        } else {
                            parsedContent = marked.parse(content);
                        }
                        
                        $('#ai-summary-content').addClass('markdown-body').html(parsedContent);
                        $('.ai-summary').show().addClass('show');
                        
                        // 在内容更新后去除边框和阴影效果
                        if (data.content === '') {
                            $('.ai-summary').css({
                                'border': 'none',
                                'box-shadow': 'none'
                            });
                        }
                        
                        // 使用事件委托，并确保事件处理器只绑定一次
                        $('#ai-summary-content').off('click.think').on('click.think', '.think-header', function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            const $block = $(this).closest('.think-block');
                            const $content = $block.find('.think-content');
                            const $toggle = $(this).find('.think-toggle');
                            
                            $block.toggleClass('expanded');
                            $content.slideToggle(200);
                            $toggle.text($block.hasClass('expanded') ? '收起' : '展开');
                        });
                    }
                } catch (e) {
                    console.error('解析消息时出错:', e, event.data);
                    if (!hasError) {  // 只有在没有其他错误的情况下才显示错误
                        hasError = true;
                        $('.loading').hide();
                        $('#ai-summary-content').html('AI 分析出现错误：' + e.message);
                        $('.ai-summary').show();
                    }
                    eventSource.close();
                }
            };
            
            eventSource.onerror = function(event) {
                console.error('EventSource 错误:', event);
                if (!hasError) {  // 只有在没有其他错误的情况下才显示错误
                    $('.loading').hide();
                    $('#ai-summary-content').html('AI 分析出现错误，请稍后重试');
                    $('.ai-summary').show();
                }
                eventSource.close();
            };
        });
    </script>
    {% endif %}
    <!-- 添加亮白色居中线和文字 -->
    <div class="center-line"></div>
    <div class="powered-by">Powered by Lokyshin</div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, query="", results=None)

# 在 search 函数中添加敏感词检查
# 在文件开头添加函数定义
def check_sensitive_words(query):
    """检查查询词是否包含敏感词
    Args:
        query: 查询词
    Returns:
        bool: 是否包含敏感词
    """
    
    sensitive_words_path = os.path.join(os.path.dirname(__file__), 'static', 'sensitive_words_lines.txt')
    
    try:
        with open(sensitive_words_path, 'r', encoding='utf-8') as f:
            sensitive_words = [word.strip() for word in f.readlines()]
            
        for word in sensitive_words:
            if not word or word.isspace():
                continue
            if query.strip().lower() == word.strip().lower():
                return True
        return False
    except FileNotFoundError:
        print("警告：未找到敏感词文件")
        return False

# 修改 search 函数中的敏感词检查部分
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return render_template_string(HTML_TEMPLATE, query="", results=None)

    # 检查敏感词
    if check_sensitive_words(query):
        return render_template_string(HTML_TEMPLATE, 
                                   query=query, 
                                   results=None, 
                                   error="检索内容包含敏感词，请修改后重试")
    
    try:
        # 请求 SearxNG 搜索引擎
        response = requests.get(
            SearxNG_URL,
            params={'q': query, 'format': 'json'},
            timeout=10
        )
        response.raise_for_status()
        search_results = response.json()
        results = search_results.get('results', [])
        
        if not results:
            return render_template_string(HTML_TEMPLATE, 
                                       query=query, 
                                       results=None, 
                                       error="未找到相关搜索结果")
        
        return render_template_string(HTML_TEMPLATE, query=query, results=results)
        
    except requests.RequestException as e:
        print(f"搜索请求错误: {str(e)}")
        return render_template_string(HTML_TEMPLATE, 
                                   query=query, 
                                   results=None, 
                                   error="搜索服务暂时不可用，请稍后重试")

@app.route('/analyze', methods=['GET'])
def analyze():
    from flask import Response
    query = request.args.get('query')
     
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # 检查敏感词
    if check_sensitive_words(query):
        def generate_error():
            yield f"data: {json.dumps({'error': '检索内容包含敏感词，请修改后重试'})}\n\n"
        return Response(generate_error(), mimetype='text/event-stream')

    def generate():
        try:
            # 请求 SearxNG 搜索引擎
            response = requests.get(
                SearxNG_URL,
                params={'q': query, 'format': 'json'},
                timeout=10
            )
            response.raise_for_status()
            search_results = response.json()
            results = search_results.get('results', [])
            
            if not results:
                yield f"data: {json.dumps({'error': '未找到相关搜索结果'})}\n\n"
                return

            content_for_analysis = "\n".join([
                f"标题: {result['title']}\n内容: {result['content']}\nURL: {result['url']}\n"
                for result in results
            ])

            data = {
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一个专业的信息助手。\n\n{content_for_analysis}"},
                    {"role": "user", "content": f"{query} 请对搜索结果进行专业的分析总结，列表展示并给出参考文献：\n\n{content_for_analysis}"}
                ],
                "stream": True
            }
            
            print("发送到 API 的数据:", json.dumps(data, ensure_ascii=False))
            
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=data,
                stream=True
            )
            
            print("API 响应状态码:", response.status_code)
            
            if response.status_code != 200:
                error_msg = f"API 返回错误状态码: {response.status_code}"
                print(error_msg)
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                return
            
            thinking_state = False  # 添加思考状态标记
            
            for line in response.iter_lines():
                if line:
                    try:
                        line_text = line.decode('utf-8')
                        print("收到的原始数据:", line_text)
                        
                        if line_text.startswith('data: '):
                            line_text = line_text[6:]
                        
                        if line_text.strip() == '[DONE]':
                            if thinking_state:  # 如果思考链还未结束，添加结束标记
                                yield "data: " + json.dumps({'content': '</think>\n\n'}) + "\n\n"
                            yield "data: [DONE]\n\n"
                            return
                            
                        json_data = json.loads(line_text)
                        print("解析后的 JSON:", json.dumps(json_data, ensure_ascii=False))
                        
                        if 'choices' in json_data and json_data['choices']:
                            delta = json_data['choices'][0].get('delta', {})
                            
                            # 处理思考链内容
                            reasoning = delta.get('reasoning_content', '')
                            if reasoning:
                                if not thinking_state:  # 如果还未开始思考链，添加开始标记
                                    thinking_state = True
                                    yield "data: " + json.dumps({'content': '<think>'}) + "\n\n"
                                yield "data: " + json.dumps({'content': reasoning}) + "\n\n"
                            
                            # 处理普通内容
                            content = delta.get('content', '')
                            if content:
                                if thinking_state:  # 如果正在思考链中，添加结束标记
                                    thinking_state = False
                                    yield "data: " + json.dumps({'content': '</think>\n\n'}) + "\n\n"
                                yield "data: " + json.dumps({'content': content}) + "\n\n"
                            elif json_data['choices'][0].get('finish_reason') == 'stop':
                                if thinking_state:  # 如果思考链还未结束，添加结束标记
                                    yield "data: " + json.dumps({'content': '</think>\n\n'}) + "\n\n"
                                yield "data: [DONE]\n\n"
                                return
                                
                    except json.JSONDecodeError as e:
                        print(f"JSON 解析错误: {str(e)}")
                        continue
                    except Exception as e:
                        print(f"处理响应时出错: {str(e)}")
                        continue

        except Exception as e:
            print(f"发生错误: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10880)