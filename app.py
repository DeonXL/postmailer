import os

from flask import Flask, request, render_template

# from parse_table import table_spam, table_courses, table_kopilka
from html2pdf_diplom import table_diplom, tamplate_diplom_html
from html2pdf import table_cert, tamplate_html, table_kopilka

from send_mail import collection_info, send_email

UPLOAD_FOLDER = 'upload/'
app = Flask(__name__)

app.config['FILE_UPLOADS'] = UPLOAD_FOLDER


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/spam', methods=['GET', 'POST'])
def spam():
    if request.method == 'POST':
        # Шаблон письма
        template_email = 'templates/sample_mail/temp_spam.html'
        # Тема письма
        subject_email = request.form['subject_email']
        # Текст письма
        text_email = request.form['text_email']
        # Вложение
        file_email = request.files['file_email']
        if file_email.filename != '':
            print(f'Файл {file_email.filename} присутствует сохраняем!')
            file_email.save(os.path.join(app.config['FILE_UPLOADS'], file_email.filename))
        else:
            print(f'Прикрепленные файлы отсутствуют!')
        # Таблица с адресами
        table_email = request.files['table_email']
        table_email.save(os.path.join(app.config['FILE_UPLOADS'], table_email.filename))
        # Получаем список адресов из таблицы
        list_email = table_cert(table_email)
        print(list_email)
        # Отправляем письма и формируем два списка успешно и ошибка
        ok_list, err_list = collection_info(template_email,
                                            subject_email,
                                            list_email,
                                            text_email=text_email)

        return render_template('list_spam.html',
                               ok_list=ok_list,
                               err_list=err_list)
    else:
        return render_template('spam.html')


@app.route('/kopilka', methods=['GET', 'POST'])
def kopilka():
    if request.method == 'POST':
        kopilka_template = 'templates/sample_mail/sample_kopilka.html'
        # kopilka_template = 'templates/sample_mail/sample_kopilka_otziv.html'

        subject_email = request.form['subject_email']
        link_form = request.form['link_form']

        table_email = request.files['table_email']
        table_email.save(os.path.join(app.config['FILE_UPLOADS'], table_email.filename))
        list_email = table_kopilka(table_email)
        print(list_email)
        ok_list, err_list = collection_info(kopilka_template,
                                            subject_email,
                                            list_email=list_email,
                                            link_form=link_form)
        return render_template('list_spam.html',
                               ok_list=ok_list,
                               err_list=err_list)
    else:
        return render_template('kopilka.html')


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == "POST":
        # Шаблон письма
        teach_template_email = 'templates/sample_mail/sample_webinar_teach.html'
        stud_template_email = 'templates/sample_mail/sample_webinar_stud.html'
        # Тема письма
        subject_email = request.form['subject_email']
        # Ссылка педагога
        link_teacher = request.form['link_teacher']
        # Ссылка на форму учета
        link_form = request.form['link_form']
        # таблица с ФИО и адресами
        table_email = request.files['table_email']
        table_email.save(os.path.join(app.config['FILE_UPLOADS'], table_email.filename))

        teacher, student = table_courses(table_email)
        print(teacher, student)
        teach_ok_list, teach_err_list = collection_info(teach_template_email,
                                                        subject_email,
                                                        teacher,
                                                        link_teacher=link_teacher)
        stud_ok_list, stud_err_list = collection_info(stud_template_email,
                                                      subject_email,
                                                      student,
                                                      link_form=link_form)

        return render_template('list.html',
                               ok_list_teach=teach_ok_list,
                               err_list_teach=teach_err_list,
                               ok_list_stud=stud_ok_list,
                               err_list_stud=stud_err_list)
    else:
        return render_template('from_webinar.html')


@app.route('/certificate', methods=['GET', 'POST'])
def cert():
    if request.method == 'POST':
        # Шаблон письма
        template_email = 'templates/sample_mail/sample_edu_doc.html'
        # Тема письма
        subject_email = request.form['subject_email']
        # Текст письма
        text_email = request.form['text_email']
        # таблица с ФИО и адресами
        table_email = request.files['table_email']
        table_email.save(os.path.join(app.config['FILE_UPLOADS'], table_email.filename))
        list_email = table_cert(table_email)
        # print(list_email)
        cert_list = tamplate_html(list_email)
        ok_list, err_list = collection_info(template_email,
                                            subject_email,
                                            list_email=list_email,
                                            file_name=cert_list,
                                            text_email=text_email)
        return render_template('list_spam.html', ok_list=ok_list, err_list=err_list)
    else:
        return render_template('dokuments.html')

@app.route('/diplom', methods=['GET', 'POST'])
def diplom():
    if request.method == 'POST':
        # Шаблон письма
        template_email = 'templates/diplom/sample_diplom_mail.html'
        # Тема письма
        subject_email = request.form['subject_email']
        # Текст письма
        text_email = request.form['text_email']
        # Вложение
        file_email = request.files['file_email']
        if file_email.filename != '':
            print(f'Файл {file_email.filename} присутствует сохраняем!')
            file_email.save(os.path.join(app.config['FILE_UPLOADS'], file_email.filename))
        else:
            print(f'Прикрепленные файлы отсутствуют!')
        # таблица с ФИО и адресами
        table_email = request.files['table_email']
        table_email.save(os.path.join(app.config['FILE_UPLOADS'], table_email.filename))
        list_email = table_diplom(table_email)
        # print(list_email)
        cert_list = tamplate_diplom_html(list_email)
        ok_list, err_list = collection_info(template_email,
                                            subject_email,
                                            list_email=list_email,
                                            file_name=cert_list,
                                            file_email=file_email)
        return render_template('list_spam.html', ok_list=ok_list, err_list=err_list)
    else:
        return render_template('diplom.html')
if __name__ == '__main__':
    app.run()
