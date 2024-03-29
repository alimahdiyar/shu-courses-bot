import json
import pickle
from enum import Enum


class MenuState(Enum):
    GENERAL = "GENERAL"
    SEARCH_COURSE = 'SEARCH_COURSE'
    SELECT_DEPARTMENT = 'SELECT_DEPARTMENT'


SEMESTER = "13981"
users = []
sess_data = []


def save_users():
    f = open('users.txt', 'wb')
    pickle.dump(users, f)
    f.close()


def load_users():
    global users
    try:
        f = open('users.txt', 'rb')
        users = pickle.load(f)
        f.close()
    except FileNotFoundError:
        pass


def persian_text_to_arabic(string):
    return string.replace('ی', 'ي').replace('ک', 'ك')


def get_dep_by_id(dep_id):
    for dep in sess_data:
        if dep['id'] == dep_id:
            return dep


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.dep_id = '2903'
        self.menu_state = MenuState.GENERAL
        self.courses = []
        users.append(self)

    def search_course(self, qs):
        qs = persian_text_to_arabic(qs)
        result = []
        for course in get_dep_by_id(self.dep_id)['courses']:
            if qs in course['title']:
                result.append(course)
        return result

    def get_courses(self):
        result = []
        for department in sess_data:
            for course in department['courses']:
                if course['ident'] in self.courses:
                    result.append(course)
        return result

    def add_course(self, course_ident):
        if course_ident not in self.courses:
            self.courses.append(course_ident)

    def remove_course(self, course_ident):
        if course_ident in self.courses:
            self.courses.remove(course_ident)

    # def __eq__(self, num):
    #     return self.chat_id == num


def get_user(chat_id):
    for user in users:
        if user.chat_id == chat_id:
            return user
    u = User(chat_id)
    users.append(u)
    return u


def search_department(qs):
    qs = persian_text_to_arabic(qs)
    result = []
    for department in sess_data:
        if len(department['courses']) > 0 and qs in department['title']:
            result.append(department)
    return result


def all_departments():
    result = []
    for department in sess_data:
        if len(department['courses']) > 0:
            result.append(department)
    return result


def course_to_str(course):
    qstr = course['title'] + ' گروه ' + course['group'] + '\n' + course['gender'] + '\n' + course['time_room'] + '\n' + \
           course['teacher'] + '\n' + 'امتحان پایان ترم:' + course['final_date']
    return qstr


def load_data():
    global sess_data
    f = open('scrap/' + SEMESTER + '.txt', 'r')
    sess_data = eval(f.read())  # json.loads(f.read())
    f.close()
    load_users()


load_data()
