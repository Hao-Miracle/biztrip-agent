# 安装指南

本文档介绍如何安装和配置 BizTrip Agent。

---

## 前置要求

| 要求 | 说明 |
|------|------|
| **Python** | ≥ 3.8 |
| **邮箱** | 已开启 IMAP 服务，并获取授权码/应用专用密码 |
| **LLM API Key（可选）** | 如需 AI 增强功能，准备兼容 OpenAI 协议的 API Key |

---

## 支持的邮箱服务商

| 邮箱 | IMAP 服务器 | 端口 | 如何获取授权码 |
|------|-----------|------|--------------|
| QQ 邮箱 | `imap.qq.com` | 993 | 设置 → 账户 → POP3/IMAP/SMTP 服务 |
| 163 邮箱 | `imap.163.com` | 993 | 设置 → POP3/SMTP/IMAP → 开启并获取 |
| 126 邮箱 | `imap.126.com` | 993 | 同上 |
| Gmail | `imap.gmail.com` | 993 | 开启两步验证 → 生成应用专用密码 |
| Outlook/Hotmail | `outlook.office365.com` | 993 | 账户安全 → 应用密码 |

> 代码会根据 `@域名` 自动推断 IMAP 服务器，也可在 `.env` 中手动指定。

---

## 安装步骤

### 方式一：克隆仓库（推荐）

```bash
git clone https://github.com/Hao-Miracle/BizTrip-Agent.git
cd BizTrip-Agent
```

### 方式二：下载 ZIP

直接从 [Releases](https://github.com/Hao-Miracle/BizTrip-Agent/releases) 下载最新版本的 ZIP 包，解压后进入目录。

---

## 安装依赖

### 规则模式（零 API Key，推荐先试用）

```bash
pip install python-dotenv PyPDF2 openpyxl
```

### Agent 模式（LLM 增强，可选）

在规则模式基础上，额外安装：

```bash
pip install openai
```

---

## 配置

### 1. 复制配置模板

```bash
cp .env.example .env
```

### 2. 编辑配置文件

打开 `.env`，至少填入邮箱配置：

```env
# 邮箱账号
EMAIL_ACCOUNT=your_email@example.com

# 邮箱授权码（不是登录密码！）
EMAIL_PASSWORD=your_authorization_code
```

### 3. （可选）配置 LLM

如需 AI 增强功能，追加 LLM 配置：

```env
# DeepSeek 示例
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

更多服务商配置示例见 `.env.example`。

---

## 验证安装

运行以下命令验证是否正常：

```bash
python3 phase1/generate_report.py
```

如果提示输入日期范围，说明安装成功！直接回车扫描最近 60 封邮件。

---

## 常见安装问题

### Q: `ModuleNotFoundError: No module named 'xxx'`

A: 缺少依赖，重新安装：
```bash
pip install python-dotenv PyPDF2 openpyxl
```

### Q: 连接邮箱失败

A: 检查以下几点：
1. 邮箱是否开启了 IMAP 服务
2. 密码是否为**授权码**（不是登录密码）
3. 网络是否能访问 IMAP 服务器（企业网络可能有限制）

### Q: Python 版本不够

A: 升级 Python 到 3.8 或更高版本。推荐使用 [pyenv](https://github.com/pyenv/pyenv) 管理 Python 版本。

---

## 下一步

- 阅读 [使用指南](usage.md) 了解详细功能
- 查看 [常见问题](faq.md) 获取更多帮助
- 加入 [Discussions](../../discussions) 交流
