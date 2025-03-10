import pandas as pd


list_col = ['Наименование мероприятия',
            'Дата проведения',
            'Объём программы',
            'Фамилия', 'Имя', 'Отчество',
            'E-mail',
            'Дата выдачи',
            'Статус обучения',
            'Регистрационный номер',
            'Куратор ФИО','Куратор ТЕЛ','Куратор E-MAIL']

def table_cert(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[list_col].values
    # print(table_value)
    cert_values = []
    for i in table_value:
        cert_value = {}
        cert_value['event_name'] = i[0]
        cert_value['event_date'] = i[1]
        cert_value['program_size'] = i[2]
        cert_value['surname'] = i[3]
        cert_value['name'] = i[4]
        cert_value['second_name'] = i[5]
        cert_value['email'] = i[6]
        cert_value['date_of_issue'] = i[7]
        cert_value['status'] = i[8]
        cert_value['reg_number'] = i[9]
        cert_value['kyrator'] = i[10]
        cert_value['kyrator_tel'] = i[11]
        cert_value['kyrator_email'] = i[12]
        cert_value['cert_file'] = f'{i[3]}{i[4]}{i[5]}_cert.pdf'
        cert_values.append(cert_value)
    return cert_values
# print(table_cert('upload/свидетельства.xlsx'))

def table_kopilka(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[list_col].values
    # print(table_value)
    cert_values = []
    for i in table_value:
        cert_value = {}
        cert_value['event_name'] = i[0]
        cert_value['event_date'] = i[1]
        # cert_value['program_size'] = i[2]
        cert_value['surname'] = i[3]
        cert_value['name'] = i[4]
        cert_value['second_name'] = i[5]
        cert_value['email'] = i[6]
        cert_value['date_of_issue'] = i[7]
        cert_value['status'] = i[8]
        cert_value['reg_number'] = i[9]
        cert_value['kyrator'] = i[10]
        cert_value['kyrator_tel'] = i[11]
        cert_value['kyrator_email'] = i[12]
        cert_value['cert_file'] = f'{i[3]}{i[4]}{i[5]}_cert.pdf'
        cert_values.append(cert_value)
    return cert_values


import pdfkit

def html2pdf(name):
    path_wkthmltopdf = b'wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    css = b'templates/cert/style_new.css'
    options = {
        'orientation': 'Portrait',
        'page-size':'A5',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        'margin-top': '0mm',
        # 'page-width': '7.12in',
    }
    try:
        pdfkit.from_file(f'{name}.html',
                         f'{name}_cert.pdf',
                         configuration=config,
                         options=options, css=css)
    except OSError:
        pass

from jinja2 import Template
import base64

def image_file_path_to_base64_string(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def tamplate_html(table):
    name_cert_list = []
    for cert_html in table:
        context = {
            'img_fon': image_file_path_to_base64_string('static/cert/new_fon.png'),
            'img_director': image_file_path_to_base64_string('static/cert/Подпись.png'),
            'img_pechat': image_file_path_to_base64_string('static/cert/печать.png'),

            'surname': cert_html.get('surname'),
            'name': cert_html.get('name'),
            'second_name': cert_html.get('second_name'),
            'date': cert_html.get('event_date'),
            'subject':  cert_html.get('event_name'),
            'time': cert_html.get('program_size'),
            'number': cert_html.get('reg_number'),
            'date_in': cert_html.get('date_of_issue')
        }
        # print(context)
        html = open('templates/cert/index_new.html', encoding='utf-8').read()
        # html = open('templates/cert/index_kopilka.html', encoding='utf-8').read()
        tmp = Template(html)
        out_file = tmp.render(context)
        name_file = f"{cert_html.get('surname')}{cert_html.get('name')}{cert_html.get('second_name')}"
        with open(name_file+'.html', 'w', encoding='utf-8') as f:
            f.write(out_file)
            f.close()
        html2pdf(name_file)
        name_cert_list.append(f'{name_file}_cert.pdf')
    print(name_cert_list)
    return name_cert_list




