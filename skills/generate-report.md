# Skill: 报表生成 · Generate Report

全链路扫描：连接邮箱 → 分类 → 提取 → 生成三 Sheet Excel 报表 + 附件归档。

纯规则引擎，零 API Key 可运行。

## 触发条件

用户需要扫描邮箱、生成差旅报销 Excel 报表。

## 调用方式

```bash
python3 phase1/generate_report.py
```

运行后按提示输入日期范围（`YYYY-MM-DD`），直接回车则扫描最近 60 封。

## 前置准备

```bash
pip install python-dotenv PyPDF2 openpyxl
```

`.env` 中配置：
```
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_authorization_code
```

## 处理流程

```
1. IMAP 连接邮箱
2. 询问日期范围 → 搜索邮件
3. 对每封邮件：分类 → 提取正文+PDF文本 → 保存附件
4. 机票类按 PDF 附件拆分为独立记录
5. 汇总 → 生成 Excel
```

## 机票拆分规则

当分类为「机票」时，每个 PDF 附件生成一条独立记录。
PDF 文件名解析示例：
`2026-05-27 成都-甘孜-204482410162-机票电子发票-1755.00.pdf`
→ 日期: 2026-05-27, 出发: 成都, 到达: 甘孜, 金额: 1755.00

## Excel 输出

文件：`output/差旅汇总_YYYYMMDD.xlsx`

| Sheet | 内容 |
|------|------|
| 报销总览 | 总额卡片 + 按类别汇总（分类配色） |
| 费用明细 | 按日期排序，最高金额红色高亮 |
| 按供应商 | 各平台消费排名，隔行配色 |

分类配色：机票=蓝, 酒店=绿, 网约车=黄, 发票=粉, 火车票=靛蓝

## 附件归档

保存到 `output/附件/`：
- 保留：`.pdf`, `.zip`, 非广告图片
- 过滤：文件名含 logo, banner, icon, button, social, qrcode 的图片

## 同级 Skill

- **agent-report**：LLM 增强版，配 API Key 后启用智能分类+提取+出差聚合

## 配套脚本

- `phase1/generate_report.py`：主入口
- 级联调用：fetch → classify → extract
