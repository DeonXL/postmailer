import re
import os

from config import PORT, SERVER, LOGIN, PWD

import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr

from bs4 import BeautifulSoup
from jinja2 import Template


def collection_info(template, subject, list_email, **params):
    # print('##### Колекция для отправки #####')
    # print(f'Шаблон письма: {template}')
    # print(f'Тема письма: {subject}')
    # print(f'Список адресатов: {list_email}')
    # print(f'Список адресатов: \n'
    #       f'Почта: {list_email[0].get("email")} \n'
    #       f'Имя: {list_email[0].get("name")} \n'
    #       f'Отчество: {list_email[0].get("second_name")} \n')
    # print(f'Дополнительные параметры: {params}')
    # print('##### ##################### #####')
    ok_list, err_list = [], []
    for email in list_email:
        print(f'что содержит переменная email - {email}')
        print(f'что такое email - {email.get("email")}')
        ok, error = send_email(template,
                               subject,
                               email.get('email'),
                               first_name=email.get('name'),
                               second_name=email.get('second_name'),
                               cert_name=email.get('cert_file'),

                               full_name=email.get('full_name'),
                               diplom_name=email.get('diplom_file'),

                               kyrator=email.get('kyrator'),
                               kyrator_tel=email.get('kyrator_tel'),
                               kyrator_email=email.get('kyrator_email'),
                               **params)
        ok_list.append(ok)
        err_list.append(error)
    return ok_list, err_list

def send_email(template, subject, email, **params):
    server = smtplib.SMTP_SSL(SERVER, PORT)
    server.login(LOGIN, PWD)
    # print(f'Переменная email: {email}')
    print(f'Переменная params текст емайла: {params.get("text_email")}')
    # print(f'Переменная team: {params.get("team")}')
    msg = MIMEMultipart()
    msg['From'] = LOGIN
    # msg['From'] = formataddr((str(Header('Техподдержка УМиИЦ', 'utf-8')), LOGIN))
    # msg['To'] = LOGIN
    msg['To'] = email
    msg['Subject'] = Header(subject, 'utf-8')
    html = open(template, encoding='utf-8').read()
    template_html = Template(html).render(subject_email=subject,
                                          first_name=params.get('first_name'),
                                          second_name=params.get('second_name'),
                                          text_email=params.get('text_email'),
                                          link_form=params.get('link_form'),
                                          link_teacher=params.get('link_teacher'),

                                          full_name=params.get('full_name'),

                                          kyrator=params.get('kyrator'),
                                          kyrator_tel=params.get('kyrator_tel'),
                                          kyrator_email=params.get('kyrator_email'),
                                          )
    body = BeautifulSoup(template_html, 'html.parser')
    msg.attach(MIMEText(body, 'html', 'utf-8'))

# Проверяем если вложение есть до прикрепляем к письму
    name_attachment = params.get('file_email', None)
    print("Файл",name_attachment)
    cert_attachment = params.get("cert_name", None)
    print("Сертификат",cert_attachment)
    diplom_attachment = params.get("diplom_name", None)
    print("Диплом",diplom_attachment)

    if name_attachment:
        file_attachment = os.path.basename(name_attachment.filename)
        # open_attach = MIMEApplication(open('upload/'+name_attachment, 'rb').read())
        file_attach = MIMEApplication(open('upload/'+name_attachment.filename, 'rb').read())
        encoders.encode_base64(file_attach)
        file_attach.add_header('Content-Disposition', 'attachment', filename=name_attachment.filename)
        msg.attach(file_attach)
    if cert_attachment:
        # print(cert_attachment)
        open_attach = MIMEApplication(open(cert_attachment, 'rb').read())
        encoders.encode_base64(open_attach)
        open_attach.add_header('Content-Disposition', 'attachment', filename=cert_attachment)
        msg.attach(open_attach)
    if diplom_attachment:
        # print(diplom_attachment)
        diplom_attach = MIMEApplication(open(diplom_attachment, 'rb').read())
        encoders.encode_base64(diplom_attach)
        diplom_attach.add_header('Content-Disposition', 'attachment', filename=diplom_attachment)
        msg.attach(diplom_attach)


    ok, error = [],[]
    try:
        server.sendmail(LOGIN, msg['To'], msg.as_string())
        server.quit()
        ok = f"{msg['To']} - OK"
    except BaseException as err:
        e = re.search('\(([^)]+)', str(err)).group(1)
        server.quit()
        error = f"{msg['To']} - {e}"
    return ok, error

# print(send_email())


