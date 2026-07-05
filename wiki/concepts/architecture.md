---
title: "技术架构"
tags: [技术, 架构, Phase1]
created: 2026-06-30
updated: 2026-06-30
sources: [raw/2026-06-30-project-plan.md]
---

# 技术架构

## Phase 1：工作流验证

使用自动化工作流工具（Hermes/n8n 等）搭建核心逻辑：

```text
用户邮箱 → IMAP 连接
  → LLM 逐封判断：是出差相关邮件吗？属于什么品类？
  → 提取结构化信息（日期、金额、供应商、出行人等）
  → 下载邮件附件
  → 按出差行程聚合（同一时间+同一目的地）
  → 生成 Excel（行程总表 + 各类目明细 + 报销汇总）
  → 输出到本地文件夹
```

## Phase 2：Web 应用

| 层 | 技术 | 理由 |
|----|------|------|
| 前端 | Next.js (React) | 前后端合一，一套代码 |
| 样式 | Tailwind CSS | 上手快，文档好 |
| 后端 | Next.js API Routes | 同一项目，不需两套 |
| 数据库 | SQLite (Turso) / PostgreSQL (Neon 免费版) | 存储结构化数据 |
| 邮箱 API | Gmail API + QQ邮箱API + 163邮箱IMAP | 只读权限 |
| AI 提取 | DeepSeek-V3 API | 中文好、价格低、国内可用 |
| Excel 生成 | SheetJS (xlsx) | 多维表格 |
| 文件存储 | Cloudflare R2 / Vercel Blob | 原件附件 |
| 部署 | Vercel (免费) | Next.js 原生平台 |

## 全品类识别清单

| 品类 | 来源 |
|------|------|
| 机票 | 携程、飞猪、航司官网等确认邮件 |
| 火车票 | 12306 确认邮件 |
| 酒店 | 携程、飞猪、Booking、美团等确认邮件 |
| 网约车 | 滴滴、高德等电子发票邮件 |
| 油费单 | 加油站电子发票邮件 |
| 发票 | 增值税发票、电子发票、定额发票等邮件 |
| 大巴/公交 | 如走邮件渠道 |

详见 [[features.md|功能范围]]。
