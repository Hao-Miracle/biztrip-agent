# Agent Skills 使用指南

BizTrip Agent 内置 5 个 AI Agent Skill，不绑定任何特定 IDE。通用格式的 Skill 定义文件存放在 `skills/` 目录下，支持几乎所有主流 AI Agent 环境。

---

## 支持的 Agent 平台

| 平台 | 状态 | 说明 |
|------|------|------|
| **TRAE IDE** | ✅ 原生支持 | `.trae/skills/` 目录自动加载 |
| **Claude Code** | ✅ 支持 | 引用 `skills/` 目录下的 `.md` 文件 |
| **Cursor** | ✅ 支持 | 复制到 `.cursor/rules/` 目录 |
| **GitHub Copilot** | ✅ 支持 | 追加到 `.github/copilot-instructions.md` |
| **Windsurf** | ✅ 支持 | 放入 `.windsurf/` 目录 |
| **其他兼容 MCP 的 Agent** | ✅ 支持 | 通过 MCP 文件系统调用 |

---

## 可用 Skill 列表

### 1. fetch-emails

**功能：** IMAP 连接邮箱，获取邮件列表和基础信息

**依赖：** `python-dotenv`

**适用场景：** 只需要看邮件列表，不需要提取详细信息

**使用方式：**
```bash
python3 phase1/fetch_emails.py
```

---

### 2. classify-emails

**功能：** 基于域名匹配 + 关键词双规则，智能分类差旅邮件

**依赖：** `python-dotenv`

**适用场景：** 先看看有哪些差旅邮件，再决定是否深入提取

**使用方式：**
```bash
python3 phase1/classify_emails.py
```

---

### 3. extract-emails

**功能：** 多平台解析器，提取金额、日期、路线、订单号等结构化信息

**依赖：** `python-dotenv PyPDF2`

**适用场景：** 需要提取具体的行程和费用信息

**使用方式：**
```bash
python3 phase1/extract_emails.py
```

---

### 4. generate-report

**功能：** 全链路扫描 → 三 Sheet Excel 报表 + 附件归档

**依赖：** `python-dotenv PyPDF2 openpyxl`

**适用场景：** 生成完整的报销报表，直接使用

**使用方式：**
```bash
python3 phase1/generate_report.py
```

---

### 5. agent-report

**功能：** LLM 增强版：智能分类 + 提取 + 出差聚合，多模型支持

**依赖：** 以上全部 + `openai`

**适用场景：** 需要更智能的识别和出差自动聚合

**使用方式：**
```bash
python3 phase2/agent_report.py
```

> 未配置 LLM API Key 时自动降级为纯规则引擎，零成本可用。

---

## 各平台使用方法

### TRAE IDE

无需额外配置，`.trae/skills/` 目录下的 Skill 会自动加载。直接在对话中触发即可：

> "帮我扫描一下最近的出差邮件，生成报销表"

### Claude Code

在项目目录下运行，通过 `/init` 或引用文件触发：

```bash
# 方式一：引用具体 Skill
/init skills/generate-report.md

# 方式二：直接对话，让 Claude 读取 skills 目录
```

### Cursor

将 Skill 文件复制到 `.cursor/rules/` 目录：

```bash
mkdir -p .cursor/rules
cp skills/*.md .cursor/rules/
```

然后 Cursor 会自动应用这些规则。

### GitHub Copilot

将 Skill 内容追加到 `.github/copilot-instructions.md`：

```bash
cat skills/generate-report.md >> .github/copilot-instructions.md
```

### Windsurf

放入 `.windsurf/` 目录：

```bash
mkdir -p .windsurf
cp skills/*.md .windsurf/
```

---

## 独立使用 Skill

如果你只需要某个特定功能，可以只下载对应的 Skill 和 Python 脚本：

```bash
# 下载 generate-report Skill
curl -o generate-report.md \
  https://raw.githubusercontent.com/Hao-Miracle/BizTrip-Agent/main/skills/generate-report.md

# 下载对应的 Python 脚本
curl -o generate_report.py \
  https://raw.githubusercontent.com/Hao-Miracle/BizTrip-Agent/main/phase1/generate_report.py

# 安装依赖
pip install python-dotenv PyPDF2 openpyxl
```

> 注意：`generate_report.py` 依赖同目录下的其他模块（`fetch_emails.py`、`classify_emails.py`、`extract_emails.py`），建议完整克隆仓库使用。

---

## Skill 工作原理

每个 Skill 都是一个纯文本的 Markdown 文件，包含：

1. **功能描述** — 告诉 Agent 这个 Skill 做什么
2. **触发条件** — 什么时候使用这个 Skill
3. **执行步骤** — 详细的操作指令
4. **注意事项** — 边界条件和约束

核心逻辑都在 `phase1/` 和 `phase2/` 的 Python 脚本中，Skill 只是告诉 Agent 如何调用这些脚本。

这种设计的好处：
- **可移植** — 换 IDE 不用重写
- **可审计** — 纯文本，随时查看内容
- **可定制** — 根据需要修改 Skill 指令

---

## 自定义 Skill

你可以基于现有 Skill 定制自己的版本。比如：

- 修改默认扫描的邮件数量
- 添加自定义的输出格式
- 集成到你自己的工作流中

只需要复制对应的 `.md` 文件，按你的需求修改即可。
