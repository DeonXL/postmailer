import pandas as pd


list_col = ['номинация',
            'школа',
            # 'преподаватель',
            'команда',
            'город',
            'ФИО',
            'E-mail',
            'Куратор ФИО',
            'Куратор ТЕЛ',
            'Куратор E-MAIL']

def table_diplom(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[list_col].values
    # print(table_value)
    diplom_values = []
    for i in table_value:
        diplom_value = {}
        diplom_value['event_name'] = i[0]
        diplom_value['school'] = i[1]
        diplom_value['team'] = i[2]
        diplom_value['city'] = i[3]
        diplom_value['full_name'] = i[4]

        diplom_value['email'] = i[5]
        diplom_value['kyrator'] = i[6]
        diplom_value['kyrator_tel'] = i[7]
        diplom_value['kyrator_email'] = i[8]
        diplom_value['diplom_file'] = f'{i[0]} {i[4]}_diplom.pdf'
        diplom_values.append(diplom_value)
    return diplom_values


# print(table_cert('upload/свидетельства.xlsx'))

import pdfkit


def html2pdf(name):
    path_wkthmltopdf = b'wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    css = b'templates/diplom/style1.css'
    options = {
        'orientation': 'landscape',
        'page-size': 'A4',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        'margin-top': '0mm',
    }
    try:
        pdfkit.from_file(f'{name}.html',
                         f'{name}_diplom.pdf',
                         configuration=config,
                         options=options, css=css)
    except OSError:
        pass


from jinja2 import Template
import base64


def image_file_path_to_base64_string(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()


import PyPDF2


def save_first_page(name):
    input_pdf = open(name, 'rb')
    reader = PyPDF2.PdfReader(input_pdf)

    output_pdf = PyPDF2.PdfWriter()
    output_pdf.add_page(reader.pages[0])

    with open(name, 'wb') as output_pdf_file:
        output_pdf.write(output_pdf_file)


def tamplate_diplom_html(table):
    name_diplom_list = []
    for diplom_html in table:
        print('Переменная TEAM',diplom_html.get('team'), "ТИП TEAM", type(str(diplom_html.get('team'))) )
        if str(diplom_html.get('team')) == 'nan':
            context = {
                'img_fon': image_file_path_to_base64_string('static/cert/fon-diplom.jpg'),
                'img_director': image_file_path_to_base64_string('static/cert/Подпись.png'),
                'img_pechat': image_file_path_to_base64_string('static/cert/печать.png'),

                'full_name': diplom_html.get('full_name'),
                'event_name': diplom_html.get('event_name'),

                'school': diplom_html.get('school'),
                'city': diplom_html.get('city')
            }
        else:
            context = {
                'img_fon': image_file_path_to_base64_string('static/cert/fon-diplom.jpg'),
                'img_director': image_file_path_to_base64_string('static/cert/Подпись.png'),
                'img_pechat': image_file_path_to_base64_string('static/cert/печать.png'),
                'team': diplom_html.get('team'),
                'full_name': diplom_html.get('full_name'),
                'event_name': diplom_html.get('event_name'),

                'school': diplom_html.get('school'),
                'city': diplom_html.get('city')
            }

        html = open('templates/diplom/diplom1.html', encoding='utf-8').read()
        tmp = Template(html)
        out_file = tmp.render(context)
        name_file = f"{diplom_html.get('event_name')} {diplom_html.get('full_name')}"
        with open(name_file + '.html', 'w', encoding='utf-8') as f:
            f.write(out_file)
            f.close()
        html2pdf(name_file)
        name_file_pdf = name_file + '_diplom.pdf'
        save_first_page(name_file_pdf)
        name_diplom_list.append(f'{name_file}_diplom.pdf')
    print(name_diplom_list)
    return name_diplom_list
