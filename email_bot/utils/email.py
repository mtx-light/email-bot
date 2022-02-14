import smtplib
from email.mime.text import MIMEText

sent_from = "intbot"
sent_from += "@smiddle.com"

pss = "oQhgBdgpEC5sSYYOkl9apjTokKk9iFzy"

def send_email(to, topic, body):
    to_list = ['iurii.paustovskii@gmail.com', 'maxinmostlight@gmail.com', to]
    email_text = "\r\n".join([
        "From: %s",
        "To: %s",
        "Subject: %s",
        "",
        "%s", ])

    email_text = email_text % (sent_from, ", ".join(to_list), topic, str(body))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sent_from, pss)
    server.sendmail(sent_from, to, email_text.encode("utf8"))
    server.close()
    print('Email sent!')
