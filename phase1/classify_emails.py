"""
模块2 · 邮件分类（基于规则）
使用发件人域名 + 主题关键词判断邮件是否与出差/旅行相关

不需要 API Key，拿到就能跑。
规则覆盖已知差旅平台，可随时扩展。
"""

import imaplib
import email
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.utils import decode_str, get_email_config
from common.rules import DOMAIN_RULES, KEYWORD_RULES, SPAM_DOMAINS


def get_body_preview(msg, max_chars=300):
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            pass
    return body[:max_chars]


def extract_domain(sender):
    """从发件人地址中提取域名"""
    match = re.search(r'@([\w.-]+)', sender.lower())
    return match.group(1) if match else sender.lower()


def classify_by_domain(sender):
    """根据发件人域名分类"""
    domain = extract_domain(sender)
    for category, patterns in DOMAIN_RULES.items():
        for p in patterns:
            if p.lower() in domain or p.lower() in sender.lower():
                return category
    return None


def classify_by_keywords(subject, body):
    """根据主题和正文关键词分类"""
    text = (subject + ' ' + body).lower()
    for category, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw.lower() in text:
                return category
    return None


def is_spam(sender, subject):
    """判断是否为垃圾/无关邮件"""
    sender_lower = sender.lower()
    for domain in SPAM_DOMAINS:
        if domain.lower() in sender_lower:
            return True
    return False


def classify_email(sender, subject, body):
    """主分类函数"""
    
    # 先检查是否垃圾邮件
    if is_spam(sender, subject):
        return {'is_relevant': False, 'category': '不相关', 'method': '黑名单'}
    
    # 优先按域名分类（更准确）
    cat = classify_by_domain(sender)
    if cat:
        return {'is_relevant': True, 'category': cat, 'method': '域名匹配'}
    
    # 再按关键词分类
    cat = classify_by_keywords(subject, body)
    if cat:
        return {'is_relevant': True, 'category': cat, 'method': '关键词匹配'}
    
    return {'is_relevant': False, 'category': '未识别', 'method': '无匹配'}


def main(count=20):
    email_addr, auth_code, imap_server, imap_port = get_email_config()
    
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
            conn.logout()
            return
        
        mail_ids = data[0].split()
        recent_ids = mail_ids[-count:]
        
        relevant = []
        irrelevant = []
        
        print(f"\n正在分析最近 {len(recent_ids)} 封邮件...\n")
        
        for mid in reversed(recent_ids):
            status, msg_data = conn.fetch(mid, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = decode_str(msg['Subject'])
            sender = decode_str(msg['From'])
            body = get_body_preview(msg)
            
            result = classify_email(sender, subject, body)
            
            short_subject = subject[:45] + '...' if len(subject) > 45 else subject
            icon = '✅' if result['is_relevant'] else '  '
            
            print(f"{icon} [{result['category']}] ({result['method']})")
            print(f"    发件人: {sender[:45]}")
            print(f"    主题:   {short_subject}")
            
            if result['is_relevant']:
                relevant.append((sender, subject, result['category']))
            else:
                irrelevant.append((sender, subject))
            print()
        
        conn.logout()
        
        # 汇总
        print("=" * 60)
        print(f"总计 {len(recent_ids)} 封")
        print(f"出差/旅行相关: {len(relevant)} 封")
        print(f"无关邮件: {len(irrelevant)} 封")
        if relevant:
            print(f"\n识别到的差旅邮件：")
            for sender, subj, cat in relevant:
                print(f"  ✅ [{cat}] {subj[:50]}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()
