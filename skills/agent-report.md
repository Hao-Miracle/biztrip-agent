# Skill: AI 增强报表 · Agent Report

全链路智能扫描：LLM 路由分类 + LLM 专用提取 + LLM 出差聚合 + Excel 输出。

支持任意兼容 OpenAI 协议的服务商，不配 API Key 自动降级为纯规则引擎。

## 触发条件

用户需要智能扫描邮箱、生成差旅报销报表，希望 AI 自动识别新格式、自动聚合出差行程。

## 调用方式

```bash
python3 phase2/agent_report.py
```

## 前置准备

```bash
pip install python-dotenv PyPDF2 openpyxl openai
```

`.env` 中配置：

```
# 邮箱（必填）
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_authorization_code

# LLM（可选，不配则走纯规则引擎，零成本）
LLM_API_KEY=sk-your-api-key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

## 支持的服务商

任何兼容 OpenAI API 协议的模型，配置三行即可切换：

```bash
# DeepSeek
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 通义千问
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus

# Ollama 本地模型（完全免费，零联网）
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen2.5:7b
```

更多服务商（GLM、Kimi、SiliconFlow、火山引擎）配置见 `.env.example`。

## 处理流程

```
1. IMAP 连接邮箱 + 日期过滤
2. 🧠 LLM 路由分类 → 低置信度自动降级 📋 域名匹配
3. 🧠 LLM 品类专用提取 → 关键字段缺失自动降级 📋 正则提取
4. 🧠 LLM 出差聚合（时间+目的地归并）→ 失败自动降级 📋 规则聚合
5. 生成 Excel 三 Sheet 报表 + 附件归档
```

## 降级兜底

```
LLM 分类置信度 < 0.7  →  域名匹配兜底
LLM 提取字段缺失 > 50% →  正则提取兜底
LLM 聚合调用失败      →  基于目的地的规则聚合
```

不配 `LLM_API_KEY` 时全程规则引擎，和 `generate-report` 完全等效。

## 与 generate-report 的区别

| | generate-report | agent-report |
|------|------|------|
| 分类 | 域名+关键词规则 | 🧠 LLM 路由 + 规则降级 |
| 提取 | 正则解析器 | 🧠 LLM 专用 prompt + 规则降级 |
| 聚合 | 无 | 🧠 LLM 出差聚合 |
| API Key | 不需要 | 可选 |
| 成本 | 0 | 0（不配 Key）或 < 0.05 元/次 |

## 成本参考

| 模型 | 一次扫描（~5 封差旅邮件） |
|------|------|
| DeepSeek V3 | < 0.05 元 |
| GLM-4-Flash | 0 元（免费额度） |
| Ollama 本地 | 0 元 |

## Excel 输出

与 generate-report 同格式的三 Sheet 报表，报销总览页额外包含 LLM 出差行程汇总。

## 配套脚本

- `phase2/agent_report.py`：主入口
- `phase2/llm_classify.py`：LLM 分类模块
- `phase2/llm_extract.py`：LLM 提取模块
- `phase2/llm_aggregate.py`：LLM 聚合模块
- 级联调用 phase1 的规则引擎做降级兜底
