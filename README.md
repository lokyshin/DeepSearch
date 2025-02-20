# Lokyshin Deep Search 🔍

![Flask](https://img.shields.io/badge/Flask-2.2.5-blue) 
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

下一代智能搜索聚合平台，深度融合搜索引擎与AI分析能力

[➤ 在线演示](https://lds.lokyshin.net)  |  [🚀 快速开始](#-快速开始)

## ✨ 核心功能

**搜索增强系统**
- 🚨 敏感词实时过滤（支持自定义词库）
- 🔍 多源搜索引擎聚合（基于SearxNG）
- 🎯 带权重的上下文相关性排序

**AI 增强模块**
- 💬 渐进式思维链呈现（支持折叠/展开）
- 📝 Markdown即时渲染（数学公式支持）
- ⚡ 流式响应（SSE协议实现）

**UI/UX 设计**
- 🌓 自适应暗色主题
- 🕶️ 毛玻璃特效界面
- 📱 响应式移动适配

## 🛠️ 技术栈

| 领域          | 技术组件                      |
|---------------|-----------------------------|
| **核心**      | DeepSeek-R1      |
| **搜索**      | SearxNG      |
| **后端**      | Flask      |
| **前端**      | Marked.js  |
| **安全**      | Dotenv  |

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/lokyshin/DeepSearch.git

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py
```

## ⚙️ 配置示例
.env 文件模板：
```bash
# AI 服务配置
API_KEY=sk_kG51vgc7hiWGkG51vgc7hk4Qh3BlRjtuqRb8eEX6rb #请输入正确的API_KEY
API_URL=https://api.baseurl.com/openai/v1/chat/completions #请输入正确的完整URL（到completions结束））
AI_MODEL=deepseek-r1

# 搜索引擎配置
SearxNG_URL=http://localhost:8080/search #假设你的SearxNG部署在localhost的8080端口，并配置打开了json格式（重要）
```

## 📂 项目结构
```bash
Lokyshing Deep Search/
├── app.py                                 # 主服务入口
├── static/                                # 前端资源
│   ├── favicon.ico                        # 网站icon
│   ├── apple-touch-icon.png               # 支持Apple设备的icon
│   ├── logo.png                           # 网站Logo
│   └── sensitive_words_lines.txt          # 敏感词列表（每个敏感词占一行））
└── .env                                   # 环境配置（git忽略）
```

## 📄 开源协议
MIT License - 自由修改和分发，需保留原许可声明
