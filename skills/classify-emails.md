# Skill: 邮件分类 · Email Classify

基于域名+关键词双规则引擎，自动判断邮件是否与出差/旅行相关，并归类到具体品类。

## 触发条件

用户需要筛选收件箱中的差旅相关邮件，或作为全链路扫描的第一道过滤。

## 调用方式

```bash
python3 phase1/classify_emails.py
```

默认扫描最近 20 封邮件。

## 分类规则

### 域名匹配（优先级最高）

| 品类 | 匹配域名 |
|------|------|
| 机票 | qunar.com, ctrip.com, fliggy.com, alitrip.com, airchina, ceair.com, csair.com, trip.com |
| 火车票 | 12306.cn, zhixing.com, tiexing.com |
| 酒店 | booking.com, agoda.com, airbnb.com, meituan.com, huazhuhotels.com |
| 网约车 | didiglobal.com, xiaojukeji.com, uber.com, amap.com |
| 发票 | crestv.cn, fapiao.com, invoice.*, txffp.com |
| 门票 | damai.cn, maoyan.com, showstart.com |

### 关键词匹配（兜底）

| 品类 | 关键词 |
|------|------|
| 机票 | 机票, 航班, 登机, 航空, flight, boarding |
| 火车票 | 火车票, 高铁, 动车, 12306, 车票, train |
| 酒店 | 酒店, 民宿, 入住, booking, hotel |
| 网约车 | 滴滴, 网约车, 行程, 快车, 专车 |
| 发票 | 发票, invoice, 报销, 电子凭证, receipt |

### 黑名单

直接跳过（不分析）：job51, steampowered, email.apple.com, amazon, jd.com, taobao.com, weixin, alipay

## 输出

每封邮件一个分类结果：
```python
{'is_relevant': bool, 'category': str, 'method': '域名匹配'|'关键词匹配'|'黑名单'|'无匹配'}
```

## 扩展规则

编辑 `phase1/classify_emails.py` 中的 `DOMAIN_RULES` 字典即可新增平台。

## 配套脚本

- 主模块：`phase1/classify_emails.py`
- 由以下 Skill 级联调用：`generate-report` / `agent-report`
