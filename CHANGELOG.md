# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/zh-CN/spec/v2.0.0.html).

---

## [0.1.0] - 2026-07-05

### 新增

#### 规则引擎（Phase 1）
- **IMAP 邮箱连接** — 支持 QQ/163/126/Gmail/Outlook 全平台邮箱，自动推断 IMAP 服务器
- **智能分类** — 域名匹配 + 关键词匹配双规则，分类准确率高
- **8 平台解析器** — 机票、火车票、酒店、网约车、发票、门票全覆盖
  - 机票：去哪儿、携程、飞猪、航司邮件
  - 火车票：12306、智行
  - 酒店：华住、Booking、携程、美团
  - 网约车：滴滴、高德（曹操/T3/及时/喜行等）
  - 发票：智慧发票(cresvtv.cn)、票根(txffp.com)
  - 门票：大麦
- **三 Sheet Excel 报表** — 报销总览 + 费用明细 + 按供应商统计
- **附件自动归档** — PDF/ZIP 原件自动下载，每条记录可溯源
- **金额提取优先级** — PDF 文件名 > 价税合计 > 合计...元 > ¥ 兜底

#### Agent 引擎（Phase 1.5）
- **LLM 分类** — 智能识别差旅邮件，置信度不足自动降级规则引擎
- **LLM 提取** — 结构化提取金额/日期/路线/订单号，关键字段缺失降级正则
- **出差聚合** — 按同一时间段+同一目的地归并为一次出差
- **多模型支持** — 兼容任何 OpenAI 协议的服务商（DeepSeek、通义千问、GLM、Kimi、Ollama 等）
- **零配置降级** — 不配 API Key 完全可用，自动降级纯规则引擎

#### Agent Skills
- **5 个 TRAE IDE Skill** — fetch-emails / classify-emails / extract-emails / generate-report / agent-report
- **5 个通用 Agent Skill** — Markdown 格式，支持 Claude Code / Cursor / GitHub Copilot / Windsurf / TRAE IDE

#### 知识库
- **LLM Wiki 知识库** — 产品定义、竞品分析、架构设计、功能规格、决策记录、任务拆解
- **SOUL.md** — Agent 身份定义、核心原则、工作流、边界

### 设计原则

1. **数据准确是底线** — 每一行金额、每一条日期、每一个路线都与邮件原文一致
2. **规则优先，零 API Key 可运行** — 默认基于规则引擎，零成本运行
3. **隐私优先** — 所有邮件数据仅在用户本地处理，只读邮箱权限
4. **两层可用** — 零配置规则引擎保证基本可用，配 LLM 升级智能提取

---

[0.1.0]: https://github.com/Hao-Miracle/BizTrip-Agent/releases/tag/v0.1.0
