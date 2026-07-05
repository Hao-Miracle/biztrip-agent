# Skill: 邮箱连接 · Email Fetch

通过 IMAP 连接用户的邮箱，获取最近邮件列表，验证连接可用性。

## 触发条件

当用户需要测试邮箱连接、获取收件箱摘要、或扫描行程邮件时调用。

## 调用方式

```bash
python3 phase1/fetch_emails.py
```

## 前置准备

在 `.env` 中配置：
```
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_authorization_code
# 可选，代码会根据 @域名 自动推断 IMAP 服务器
# EMAIL_IMAP_SERVER=imap.qq.com
# EMAIL_IMAP_PORT=993
```

依赖：`python-dotenv`

## 支持的邮箱

| 邮箱 | 自动推断的 IMAP 服务器 |
|------|------|
| @qq.com | imap.qq.com |
| @163.com | imap.163.com |
| @126.com | imap.126.com |
| @gmail.com | imap.gmail.com |
| @outlook.com / @hotmail.com | outlook.office365.com |

授权码获取：
- QQ 邮箱：设置 → 账户 → POP3/IMAP/SMTP 服务
- 163/126：设置 → POP3/SMTP/IMAP
- Gmail：开启两步验证 → 生成应用专用密码

## 输出

控制台打印最近 10 封邮件的发件人、主题、日期。

## 配套脚本

- 主模块：`phase1/fetch_emails.py`
- 由以下 Skill 级联调用：`generate-report` / `agent-report`
