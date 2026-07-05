---
title: "BizTrip Agent 知识库索引"
tags: [元数据, 导航]
created: 2026-06-30
updated: 2026-07-04
---

# BizTrip Agent 知识库索引

## 实体页面

| 页面 | 一句话 | 最后更新 |
|------|--------|---------|
| [[wiki/entities/product.md]] | BizTrip Agent 的产品定义、核心价值、发展阶段 | 2026-06-30 |
| [[wiki/entities/competitors.md]] | 竞品分析、市场空白、核心差异 | 2026-06-30 |

## 概念页面

| 页面 | 一句话 | 最后更新 |
|------|--------|---------|
| [[wiki/concepts/architecture.md]] | Phase 1 工作流 + Phase 2 Web 技术方案 | 2026-06-30 |
| [[wiki/concepts/features.md]] | MVP 功能清单和进化路径 | 2026-06-30 |
| [[wiki/concepts/decisions.md]] | 所有关键决策和排除方向的记录（含金额修复、PDF拆分等） | 2026-06-30 |
| [[wiki/concepts/workflow.md]] | 基于 Anthropic Agent 模式的三层工作流设计 | 2026-06-30 |
| [[wiki/concepts/phase1-spec.md]] | Phase 1 完整规格说明（输入/输出/验收标准） | 2026-07-04 |
| [[wiki/concepts/phase1-tasks.md]] | Phase 1 任务拆解（33 个任务，全部完成） | 2026-07-04 |
| [[wiki/concepts/agent-config.md]] | Agent 通用 LLM 接入配置说明（多服务商支持） | 2026-07-04 |

## TRAE Skills

| Skill | 一句话 | 位置 |
|------|--------|------|
| fetch-emails | IMAP 邮箱连接与邮件获取 | `.trae/skills/fetch-emails/` |
| classify-emails | 域名+关键词双规则邮件分类 | `.trae/skills/classify-emails/` |
| extract-emails | 8 平台专用解析器 + 通用兜底提取 | `.trae/skills/extract-emails/` |
| generate-report | 全链路扫描 → Excel 报表输出 | `.trae/skills/generate-report/` |
| agent-report | Agent 模式：LLM 增强 + 出差聚合 + 自动降级 | `.trae/skills/agent-report/` |

## 通用 Agent Skills（多平台）

| Skill | 说明 | 位置 |
|------|------|------|
| fetch-emails | IMAP 邮箱连接，通用 Agent 可读 | `skills/fetch-emails.md` |
| classify-emails | 规则分类引擎 | `skills/classify-emails.md` |
| extract-emails | 结构化提取 | `skills/extract-emails.md` |
| generate-report | 全链路报表生成 | `skills/generate-report.md` |
| agent-report | LLM 增强 Agent | `skills/agent-report.md` |

## 原始资料

| 文件 | 描述 | 日期 |
|------|------|------|
| [[raw/2026-06-30-完整项目方案.md]] | BizTrip Agent 完整项目方案（最全版本）| 2026-06-30 |
| [[raw/2026-06-30-project-plan.md]] | 项目计划书初版 | 2026-06-30 |
| [[raw/2026-06-29-需求探索过程.md]] | 从想法到方向的完整讨论记录 | 2026-06-29 |

## 待创建页面

- 工作流架构图（SVG/图表）
- Phase 1 Spec 待关联到 CI/测试流程
- Phase 2 Web 应用规划
