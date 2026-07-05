# BizTrip Agent

> 个人出差与旅行的行程与报销信息自动归集工具。
> 授权邮箱，AI 自动扫描确认邮件，提取结构化信息。出差中看行程，出差后一键生成报销表。

<p>
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-yellow" alt="python">
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/CHANGELOG-查看-8A2BE2" alt="changelog"></a>
</p>

## 🌟 核心价值

| 阶段 | 你需要什么 | 它做什么 |
|------|-----------|---------|
| **出差/旅行中** | 今晚住哪？明天几点车？航班号？ | 按行程聚合，一目了然 |
| **出差后** | 整理订单和发票，生成报销单 | 自动汇总，一键导出 Excel |
| **旅行后** | 整理行程记录 | 旅行日程表 |

## 🎯 两种模式，同一引擎

| 模式 | 输入 | 输出 |
|------|------|------|
| **出差** | 机票、火车票、酒店、网约车、油费单、发票 | 行程卡 + 报销汇总表 + Excel |
| **旅行** | 机票、火车票、酒店、门票、租车 | 行程卡 + 旅行日程表 |

> 底层识别和提取逻辑完全一样，仅输出不同。同一套引擎，零额外开发成本。

## 🏗 项目架构

```
biztrip-agent/
├── phase1/             ← 规则引擎（零依赖，必装）
│   ├── fetch_emails.py      ← IMAP 邮箱连接
│   ├── classify_emails.py   ← 规则分类（域名+关键词）
│   ├── extract_emails.py    ← 结构化提取（正则+PDF）
│   └── generate_report.py   ← 全链路输出（Excel+附件）
├── phase2/             ← Agent 引擎（LLM 增强，可选）
│   ├── llm_classify.py      ← LLM 路由分类 + 正则降级
│   ├── llm_extract.py       ← LLM 专用提取 + 正则降级
│   ├── llm_aggregate.py     ← LLM 出差聚合 + 规则兜底
│   └── agent_report.py      ← Agent 主入口
├── wiki/               ← 知识库（产品、架构、决策、规格）
├── raw/                ← 原始需求文档
├── skills/             ← 通用 Agent Skill 定义（Claude/Cursor/Copilot 都能用）
├── .trae/skills/       ← TRAE IDE 专用 Skill
├── .env.example        ← 配置模板
└── output/             ← 生成的报表（本地，不提交 Git）
```

## 🚀 快速开始

### 前置条件

- Python ≥ 3.8
- 邮箱需开启 IMAP 服务并获取授权码/应用专用密码：

| 邮箱 | IMAP 服务器 | 获取授权码 |
|------|-----------|-----------|
| QQ 邮箱 | `imap.qq.com` | 设置 → 账户 → POP3/IMAP/SMTP 服务 |
| 163 邮箱 | `imap.163.com` | 设置 → POP3/SMTP/IMAP → 开启并获取 |
| 126 邮箱 | `imap.126.com` | 同上 |
| Gmail | `imap.gmail.com` | 开启两步验证 → 生成应用专用密码 |
| Outlook/Hotmail | `outlook.office365.com` | 账户安全 → 应用密码 |

> 代码会根据 `@域名` 自动推断 IMAP 服务器，也可在 `.env` 中手动指定 `EMAIL_IMAP_SERVER`。

### 安装

```bash
git clone https://github.com/Hao-Miracle/biztrip-agent.git
cd biztrip-agent

# 规则模式（零 API Key）
pip install python-dotenv PyPDF2 openpyxl

# Agent 模式（LLM 增强，可选）
pip install openai
```

### 配置

```bash
cp .env.example .env
```

编辑 `.env`，填入自己的邮箱和授权码。如需 AI 增强，再填入 LLM 配置（详见下方）。

### 运行

```bash
# 规则模式（零 API Key）
python3 phase1/generate_report.py

# Agent 模式（AI 增强，不配 Key 自动降级规则模式）
python3 phase2/agent_report.py
```

运行后按提示输入日期范围（`YYYY-MM-DD`），直接回车则扫描最近 60 封邮件。

---

## 🤖 Agent 配置（零成本可用）

Agent 支持**任意兼容 OpenAI 协议的服务商**（含本地模型），配置 `.env` 三行即可切换：

```bash
# DeepSeek（推荐，中文好）
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 通义千问
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus

# Ollama 本地模型（完全免费，零联网）
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen2.5:7b
```

更多服务商（GLM、Kimi、SiliconFlow、火山引擎）配置示例见 `.env.example`。

### 降级策略

```
🧠 LLM 分类 → 置信度 < 0.7？→ 📋 域名匹配兜底
🧠 LLM 提取 → 关键字段缺失 > 50%？→ 📋 正则提取兜底
🧠 LLM 聚合 → 调用失败？→ 📋 基于目的地的规则聚合
```

**不配 `LLM_API_KEY` 完全可用**，自动降级纯规则引擎，零成本。

### 成本参考

| 模型 | 一次扫描（~5 封差旅邮件） |
|------|------|
| DeepSeek V3 | < 0.05 元 |
| GLM-4-Flash | 0 元（免费额度） |
| Ollama 本地 | 0 元 |

---

## 📊 输出说明

| 文件 | 说明 |
|------|------|
| `output/差旅汇总_YYYYMMDD.xlsx` | 三 Sheet Excel 报表 |
| `output/附件/` | 原始 PDF/ZIP 原件归档 |

### Excel 报表结构

| Sheet | 内容 |
|------|------|
| **报销总览** | 出差行程汇总 + 总额卡片 + 按类别汇总（分类配色） |
| **费用明细** | 所有记录，按日期排序，最高金额红色高亮，标注提取方法 |
| **按供应商** | 各平台消费排名，隔行配色 |

Agent 模式下，报销总览表额外包含**出差行程汇总**（LLM 自动聚合）。

---

## 🔧 支持的平台

| 品类 | 识别方式 | 覆盖平台 |
|------|---------|---------|
| 机票 | 域名 + 关键词 + LLM | 去哪儿、携程、飞猪、航司邮件 |
| 火车票 | 域名 + 关键词 + LLM | 12306、智行 |
| 酒店 | 域名 + 关键词 + LLM | 华住、Booking、携程、美团 |
| 网约车 | 域名 + 关键词 + LLM | 滴滴、高德（曹操/T3/及时/喜行等） |
| 发票 | 域名 + 关键词 + LLM | 智慧发票(cresvtv.cn)、票根(txffp.com) |
| 门票 | 域名 + 关键词 + LLM | 大麦 |

新增平台只需在 `classify_emails.py` 的 `DOMAIN_RULES` 加一行域名。

---

## 🧩 Agent Skills（支持多平台）

项目内置 5 个 AI Agent Skill，不绑定任何特定 IDE。`skills/` 目录下的 `.md` 文件是通用格式，**Claude Code、Cursor、GitHub Copilot、Windsurf、TRAE IDE** 等均可使用。

### 可用 Skill

| Skill | 做什么 | 需要安装 |
|------|------|------|
| **fetch-emails** | IMAP 连接邮箱，获取邮件列表 | `python-dotenv` |
| **classify-emails** | 域名+关键词双规则分类差旅邮件 | `python-dotenv` |
| **extract-emails** | 8 平台解析器，提取金额/日期/路线/订单号 | `python-dotenv PyPDF2` |
| **generate-report** | 全链路扫描 → 三 Sheet Excel + 附件归档 | `python-dotenv PyPDF2 openpyxl` |
| **agent-report** | LLM 增强版：智能分类+提取+出差聚合，多模型 | `python-dotenv PyPDF2 openpyxl openai` |

### 如何使用

**方式一：克隆仓库（推荐，所有 Skill 自动就绪）**

```bash
git clone https://github.com/Hao-Miracle/biztrip-agent.git
```

- **TRAE IDE**：`.trae/skills/` 自动加载，直接对话触发
- **Claude Code**：`/init` 或引用 `skills/` 目录下的 `.md` 文件
- **Cursor**：将 `skills/*.md` 复制到 `.cursor/rules/` 目录
- **Copilot**：将 Skill 内容追加到 `.github/copilot-instructions.md`

**方式二：只下载需要的 Skill**

```bash
# 下载 Skill 定义文件 + 对应 Python 脚本即可
curl -o skills/generate-report.md \
  https://raw.githubusercontent.com/Hao-Miracle/biztrip-agent/main/skills/generate-report.md

# 放入你的 Agent 能识别的位置
cp skills/generate-report.md .cursor/rules/
```

> Skill 是纯文本指令，核心能力在 `phase1/` 和 `phase2/` 的 Python 脚本中。单独下载 Skill 时需确保对应脚本也在项目中。

---

## 💡 设计原则

1. **两层可用** — 零配置规则引擎保证基本可用，配 LLM 升级智能提取，不配也完整
2. **金额准确第一** — PDF 文件名 > 价税合计 > 合计...元 > ¥ 兜底，禁止取税额
3. **机票按附件拆分** — 往返机票拆为独立记录，不从一封邮件合并
4. **出差+旅行双模式** — 同一引擎，切换输出模式，零额外开发成本
5. **附件自动归档** — PDF/ZIP 原件自动下载，每条记录可溯源
6. **隐私优先** — 所有数据本地处理，只读邮箱权限

---

## 🔭 路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| **Phase 1** | 规则引擎 — 域名+关键词+正则，零 API Key | ✅ 完成 |
| **Phase 1.5** | Agent 引擎 — LLM 增强 + 出差聚合 + 自动降级 | ✅ 完成 |
| **Phase 2** | Web 应用 — Next.js + 邮箱 OAuth + 可视化行程卡片 | 📋 规划中 |

---

## 📄 许可证

MIT

## 📝 变更日志

完整版本历史请查看 [CHANGELOG.md](CHANGELOG.md)。

## 🤝 贡献

- PR / Issue 欢迎
- 新增平台规则：在 `classify_emails.py` 的 `DOMAIN_RULES` 加一行域名
- 问题反馈：在 GitHub Issues 中描述你的邮箱平台和遇到的提取错误
