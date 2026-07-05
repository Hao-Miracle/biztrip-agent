"""
模块1 · 邮箱连接
QQ邮箱 IMAP 接入测试

用法：
    python3 phase1/fetch_emails.py

首次运行：
    确保 .env 配置了正确的邮箱信息
"""

import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def decode_str(s):
    """解码邮件标题等"""
    if not s:
        return ''
    parts = decode_header(s)
    result = []
    for content, charset in parts:
        if isinstance(content, bytes):
            try:
                result.append(content.decode(charset or 'utf-8', errors='replace'))
            except:
                result.append(content.decode('utf-8', errors='replace'))
        else:
            result.append(content)
    return ''.join(result)

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


def fetch_recent_emails(count=10):
    """连接邮箱，获取最近 N 封邮件的基本信息"""
    
    email_addr, auth_code, server, port = _get_email_config()
    
    if not email_addr or not auth_code:
        print("错误：请在 .env 文件中配置邮箱信息")
        print("  EMAIL_ACCOUNT=your_email@example.com")
        print("  EMAIL_PASSWORD=your_authorization_code")
        return
    
    try:
        print(f"正在连接 {server}:{port} ...")
        conn = imaplib.IMAP4_SSL(server, port)
        conn.login(email_addr, auth_code)
        print("✅ 登录成功")
        
        conn.select('INBOX')
        
        status, data = conn.search(None, 'ALL')
        if status != 'OK' or not data[0]:
            print("收件箱为空或搜索失败")
            conn.logout()
            return
        
        # 获取最近的 N 封邮件 ID
        mail_ids = data[0].split()
        recent_ids = mail_ids[-count:]
        
        print(f"\n最近 {len(recent_ids)} 封邮件：")
        print("-" * 60)
        
        for mid in reversed(recent_ids):
            status, msg_data = conn.fetch(mid, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = decode_str(msg['Subject'])
            sender = decode_str(msg['From'])
            date = msg['Date']
            
            print(f"发件人: {sender}")
            print(f"主题:   {subject}")
            print(f"日期:   {date}")
            print("-" * 60)
        
        conn.logout()
        print("✅ 连接已关闭")
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP 错误: {e}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")

if __name__ == '__main__':
    fetch_recent_emails(10)
