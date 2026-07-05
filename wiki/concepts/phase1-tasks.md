---
title: "Phase 1 任务拆解"
tags: [任务, Phase1, 项目管理]
created: 2026-07-04
updated: 2026-07-04
---

# Phase 1 任务拆解

> 共 33 个任务，全部已完成。

## 基础设施

| 编号 | 任务 | 状态 |
|------|------|------|
| T01 | 项目初始化：目录结构、`.gitignore`、`.env` 模板 | ✅ |
| T02 | 安装依赖：`python-dotenv`、`PyPDF2`、`openpyxl` | ✅ |
| T03 | 知识库搭建：`raw/` + `wiki/` + `SOUL.md` | ✅ |
| T04 | 规格说明文档 `phase1-spec.md` | ✅ |

## 模块开发

| 编号 | 任务 | 关联文件 | 状态 |
|------|------|------|------|
| T05 | IMAP 连接 + 多编码解码 + 邮件列表打印 | `fetch_emails.py` | ✅ |
| T06 | 域名匹配分类引擎（5 品类 × 20+ 平台） | `classify_emails.py` | ✅ |
| T07 | 关键词匹配兜底分类 | `classify_emails.py` | ✅ |
| T08 | 黑名单过滤（广告/电商/社交） | `classify_emails.py` | ✅ |
| T09 | HTML 正文清洗（去标签 + 去样式） | `extract_emails.py` | ✅ |
| T10 | PDF 附件文本提取（PyPDF2） | `extract_emails.py` | ✅ |
| T11 | ZIP 内 PDF 解压提取 | `generate_report.py` | ✅ |
| T12 | 去哪儿网机票解析器 | `extract_emails.py` | ✅ |
| T13 | 滴滴出行解析器 | `extract_emails.py` | ✅ |
| T14 | 高德打车解析器 | `extract_emails.py` | ✅ |
| T15 | 12306 火车票解析器 | `extract_emails.py` | ✅ |
| T16 | 华住酒店解析器 | `extract_emails.py` | ✅ |
| T17 | 智慧发票解析器 | `extract_emails.py` | ✅ |
| T18 | 票根通行费解析器 | `extract_emails.py` | ✅ |
| T19 | 携程机票解析器 | `generate_report.py` | ✅ |
| T20 | 通用正则兜底提取 | `extract_emails.py` | ✅ |

## 数据准确性

| 编号 | 任务 | 状态 |
|------|------|------|
| T21 | 金额六级优先级（PDF文件名 → 价税合计 → 合计元 → ¥ → XX.XX → 最大值兜底） | ✅ |
| T22 | 禁止取税额修复（`¥` 模式降到低优先级） | ✅ |
| T23 | 机票按 PDF 附件拆分记录 | ✅ |
| T24 | PDF 文件名解析日期/路线/金额 | ✅ |

## 输出

| 编号 | 任务 | 状态 |
|------|------|------|
| T25 | Excel Sheet 1：报销总览（总额卡片 + 分类汇总 + 配色） | ✅ |
| T26 | Excel Sheet 2：费用明细（日期排序 + 最高金额高亮） | ✅ |
| T27 | Excel Sheet 3：按供应商统计（隔行配色） | ✅ |
| T28 | 附件归档到 `output/附件/`（广告图片过滤） | ✅ |
| T29 | 交互式日期范围过滤 | ✅ |

## 验证与修复

| 编号 | 任务 | 状态 |
|------|------|------|
| T30 | 滴滴金额误取税额修复 | ✅ |
| T31 | 扫描范围从 60 封扩大到 200 封 | ✅ |
| T32 | 输出目录沙箱兼容修复 | ✅ |
| T33 | 清理 8 个一次性调试脚本 | ✅ |
