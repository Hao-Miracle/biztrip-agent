---
name: "fetch-emails"
description: "Connect QQ mailbox via IMAP to fetch recent emails. Invoke when user needs to test email connection, retrieve email list, or scan inbox."
---

# Fetch Emails

Connect to QQ mailbox via IMAP SSL (port 993) and retrieve recent emails.

## Usage

```bash
python3 phase1/fetch_emails.py
```

## Prerequisites

- `QQ_EMAIL` and `QQ_AUTH_CODE` configured in `.env`
- QQ mailbox IMAP service enabled (Settings → Account → POP3/IMAP/SMTP)

## Behavior

- Fetches the most recent 10 emails by default
- Decodes Chinese email headers (subject, sender) using multi-encoding support (UTF-8 / GBK / GB2312 / GB18030)
- Prints: sender, subject, date for each email

## Error Handling

| Scenario | Output |
|----------|--------|
| `.env` missing config | "请在 .env 文件中配置 QQ_EMAIL 和 QQ_AUTH_CODE" |
| Login failure | "IMAP 错误: ..." |
| Empty inbox | "收件箱为空或搜索失败" |

## Notes

- Read-only operation; does not modify mailbox content
- All data processed locally only
- This is a connection test module; for full pipeline use `generate-report` skill
