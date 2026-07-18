"""
邮件正文解析 —— 提取邮件文本 + PDF/ZIP 附件内容。

统一入口 get_email_text(msg)，所有模块复用。
"""

import re
from io import BytesIO

from common.utils import decode_str


def get_email_text(msg):
    """提取邮件正文 + PDF/ZIP 附件文本"""
    body = ''
    pdf_texts = []

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            raw = part.get_payload(decode=True)
            if not raw:
                continue

            if ct == 'text/plain':
                for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                    try:
                        body = raw.decode(enc)
                        break
                    except Exception:
                        pass
                if body:
                    break

            if ct == 'text/html' and not body:
                for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                    try:
                        html = raw.decode(enc)
                        break
                    except Exception:
                        pass
                else:
                    html = raw.decode('utf-8', errors='replace')
                html = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
                html = re.sub(r'<[^>]+>', '\n', html)
                html = re.sub(r'\n{3,}', '\n\n', html)
                html = re.sub(r'&nbsp;', ' ', html)
                body = html.strip()

    # PDF / ZIP 附件
    if msg.is_multipart():
        for part in msg.walk():
            fn_raw = part.get_filename()
            fn = decode_str(fn_raw) if fn_raw else ''
            ct = part.get_content_type()
            raw = part.get_payload(decode=True)
            if not raw:
                continue

            if fn.lower().endswith('.pdf') or ct == 'application/pdf':
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(BytesIO(raw))
                    for page in reader.pages:
                        t = page.extract_text()
                        if t:
                            pdf_texts.append(t)
                except Exception:
                    pass

            if fn.lower().endswith('.zip'):
                try:
                    import zipfile
                    zf = zipfile.ZipFile(BytesIO(raw))
                    for info in zf.infolist():
                        if not info.filename.lower().endswith('.pdf'):
                            continue
                        pdf_data = zf.read(info.filename)
                        from PyPDF2 import PdfReader
                        reader = PdfReader(BytesIO(pdf_data))
                        for page in reader.pages:
                            t = page.extract_text()
                            if t:
                                pdf_texts.append(t)
                    zf.close()
                except Exception:
                    pass

    if pdf_texts:
        body = body + '\n' + '\n'.join(pdf_texts)
    return body or ''
