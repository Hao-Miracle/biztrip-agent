"""
模块3 · 结构化提取
对已分类的出差邮件，提取结构化字段（日期、金额、供应商等）

提取方式：基于规则的解析（针对各平台模板定制 + 通用正则兜底）
不需要 API Key。

用法：
    python3 phase1/extract_emails.py
"""

import imaplib
import email
from email.header import decode_header
import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ---------- 复用模块2的分类 ----------
# 域名规则（同 classify_emails.py）
DOMAIN_RULES = {
    '机票': ['qunar.com', 'ctrip.com', 'fliggy.com', 'alitrip.com', 'airchina', 'ceair.com', 'csair.com', 'trip.com'],
    '火车票': ['12306.cn', 'zhixing.com', 'tiexing.com'],
    '酒店': ['booking.com', 'agoda.com', 'airbnb.com', 'meituan.com', 'huazhuhotels.com'],
    '网约车': ['didiglobal.com', 'xiaojukeji.com', 'uber.com', 'amap.com'],
    '发票': ['crestv.cn', 'fapiao.com', 'invoice.', 'txffp.com'],
    '门票': ['damai.cn', 'maoyan.com', 'showstart.com'],
}

KEYWORD_RULES = {
    '机票': ['机票', '航班', '登机', '航空'],
    '火车票': ['火车票', '高铁', '动车', '12306'],
    '酒店': ['酒店', '民宿', '入住'],
    '网约车': ['滴滴', '网约车'],
    '发票': ['发票', '报销', '电子凭证'],
}

def decode_str(s):
    if not s: return ''
    parts = decode_header(s)
    result = []
    for content, charset in parts:
        if isinstance(content, bytes):
            try: result.append(content.decode(charset or 'utf-8', errors='replace'))
            except: result.append(content.decode('utf-8', errors='replace'))
        else: result.append(content)
    return ''.join(result)

def get_full_body(msg):
    """获取邮件完整正文（优先纯文本 → HTML降级 → PDF附件）"""
    body = ''
    pdf_texts = []
    
    # 先找纯文本
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                raw = part.get_payload(decode=True)
                if raw:
                    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                        try:
                            body = raw.decode(enc)
                            break
                        except: pass
                if body:
                    break
    
    # 没有纯文本，降级到 HTML
    if not body and msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                raw = part.get_payload(decode=True)
                if raw:
                    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                        try:
                            html = raw.decode(enc)
                            break
                        except: pass
                    else:
                        html = raw.decode('utf-8', errors='replace')
                    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
                    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
                    html = re.sub(r'<[^>]+>', '\n', html)
                    html = re.sub(r'\n{3,}', '\n\n', html)
                    html = re.sub(r'&nbsp;', ' ', html)
                    body = html.strip()
                break
    
    # 尝试从 PDF 附件提取
    if msg.is_multipart():
        for part in msg.walk():
            fn = part.get_filename()
            ct = part.get_content_type()
            # 解码文件名
            fn_decoded = decode_str(fn) if fn else ''
            is_pdf = (fn and fn.lower().endswith('.pdf')) or ct == 'application/pdf' or '.pdf' in fn_decoded.lower()
            if is_pdf:
                raw = part.get_payload(decode=True)
                if raw:
                    try:
                        from io import BytesIO
                        from PyPDF2 import PdfReader
                        reader = PdfReader(BytesIO(raw))
                        txt = ''
                        for page in reader.pages:
                            txt += page.extract_text() + '\n'
                        if txt.strip():
                            pdf_texts.append(txt.strip())
                    except:
                        pass
    
    # 合并正文和PDF文本
    if pdf_texts:
        body = body + '\n' + '\n--- PDF附件 ---\n'.join(pdf_texts)
    
    if not body:
        try:
            raw = msg.get_payload(decode=True)
            if raw:
                for enc in ['utf-8', 'gbk', 'gb2312']:
                    try:
                        body = raw.decode(enc)
                        break
                    except: pass
        except: pass
    
    return body or ''

# ========== 平台专用解析器 ==========

def parse_qunar_flight(body, subject):
    """去哪儿网机票"""
    data = {'平台': '去哪儿网', '品类': '机票'}
    # 金额：HTML中各种格式
    m = re.search(r'[价额共].*?(\d+\.?\d*)', body)
    if m: data['金额'] = float(m.group(1))
    else:
        m = re.search(r'(\d+\.\d{2})\s*元', body)
        if m: data['金额'] = float(m.group(1))
    # 订单号
    for p in [r'订单[号编][码号]?[：:]\s*(\w+)', r'(?:订单|订).*?(\d{10,})']:
        m = re.search(p, body)
        if m: data['订单号'] = m.group(1); break
    # 日期
    for p in [r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', r'出发[日期时间]*[：:]\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})']:
        m = re.search(p, body)
        if m: data['日期'] = m.group(1); break
    # 出发地→目的地
    m = re.search(r'([\u4e00-\u9fa5]{2,4})\s*[→\-]\s*([\u4e00-\u9fa5]{2,4})', body)
    if m:
        data['出发地'] = m.group(1)
        data['目的地'] = m.group(2)
    return data

def parse_didi(body, subject):
    """滴滴出行"""
    data = {'平台': '滴滴出行', '品类': '网约车'}
    m = re.search(r'(\d+\.?\d*)\s*元', body)
    if m: data['金额'] = float(m.group(1))
    m = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', body)
    if m: data['日期'] = m.group(1)
    # 路线
    m = re.search(r'([\u4e00-\u9fa5]{2,}[\u4e00-\u9fa50-9\-]*)\s*[至→\-]\s*([\u4e00-\u9fa5]{2,})', body)
    if m:
        data['出发地'] = m.group(1)
        data['目的地'] = m.group(2)
    return data

def parse_gaode(body, subject):
    """高德打车"""
    data = {'平台': '高德打车', '品类': '网约车'}
    m = re.search(r'(\d+\.?\d*)\s*元', body)
    if m: data['金额'] = float(m.group(1))
    m = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', body)
    if m: data['日期'] = m.group(1)
    return data

def parse_12306(body, subject):
    """12306 火车票"""
    data = {'平台': '12306', '品类': '火车票'}
    m = re.search(r'(\d+\.?\d*)\s*元', body)
    if m: data['金额'] = float(m.group(1))
    m = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', body)
    if m: data['日期'] = m.group(1)
    # 车次
    m = re.search(r'([GCDZ]\d{1,6})', body)
    if m: data['车次'] = m.group(1)
    return data

def parse_huazhu(body, subject):
    """华住酒店"""
    data = {'平台': '华住酒店', '品类': '酒店'}
    m = re.search(r'(\d+\.?\d*)\s*元', body)
    if m: data['金额'] = float(m.group(1))
    m = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', body)
    if m: data['日期'] = m.group(1)
    # 酒店名：从主题提取
    m = re.search(r'你好(.+?)酒店', subject)
    if m: data['酒店名称'] = m.group(1) + '酒店'
    # 发票号码（在主题中）
    m = re.search(r'发票号码[：:](\d+)', subject)
    if m: data['发票号码'] = m.group(1)
    return data

def parse_crestv(body, subject):
    """智慧发票服务平台"""
    data = {'平台': '智慧发票', '品类': '发票'}
    # 金额从主题中提取
    m = re.search(r'金额[：:](\d+\.?\d*)', subject)
    if m: data['金额'] = float(m.group(1))
    else:
        m = re.search(r'(\d+\.?\d*)\s*元', body)
        if m: data['金额'] = float(m.group(1))
    # 商家名称
    m = re.search(r'【(.+?)】', subject)
    if m: data['商家'] = m.group(1)
    # 发票分类
    if '油' in subject + body:
        data['品类'] = '发票(油费)'
    elif '餐' in subject + body:
        data['品类'] = '发票(餐饮)'
    return data

def parse_txffp(body, subject):
    """票根通行费"""
    data = {'平台': '票根', '品类': '发票(通行费)'}
    m = re.search(r'发票金额[：:]\s*(\d+\.?\d*)', body)
    if m: data['金额'] = float(m.group(1))
    m = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', body)
    if m: data['日期'] = m.group(1)
    else:
        m = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', body)
        if m: data['日期'] = m.group(1)
    m = re.search(r'(收费公路通行费|高速[公费]?通行费)', body)
    if m: data['类型'] = '通行费'
    return data

# ========== 通用提取（兜底）==========

def generic_extract(body, subject, category):
    """通用字段提取——任何品类都能提取的基础字段"""
    data = {'品类': category, '金额': None, '日期': None, '订单号': None, '供应商': None}
    
    # 金额：HTML 文本中常见的格式
    patterns = [
        r'发票金额[：:]\s*(\d+\.?\d*)',
        r'金额[：:]\s*(\d+\.?\d*)',
        r'价[格款][：:]\s*(\d+\.?\d*)',
        r'合计[：:]\s*(\d+\.?\d*)',
        r'总计[：:]\s*(\d+\.?\d*)',
        r'¥\s*(\d+\.?\d*)',
        r'(\d+\.\d{2})\s*元',
    ]
    for p in patterns:
        m = re.search(p, body)
        if m:
            data['金额'] = float(m.group(1))
            break
    
    if not data['金额']:
        # 从主题行提取金额
        m = re.search(r'金额[：:](\d+\.?\d*)', subject)
        if m: data['金额'] = float(m.group(1))
    
    # 日期
    patterns = [
        r'(\d{4}年\d{1,2}月\d{1,2}日)',
        r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})',
    ]
    for p in patterns:
        m = re.search(p, body)
        if m:
            data['日期'] = m.group(1)
            break
    
    # 订单号 / 发票号码
    m = re.search(r'(?:订单|发票)[号编][码号]?[：:（(]?\s*(\w{10,})', body)
    if m: data['订单号'] = m.group(1)
    
    return data


# ========== 主提取逻辑 ==========

# 平台 → 解析函数映射
PLATFORM_PARSERS = {
    'qunar.com': parse_qunar_flight,
    'xiaojukeji.com': parse_didi,
    'didiglobal.com': parse_didi,
    'crestv.cn': parse_crestv,
    'huazhuhotels.com': parse_huazhu,
    'amap.com': parse_gaode,
    '12306': parse_12306,
    'txffp.com': parse_txffp,
}


def extract_email(msg, category):
    """对单封邮件执行提取"""
    subject = decode_str(msg['Subject'])
    sender = decode_str(msg['From'])
    body = get_full_body(msg)
    
    # 查找匹配的平台解析器
    sender_lower = sender.lower()
    for domain, parser in PLATFORM_PARSERS.items():
        if domain in sender_lower:
            data = parser(body, subject)
            data['主题'] = subject
            data['发件人'] = sender
            return data
    
    # 没有匹配到平台解析器，使用通用提取
    data = generic_extract(body, subject, category)
    data['主题'] = subject
    data['发件人'] = sender
    return data


def _get_email_config():
    """获取邮箱配置，支持通用变量 + 向后兼容旧 QQ_EMAIL"""
    account = os.getenv('EMAIL_ACCOUNT', '') or os.getenv('QQ_EMAIL', '')
    password = os.getenv('EMAIL_PASSWORD', '') or os.getenv('QQ_AUTH_CODE', '')
    server = os.getenv('EMAIL_IMAP_SERVER', '') or os.getenv('QQ_IMAP_SERVER', '')
    port = int(os.getenv('EMAIL_IMAP_PORT', '') or os.getenv('QQ_IMAP_PORT', '0'))
    if not server:
        if '@163.com' in account: server = 'imap.163.com'
        elif '@126.com' in account: server = 'imap.126.com'
        elif '@gmail.com' in account: server = 'imap.gmail.com'
        elif '@outlook.com' in account or '@hotmail.com' in account: server = 'outlook.office365.com'
        else: server = 'imap.qq.com'
    if not port: port = 993
    return account, password, server, port


def main():
    email_addr, auth_code, imap_server, imap_port = _get_email_config()
    
    if not email_addr or not auth_code:
        print("❌ 请在 .env 中配置邮箱信息")
        print("   EMAIL_ACCOUNT=your_email@example.com")
        print("   EMAIL_PASSWORD=your_authorization_code")
        return
    
    try:
        conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        conn.login(email_addr, auth_code)
        conn.select('INBOX')
        
        status, data = conn.search(None, 'ALL')
        if status != 'OK' or not data[0]:
            print("收件箱为空")
            return
        
        mail_ids = data[0].split()
        recent_ids = mail_ids[-30:]
        
        extracted = []
        
        for mid in reversed(recent_ids):
            status, msg_data = conn.fetch(mid, '(RFC822)')
            if status != 'OK': continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = decode_str(msg['From'])
            subject = decode_str(msg['Subject'])
            body = get_full_body(msg)
            
            # 先分类
            # 规则同 classify_emails.py
            sender_lower = sender.lower()
            is_spam = any(d in sender_lower for d in ['job51', 'steampowered', '10000@', 'email.apple.com', 'cmbchina', '2ksports'])
            if is_spam:
                continue
            
            # 域名匹配
            category = None
            for cat, domains in DOMAIN_RULES.items():
                for domain in domains:
                    if domain in sender_lower:
                        category = cat
                        break
                if category: break
            
            # 关键词匹配
            if not category:
                text = subject.lower()
                for cat, keywords in KEYWORD_RULES.items():
                    for kw in keywords:
                        if kw in text:
                            category = cat
                            break
                    if category: break
            
            if not category:
                continue
            
            # 提取
            result = extract_email(msg, category)
            result['分类'] = category
            extracted.append(result)
            
            short = subject[:40] + '...' if len(subject) > 40 else subject
            amt = result.get('金额', '-')
            dt = result.get('日期', '-')
            print(f"✅ [{category}] {short}")
            print(f"   金额: {amt}  日期: {dt}")
            extra = {k: v for k, v in result.items() if k not in ('主题', '发件人', '分类', '金额', '日期', '品类')}
            if extra:
                print(f"   其他: {json.dumps(extra, ensure_ascii=False)}")
            print()
        
        conn.logout()
        
        # 汇总
        print("=" * 60)
        print(f"成功提取 {len(extracted)} 封邮件")
        print(f"可报销总额: {sum(e.get('金额') or 0 for e in extracted):.2f} 元")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()
