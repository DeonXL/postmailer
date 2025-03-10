import pandas as pd


def table_spam(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[["E-mail"]].values
    email = {}
    emails = []
    for i in table_value:
        email['email'] = i[0]
        emails.append(email)
    return emails

# print(table_spam('таблицы/вебинары.xlsx'))

def table_courses(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[["Имя", "Отчество",
                      "E-mail",
                      "Статус",
                      'Куратор ФИО',
                      'Куратор ТЕЛ',
                      'Куратор E-MAIL']].values
    teachers = []
    students = []
    for i in table_value:
        teacher = {}
        student = {}
        if 'Преподаватель' in i or 'преподаватель' in i:
            teacher['name'] = i[0]
            teacher['second_name'] = i[1]
            teacher['email'] = i[2]
            teacher['status'] = i[3]
            teacher['kyrator'] = i[4]
            teacher['kyrator_tel'] = i[5]
            teacher['kyrator_email'] = i[6]
            teachers.append(teacher)
            # print(i[0],'\n',i[1],'\n',i[2],'\n',i[3])
        else:
            student['name'] = i[0]
            student['second_name'] = i[1]
            student['email'] = i[2]
            student['status'] = i[3]
            student['kyrator'] = i[4]
            student['kyrator_tel'] = i[5]
            student['kyrator_email'] = i[6]
            students.append(student)
            # print(i[0], '\n', i[1], '\n', i[2], '\n', i[3])
    return teachers, students

# print(table_courses('таблицы/вебинары.xlsx'))

def table_kopilka(file):
    table = pd.read_excel(file)
    df = pd.DataFrame(table)
    table_value = df[['Секция',
                      'Имя', 'Отчество',
                      'E-mail',
                      'Куратор ФИО',
                      'Куратор ТЕЛ',
                      'Куратор E-MAIL']].values
    students = []
    for i in table_value:
        student = {}
        student['event_name'] = i[0]
        student['name'] = i[1]
        student['second_name'] = i[2]
        student['email'] = i[3]
        student['kyrator'] = i[4]
        student['kyrator_tel'] = i[5]
        student['kyrator_email'] = i[6]
        students.append(student)
    return students

#
