import smtplib
import config

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send(subject, mailbody):
    system = config.getSystem()

    # 收件人邮箱
    areceiver = system["mail"]["to_account"]
    # 发件人地址
    from_addr = system["mail"]["from_account"]
    # 邮箱密码（授权码）
    password = system["mail"]["from_account_password"]

    # 邮件设置
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['to'] = areceiver
    msg['from'] = "clutch"

    # 添加邮件正文:
    msg.attach(MIMEText(mailbody, 'plain', 'utf-8'))

    # 设置邮箱服务器地址以及端口
    smtp_server = system["mail"]["smtp_server"]
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    # 登陆邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, areceiver.split(','), msg.as_string())
    # 断开服务器链接
    server.quit()
