import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email(subject, body, config):
    msg = MIMEMultipart()
    msg['From'] = config['smtp_user']
    msg['To'] = config['alert_email']
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
    server.starttls()
    server.login(config['smtp_user'], config['smtp_password'])
    text = msg.as_string()
    server.sendmail(config['smtp_user'], config['alert_email'], text)
    server.quit()
