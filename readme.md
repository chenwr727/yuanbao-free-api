# YuanBao-Free-API ✨

一个允许您通过 OpenAI 兼容接口访问腾讯元宝的服务。

## ✨ 核心特性

✅ **完整兼容 OpenAI API 规范**
🚀 **支持主流元宝大模型**（DeepSeek/HunYuan系列）
⚡️ **流式输出 & 网络搜索功能**
🖼️ **支持上传图片或文件**
🔐 **自动浏览器登录认证**
📦 **开箱即用的部署方案**（本地/Docker）

## ⚠️ 使用须知

- 本项目仅限**学习研究用途，请勿用于商业用途**
- **本项目可能导致账号被封禁风险**
- 请严格遵守腾讯元宝的[使用条款](https://yuanbao.tencent.com/)

## 🚀 快速开始

### 环境准备

```bash
# 克隆项目
git clone https://github.com/chenwr727/yuanbao-free-api.git
cd yuanbao-free-api

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，配置 API Keys
# 支持多个 key，用逗号分隔
# API_KEYS=sk-your-api-key-here,sk-another-api-key
```

## 🖥️ 服务端部署

### 本地运行

```bash
# 启动服务（首次启动会自动打开浏览器进行扫码登录）
python app.py

# 服务地址：http://localhost:8000
```

### Docker 部署

```bash
# 构建镜像
docker build -t yuanbao-free-api .

# 运行容器
docker run -d -p 8000:8000 --name yuanbao-api yuanbao-free-api
```

## 🧠 支持模型

| 模型名称              | 特性说明                    |
|----------------------|-----------------------------|
| deepseek-v3          | 深度求索 V3 基础模型         |
| deepseek-r1          | 深度求索 R1 增强模型         |
| deepseek-v3-search   | 深度求索 V3 模型（带搜索功能）|
| deepseek-r1-search   | 深度求索 R1 模型（带搜索功能）|
| hunyuan              | 腾讯混元基础模型             |
| hunyuan-t1           | 腾讯混元 T1 模型             |
| hunyuan-search       | 腾讯混元模型（带搜索功能）    |
| hunyuan-t1-search    | 腾讯混元 T1 模型（带搜索功能）|

## 🔧 配置说明

### 环境变量配置

在 `.env` 文件中配置以下变量：

```bash
# API 认证密钥（多个 key 用逗号分隔，必填）
API_KEYS=sk-your-api-key-here,sk-another-api-key

# Agent ID（默认为 naQivTmsDa，一般无需修改）
# AGENT_ID=naQivTmsDa

# 腾讯元宝页面 URL（默认为固定地址，一般无需修改）
# PAGE_URL=https://yuanbao.tencent.com/chat/naQivTmsDa

# 文件上传域名（默认为固定地址，一般无需修改）
# UPLOAD_HOST=hunyuan-prod-1258344703.cos.accelerate.myqcloud.com
```

### 认证机制

本项目使用浏览器自动化方式自动获取认证参数：

- 服务启动时自动启动无头浏览器
- 自动打开腾讯元宝登录页面
- 通过二维码扫码登录
- 自动拦截认证请求头（x-uskey 等）

**注意**：首次启动时需要在终端显示的二维码上完成扫码登录。

## 🌟 应用案例

[FinVizAI](https://github.com/chenwr727/FinVizAI) 实现多步骤金融分析工作流：
- 实时资讯搜索分析
- 市场趋势数据集成
- 结构化报告生成

[AI-Short-Video-Engine](https://github.com/chenwr727/AI-Short-Video-Engine) 一个基于 AI 的智能视频生成平台：
- 支持文章链接或主题文本输入（支持联网搜索）
- 自动完成内容理解与脚本生成
- 素材匹配、语音合成与视频剪辑一体化输出

## 📜 开源协议

MIT License © 2025

## 🤝 参与贡献

欢迎通过以下方式参与项目：
1. 提交 Issue 报告问题
2. 创建 Pull Request 贡献代码
3. 分享你的集成案例

## 🙏 致谢

- [Tencent YuanBao](https://yuanbao.tencent.com/) - 提供强大的 AI 能力
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Playwright](https://playwright.dev/) - 强大的浏览器自动化工具
