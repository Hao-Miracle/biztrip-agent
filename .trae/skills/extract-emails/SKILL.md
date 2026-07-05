---
name: "extract-emails"
description: "Extract structured fields (amount, date, route, order number) from classified travel emails using platform-specific parsers. Invoke when user needs structured data from trip emails."
---

# Extract Emails

Extract structured fields from classified travel emails using 8 platform-specific parsers with generic regex fallback.

## Usage

```bash
python3 phase1/extract_emails.py
```

## Platform Parsers

| Parser | Platform | Fields Extracted |
|--------|----------|-----------------|
| `parse_qunar_flight` | 去哪儿网 | 金额, 订单号, 日期, 出发地/目的地 |
| `parse_didi` | 滴滴出行 | 金额, 日期, 出发地/目的地 |
| `parse_gaode` | 高德打车 | 金额, 日期 |
| `parse_12306` | 12306 | 金额, 日期, 车次 |
| `parse_huazhu` | 华住酒店 | 金额, 日期, 酒店名称, 发票号码 |
| `parse_crestv` | 智慧发票 | 金额, 商家, 品类(油费/餐饮) |
| `parse_txffp` | 票根 | 金额, 日期, 通行费类型 |
| `parse_ctrip_flight` | 携程 | 金额, 日期, 出发地/目的地 |

## Amount Extraction Priority

1. PDF filename amount (e.g. `1755.00.pdf`)
2. PDF text `价税合计(小写)` 
3. Body text `合计...元`
4. Body text `¥/￥` symbol
5. Body text `XX.XX 元`
6. Fallback: max `XX.XX` value in body

## Multi-encoding Support

UTF-8 → GBK → GB2312 → GB18030 → UTF-8 (errors=replace)

## PDF Processing

- Extracts text from PDF attachments via PyPDF2
- Appends PDF text to email body for unified extraction
- Emails without matching platform parser use `generic_extract()` fallback
