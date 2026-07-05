---
name: "generate-report"
description: "Full pipeline: scan mailbox → classify → extract → generate Excel report with 3 sheets. Invoke when user wants to generate a complete reimbursement or travel expense report."
---

# Generate Report

Full pipeline that connects to mailbox, scans for travel emails, extracts structured data, and generates a formatted Excel report.

## Usage

```bash
python3 phase1/generate_report.py
```

## Interactive Flow

1. Connect to QQ mailbox via IMAP
2. Ask for date range filter (optional, format `YYYY-MM-DD`)
   - With dates: IMAP SINCE/BEFORE search
   - Without dates: default to latest 60 emails
3. Scan emails → classify → extract → aggregate
4. Generate Excel → save to `output/`

## Flight Ticket Splitting

When category is `机票`, each PDF attachment generates a separate record:
- Parse date from filename: `2026-05-27`
- Parse route from filename: `成都-甘孜`
- Parse amount from filename: `1755.00.pdf`

Example filename: `2026-05-27 成都-甘孜-204482410162-机票电子发票-1755.00.pdf`

## Attachment Archiving

Saved to `output/附件/`:
- **Keep**: `.pdf`, `.zip`, non-ad images (`.jpg`/`.png`/`.heic`)
- **Filter out**: images with advertising keywords in filename (logo, banner, icon, button, social, qrcode)

## Excel Output

File: `output/差旅汇总_YYYYMMDD.xlsx`

### Sheet 1: 报销总览 (Overview)
- Total amount card (¥ X,XXX.XX in blue)
- Category breakdown with color coding:
  - 机票: blue, 酒店: green, 网约车: yellow, 发票: pink, 火车票: indigo

### Sheet 2: 费用明细 (Detail)
- Columns: 序号, 日期, 类别, 供应商/平台, 金额, 出发地→目的地, 附件
- Sorted by date descending
- Highest amount highlighted in red bold

### Sheet 3: 按供应商 (By Vendor)
- Columns: 供应商, 笔数, 金额, 占比
- Sorted by amount descending
- Alternating row colors

## Prerequisites

- `.env` with `QQ_EMAIL` and `QQ_AUTH_CODE`
- Dependencies: `python-dotenv`, `PyPDF2`, `openpyxl`
- QQ mailbox IMAP enabled

## Notes

- Rule-based engine, zero API Key required
- All data processed locally
- ZIP attachments are decompressed to extract inner PDFs
- Ad images filtered by filename blacklist
