---
name: "classify-emails"
description: "Classify emails by travel category using domain + keyword rule engine. Invoke when user needs to filter trip-related emails from inbox."
---

# Classify Emails

Rule-based classification engine that identifies travel-related emails and categorizes them by type.

## Usage

```bash
python3 phase1/classify_emails.py
```

Scans the 20 most recent emails by default.

## Classification Rules

### Domain Matching (priority 1)

| Category | Domains |
|----------|---------|
| 机票 | qunar.com, ctrip.com, fliggy.com, alitrip.com, airchina, ceair.com, csair.com, trip.com |
| 火车票 | 12306.cn, zhixing.com, tiexing.com |
| 酒店 | booking.com, agoda.com, airbnb.com, meituan.com, huazhuhotels.com |
| 网约车 | didiglobal.com, xiaojukeji.com, uber.com, amap.com |
| 发票 | crestv.cn, fapiao.com, txffp.com |
| 门票 | damai.cn, maoyan.com, showstart.com |

### Keyword Matching (fallback)

| Category | Keywords |
|----------|----------|
| 机票 | 机票, 航班, 登机, 航空, flight, boarding |
| 火车票 | 火车票, 高铁, 动车, 12306, 车票, train |
| 酒店 | 酒店, 民宿, 入住, booking confirmation, hotel |
| 网约车 | 滴滴, 网约车, 行程, 快车, 专车, 出租车 |
| 发票 | 发票, invoice, 报销, 电子凭证, receipt |

### Blacklist (direct skip)

job51, steampowered, email.apple.com, amazon, jd.com, taobao.com, weixin, alipay

## Output

Each email returns:
```python
{
    'is_relevant': bool,
    'category': '机票' | '火车票' | '酒店' | '网约车' | '发票' | '门票/活动' | '不相关' | '未识别',
    'method': '域名匹配' | '关键词匹配' | '黑名单' | '无匹配'
}
```

## Extending Rules

Add new platforms by editing `DOMAIN_RULES` / `KEYWORD_RULES` dicts in `classify_emails.py`.
