# from email import encoders
# from email.mime.base import MIMEBase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup as bs


def send_mail(data):
    email = "dmitrilay@gmail.com"  # Ваша почта
    password = "Aa@58800111"  # Ваш пароль
    from_user = "dmitrilay@gmail.com"  # электронная почта отправителя
    to_user = "dmitrilay@gmail.com"  # адрес электронной почты получателя
    subject = "Отчет об изменениях"  # тема письма (тема)

    msg = MIMEMultipart("alternative")  # инициализируем сообщение, которое хотим отправить
    msg["From"] = from_user  # установить адрес электронной почты отправителя
    msg["To"] = to_user  # установить адрес электронной почты получателя
    msg["Subject"] = subject  # задаем тему

    # установить тело письма как HTML
    html = f'{data}<br>Это письмо отправляется с помощью <b>Python</b>!'

    text = bs(html, "html.parser").text  # делаем текстовую версию HTML
    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    msg.attach(text_part)  # прикрепить тело письма к почтовому сообщению
    msg.attach(html_part)  # сначала прикрепите текстовую версию

    server = smtplib.SMTP("smtp.gmail.com", 587)  # инициализировать SMTP-сервер
    server.starttls()  # подключиться к SMTP-серверу в режиме TLS (безопасный) и отправить EHLO
    server.login(email, password)  # войти в учетную запись, используя учетные данные
    server.sendmail(from_user, to_user, msg.as_string())  # отправить электронное письмо
    server.quit()  # завершить сеанс SMTP
