import sys  # sys нужен для передачи argv в QApplication
# import requests
from urllib.request import urlopen
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QStyleFactory

from functools import partial
from datetime import datetime
import random

from Login import Ui_LoginWindow
from main_ui_proba import Ui_MainWindow
from uch_to_achiv import Ui_Uch_to_achiv_Window
from achiv_info import Ui_achiv_info
from uch_info import Ui_Uch_info
# from collections import Counter
from lessons import Ui_lessons

# import socks
# db

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import auth
from firebase_admin import firestore

import qrcode

# import pyrebase


# Fetch the service account key JSON file contents
cred = credentials.Certificate('new_cubsappkotlin-firebase-adminsdk-ovpmb-f533780929.json')
firebase_admin.initialize_app(cred,{'storageBucket':'cubsappkotlin.appspot.com'})

db = firestore.client()

#cred = credentials.Certificate('cubapp-cd4ba-firebase-adminsdk-7xaqh-5688a100f9.json')

'''
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cubapp-cd4ba-default-rtdb.firebaseio.com/',
    'storageBucket':'cubsappkotlin.appspot.com'
})
'''
bucket = storage.bucket()
#blob = bucket.blob('UserImages/logo1.png')
#blob.upload_from_filename('logo1.png')
#blob.make_public()
#url = blob.public_url
#print(url)


# storage=firebase_admin.storage()
# storage.child("users_image/logo.png").put('logo.png')


# from wrong_pass import Ui_WrongWindow
rank = {
    "Никто": 0,
    "Новичок": 50,
    "Специалист 3 уровня": 100,
    "Специалист 2 уровня": 150,
    "Специалист 1 уровня": 200,
    "Эксперт 3 уровня": 250,
    "Эксперт 2 уровня": 300,
    "Эксперт 1 уровня": 350,
    "Ветеран 3 уровня": 400,
    "Ветеран 2 уровня": 450,
    "Ветеран 1 уровня": 500,
    "Мастер 3 уровня ": 600,
    "Мастер 2 уровня": 700,
    "Мастер 1 уровня": 800,
    "Великий мастер 3 уровня ": 1000,
    "Великий мастер 2 уровня": 1150,
    "Великий мастер 1 уровня": 1300,
    "Легенда": 10000
}
rank = list(rank.items())


class uch_to_achiv(QtWidgets.QMainWindow):
    submitted = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        # инициализация мейна
        super(uch_to_achiv, self).__init__(parent)

        self.ui = Ui_Uch_to_achiv_Window()
        self.ui.setupUi(self)
        # self.Main_window= main_window()

        self.ui.search_button.clicked.connect(self.search)

        self.ui.pushButton.clicked.connect(self.handleItemClicked)
        self.get_data()

    def get_data(self):
        users = db.reference('users').get()
        # print(users)

        users_count = len(users)
        for i in range(users_count):
            lenght = self.ui.tableWidget.rowCount()
            # print(lenght)
            rowPosition = self.ui.tableWidget.rowCount()
            # print(rowPosition)
            if rowPosition < users_count:
                self.ui.tableWidget.insertRow(rowPosition)

            users_list = users.get(list(users.keys())[i])
            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(i, 1, item)
            self.ui.tableWidget.item(i, 1).setText(str(users_list.get('user_ID')))
            # Фио
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(i, 0, item)
            self.ui.tableWidget.item(i, 0).setText(users_list.get('name'))
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget.setItem(i, 2, item)

    # проверка на отмеченные клетки
    def handleItemClicked(self, item):
        item_list = []
        print("on_submit")

        for i in range(self.ui.tableWidget.rowCount()):
            print(i)
            item_id = self.ui.tableWidget.item(i, 2)
            print(self.ui.tableWidget.item(i, 0).text())
            item_text = self.ui.tableWidget.item(i, 0).text()
            if item_id.checkState() == QtCore.Qt.Checked:
                item_list.append(item_text)
                print(" Checked")

            else:
                print(" Noncheked")

        print(item_list)
        # передача сообщения
        self.submitted.emit(
            item_list
        )
        self.close()
        # self.main_window().setText(self.ui.tableWidget.item(1, 0).text())

    # поиск
    def search(self):

        if self.ui.search_line.text() == "":
            for i in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.setRowHidden(i, False)
        else:
            # показ всех

            items_row = [itm.row() for itm in
                         self.ui.tableWidget.findItems(self.ui.search_line.text(), QtCore.Qt.MatchContains)]

            items1 = [itm.text() for itm in
                      self.ui.tableWidget.findItems(self.ui.search_line.text(), QtCore.Qt.MatchContains)]

            if len(items1) != 0:
                for i in range(self.ui.tableWidget.rowCount()):
                    self.ui.tableWidget.setRowHidden(i, False)

                # скрытие лишних
                for i in range(self.ui.tableWidget.rowCount()):
                    if i != items_row[0]:
                        self.ui.tableWidget.setRowHidden(i, True)


class achiv_info(QtWidgets.QMainWindow):
    submitted = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        # инициализация мейна
        super(achiv_info, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_achiv_info()
        self.ui.setupUi(self)

        # self.Main_window= main_window()

        # отключение всех подключений при закрытии

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("closed")
        try:
            self.ui.pushButton_9.clicked.disconnect()
            self.ui.pushButton.clicked.disconnect()
            self.ui.lineEdit_2.returnPressed.disconnect()
            self.ui.lineEdit_2.setEnabled(False)
        except Exception:
            pass

    # проверка на отмеченные клетки
    def saveAchivInfo(self, achivments_list=None):
        item_list = []
        print("on_submit")

        for i in range(self.achiv_info.ui.tableWidget.rowCount()):
            print(i)
            item_id = self.achiv_info.ui.tableWidget.item(i, 4)
            print(self.achiv_info.ui.tableWidget.item(i, 1).text())
            item_text = self.achiv_info.ui.tableWidget.item(i, 0).text()
            if item_id.checkState() == QtCore.Qt.Checked:
                self.achiv_info.ui.tableWidget.item(i, 2).setText(str(achivments_list[4][1]))

                item_list.append(item_text)
                print(" Checked")

            else:
                print(" Noncheked")

        print(item_list)
        # передача сообщения

    def displayInfo(self):
        self.show()


class uch_info(QtWidgets.QMainWindow):
    submitted = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        # инициализация мейна
        super(uch_info, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.ui = Ui_Uch_info()
        self.ui.setupUi(self)

    # отключение всех подключений при закрытии
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("closed")
        try:
            self.ui.lineEdit.returnPressed.disconnect()

        except Exception:
            pass
        try:

            self.ui.pushButton.clicked.disconnect()

        except Exception:
            pass
        try:

            self.ui.pushButton_2.clicked.disconnect()
        except Exception:
            pass

    def displayInfo(self):
        self.show()


class add_lessons(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        # инициализация мейна
        super(add_lessons, self).__init__(parent)

        self.ui = Ui_lessons()
        self.ui.setupUi(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("closed")

        try:
            self.ui.lineEdit.returnPressed.disconnect()
        except Exception:
            pass
        try:
            self.ui.pushButton_lesson.clicked.disconnect()
        except Exception:
            pass
        try:
            self.ui.pushButton_intensiv.clicked.disconnect()
        except Exception:
            pass

    def displayInfo(self):
        self.show()


# главное окно
class main_window(QtWidgets.QMainWindow):
    global imagePath, user_imagePath
    imagePath = ''
    user_imagePath = ''

    def __init__(self, parent=None):
        # инициализация мейна
        super(main_window, self).__init__(parent)
        self.achiv_info = achiv_info()
        self.uch_info = uch_info()
        self.add_lessons = add_lessons()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.get_data_from_db()

        self.ui.pushButton_add_uch_to_achiv.clicked.connect(self.edit_messages)

        self.ui.pushButton_select_image_2.clicked.connect(self.browseImage_2)
        self.ui.pushButton_delete_image.clicked.connect(self.delete_image_2)

        self.ui.pushButton_select_image_3.clicked.connect(self.browseImage_3)
        self.ui.pushButton_delete_image_2.clicked.connect(self.delete_image_3)
        # поиск
        self.ui.pushButton_uch_search.clicked.connect(self.search_uch)
        self.ui.pushButton_achiv_search.clicked.connect(self.search_achiv)

        # открытие информации
        self.ui.tableWidget_achiv.cellDoubleClicked.connect(self.open_achiv_Window)
        self.ui.tableWidget_uch.cellDoubleClicked.connect(self.open_uch_Window)
        # новый пользователь
        self.ui.pushButton_password_generation.clicked.connect(self.generate_password)
        self.ui.pushButton_add_new_uch.clicked.connect(self.add_new_uch)
        # новое достижение
        self.ui.pushButton_add_achive_2.clicked.connect(self.add_new_achiv)
        # посещения
        self.ui.pushButton_lesson.clicked.connect(self.lesson)
        self.ui.pushButton_intensiv.clicked.connect(self.lesson)
        self.ui.pushButton_club_1.clicked.connect(self.lesson)
        self.ui.pushButton_club_2.clicked.connect(self.lesson)
        self.ui.pushButton_club_3.clicked.connect(self.lesson)
        self.ui.pushButton_help_1.clicked.connect(self.lesson)
        self.ui.pushButton_help_2.clicked.connect(self.lesson)
        self.ui.pushButton_help_3.clicked.connect(self.lesson)
        self.ui.pushButton_festival.clicked.connect(self.lesson)

    # посещения
    def lesson(self):
        print("clicked")
        self.add_lessons.ui.lineEdit.clear()
        self.add_lessons.setWindowTitle(self.sender().text())
        self.add_lessons.ui.lineEdit.setFocus()
        if self.sender().text() == "Посещение занятий и мастер классов":
            point = 1
        elif self.sender().text() == "Посещение интенсивов" \
                or self.sender().text() == "Клубное событие 3 уровня" \
                or self.sender().text() == "Помощь клубу 3 уровня":
            point = 2
        elif self.sender().text() == "Клубное событие 2 уровня" \
                or self.sender().text() == "Помощь клубу 2 уровня":
            point = 4
        elif self.sender().text() == "Клубное событие 1 уровня" \
                or self.sender().text() == "Помощь клубу 1 уровня":
            point = 6
        elif self.sender().text() == "Участие в фестивале":
            point = 5

        # qr code
        qr_word = ''
        for x in range(20):  # Количество символов (16)
            qr_word = qr_word + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен qr-слово
        print(qr_word)
        img = qrcode.make(qr_word)
        img.save("qr_code.png")
        db.reference("pass_key").set(qr_word)

        self.add_lessons.ui.label.setPixmap(QtGui.QPixmap("qr_code.png"))
        self.add_lessons.ui.lineEdit.returnPressed.connect(partial(self.add_point, point, self.sender().text()))

        self.add_lessons.displayInfo()

    def add_point(self, point, achiv_text):
        print('point', point, achiv_text)
        user = db.reference('users').order_by_child('card_ID').equal_to(int(self.add_lessons.ui.lineEdit.text())).get()
        login = list(user)[0]

        users = db.reference('users')
        users_ref = users.child(login)
        user_id = users_ref.child("user_ID").get()

        achiv_search = 'None'
        # self.get_data_from_db()
        if achiv_text == "Посещение занятий и мастер классов":
            achiv_search = "Посетить занятия"
        elif achiv_text == "Посещение интенсивов":
            achiv_search = "Посетить интенсив"
        elif achiv_text == "Клубное событие 3 уровня":
            achiv_search = "Участвовать в клубном событии 3"
        elif achiv_text == "Помощь клубу 3 уровня":
            achiv_search = "Участвовать в помощи клубу 3"
        elif achiv_text == "Клубное событие 2 уровня":
            achiv_search = "Участвовать в клубном событии 2"
        elif achiv_text == "Помощь клубу 2 уровня":
            achiv_search = "Участвовать в помощи клубу 2"
        elif achiv_text == "Клубное событие 1 уровня":
            achiv_search = "Участвовать в клубном событии 1"
        elif achiv_text == "Помощь клубу 1 уровня":
            achiv_search = "Участвовать в помощи клубу 1"
        elif achiv_text == "Участие в фестивале":
            achiv_search = "Принять участие в фестивале"
        self.add_lessons.ui.lineEdit.clear()

        achiv_progress = users_ref.child('achiv_progress')
        achivments = db.reference('achivments').get()

        for i in range(len(achivments)):
            achivments_key = list(achivments[i].keys())
            achivments_value = list(achivments[i].values())
            # print(achivments_key, achivments_value, dict(zip(achivments_key, achivments_value)))
            achivment = dict(zip(achivments_key, achivments_value))
            user_progress = achivment['users_progress'][user_id]
            if achivment['name'].find(achiv_search) != -1 and type(user_progress) != str:
                print(achivment['name'], achivment['achiv_ID'], user_progress)
                # добавление очков в пользователя
                achiv_progress.update({
                    achivment['achiv_ID']: str(int(achiv_progress.child(str(achivment['achiv_ID'])).get()) + 1)
                })
                # добавление очков в достижение
                db.reference('achivments').child(str(achivment['achiv_ID'])).child('users_progress').update({
                    user_id: str(int(user_progress) + 1)
                })
                # проверка на выполнение достижения
                if user_progress + 1 >= achivment['points_need']:
                    achiv_progress.update({
                        achivment['achiv_ID']: str(datetime.today().day) + '.' + str(
                            datetime.today().month) + '.' + str(datetime.today().year)
                    })
                    db.reference('achivments').child(str(achivment['achiv_ID'])).child('users_progress').update({
                        user_id: str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(
                            datetime.today().year)
                    })
                    point += achivment['point']

        users_ref.update({
            'all_points': int(users_ref.child('all_points').get()) + point,
            'points': int(users_ref.child('points').get()) + point
        })
        self.get_data_from_db()

    # добавление нового достижения
    def add_new_achiv(self):

        name = self.ui.lineEdit_achiv_name_2.text()

        type = self.ui.comboBox_achiv_type.currentText()
        points_need = self.ui.spinBox_reward_search_3.value()
        image_url = 'None'

        users = db.reference('users').get()
        achivments = db.reference('achivments').get()
        achivments_count = len(achivments)
        point = 0
        if user_imagePath != '':
            blob = bucket.blob("achivments_image/achivments_" + str(achivments_count + 1) + ".png")
            blob.upload_from_filename(user_imagePath)
            blob.make_public()
            image_url = blob.public_url

        users_progress = {}
        for i in range(len(users)):
            users_progress.update({str(i): "0"})

        if self.ui.tableWidget_uch_in_achiv.rowCount() != 0:
            point = {}
            for i in range(len(users)):
                point.update({str(i): "0"})
            for i in range(self.ui.tableWidget_uch_in_achiv.rowCount()):
                point.update({self.ui.tableWidget_uch_in_achiv.item(i, 0).text(): int(
                    self.ui.tableWidget_uch_in_achiv.item(i, 2).text())})
                users_progress.update({self.ui.tableWidget_uch_in_achiv.item(i, 0).text():
                                           str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(
                                               datetime.today().year)})
                print(self.ui.tableWidget_uch_in_achiv.item(i, 0).text())
                print(self.ui.tableWidget_uch_in_achiv.item(i, 1).text())
                print(self.ui.tableWidget_uch_in_achiv.item(i, 2).text())

        if self.ui.spinBox_reward_search_2.isEnabled():
            print('value', self.ui.spinBox_reward_search_2.value())
            point = int(self.ui.spinBox_reward_search_2.value())

        achivment_data = {
            'achiv_ID': achivments_count,
            'achiv_image_URL': image_url,
            'name': name,
            'point': point,
            'points_need': points_need,
            'type': type,
            'users_progress': users_progress
        }

        db.reference("achivments").child(str(achivments_count)).set(achivment_data)
        print(achivment_data)
        achiv_progress1 = db.reference('achivments').child(str(achivments_count)).child('users_progress').get()
        print('achiv_progress1', achiv_progress1)

        for i in range(len(achiv_progress1)):
            print(list(db.reference('users').get())[i])
            users_list = users.get(list(users.keys())[i])
            id = users_list.get('user_ID')
            print('ID', id, list(db.reference('users').get())[i])

            db.reference('users').child(list(db.reference('users').get())[i]).child('achiv_progress').update(
                {str(achivments_count): achiv_progress1[id]})

            # db.reference('users').child(i).child("achiv_progress").update(      )
        self.get_data_from_db()

    # генерация пароля
    def generate_password(self):
        pas = ''
        for x in range(16):  # Количество символов (16)
            pas = pas + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен пароль
        self.ui.lineEdit_ush_pass.setText(pas)

    # добавление нового ученика
    def add_new_uch(self):


        email = self.ui.lineEdit_uch_login.text() + '@cubs.com'
        password = self.ui.lineEdit_ush_pass.text()
        login = self.ui.lineEdit_uch_login.text()

        user = auth.create_user(
            email=email,
            password=password)
        print("account added")
        image_url = 'None'




        achivments = db.collection('achivments').stream()
        achiv_progress={}
        for achivment in achivments:
            achiv_id=achivment.get("achivID")
            print(achiv_id)
            achiv_progress[achiv_id]="0"
        print(achiv_progress)
        user_id = ''
        for x in range(16):  # Количество символов (16)
            user_id = user_id + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен пароль


        print('imagePath', user_imagePath, type(user_imagePath))
        # print(storage.child("users_image/logo.png").get_url(user['idToken']))
        if user_imagePath != '':
            print("put in db")
            blob = bucket.blob("UserImages/user_" + user_id + ".png")
            blob.upload_from_filename(user_imagePath)
            blob.make_public()
            image_url = blob.public_url

        user_data = {
            'achivProgress': achiv_progress,
            "cart": {},
            "likes": {},
            "orders": {},
            "allPoints": 0,
            "cardId": 'None',
            "hours": 0,
            "login": login,
            "name": self.ui.lineEdit_uch_name.text(),
            "password": password,
            "points": 0,
            "userId": user_id,
            "userImageUrl": image_url,
            "userType":"CUSTOMER"
        }
        db.collection('users').add( user_data)
        '''
        for i in range(len(achivments)):
            achivments_list = list(achivments[i].items())
            db.reference('users').child(login).child('achiv_progress').update({str(i): "0"})
            db.reference('achivments').child(str(i)).child('users_progress').update({str(users_count): "0"})
        db.reference("users").child(login).set(user_data)
        '''
        self.get_data_from_db()

        # storage.child("users_image/logo.png").put(imagePath)   #put('logo1.png')

    def update_uch_data_from_db(self):
        # print("update from db")
        users = db.collection('users').stream()

        user_number = 1

        # Добавление учеников в список
        for user in users:
            lenght = self.ui.tableWidget_uch.rowCount()
            # print(lenght)
            rowPosition = self.ui.tableWidget_uch.rowCount()
            # print(rowPosition)
            if rowPosition < user_number:
                self.ui.tableWidget_uch.insertRow(rowPosition)

            # print("users_list",' ',users_list)
            # добавление данных в ячейки
            # ID

            self.ui.tableWidget_uch.item(user_number - 1, 0).setText(str(user.get('userId')))
            # print("ID", self.ui.tableWidget_uch.item(i, 0).text(), users_list)
            # Фио

            self.ui.tableWidget_uch.item(user_number - 1, 1).setText(user.get('name'))
            # кубиков всего

            self.ui.tableWidget_uch.item(user_number - 1, 2).setText(str(user.get('allPoints')))
            # кубикорубли

            self.ui.tableWidget_uch.item(user_number - 1, 3).setText(str(user.get('points')))
            # достижений

            achiv_counter = 0
            for achiv in user.get('achivProgress'):
                # print('achiv_count',achiv_count)
                if len(achiv) >= 7:
                    achiv_counter += 1
            self.ui.tableWidget_uch.item(user_number - 1, 4).setText(str(achiv_counter))
            # часов всего

            self.ui.tableWidget_uch.item(user_number - 1, 5).setText(str(user.get('hours')))

            self.ui.tableWidget_uch.item(user_number - 1, 6).setText(str(user.get('cardId')))
            user_number += 1
        # print("ID", self.ui.tableWidget_uch.item(0, 0).text())
        # self.ui.tableWidget_uch.sortItems(0)

    # данные из бд
    def get_data_from_db(self):

        start = datetime.now()

        print("get from db")
        users = db.collection('users').stream()

        user_number = 1
        # print(users)
        for user in users:
            #print(user.get('userId'))
            # Добавление учеников в список
            rowPosition = self.ui.tableWidget_uch.rowCount()

            if rowPosition < user_number:
                self.ui.tableWidget_uch.insertRow(rowPosition)

            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 0, item)
            self.ui.tableWidget_uch.item(user_number - 1, 0).setText(str(user.get('userId')))
            # print("ID",self.ui.tableWidget_uch.item(i, 0).text(),users_list)
            # Фио
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 1, item)
            self.ui.tableWidget_uch.item(user_number - 1, 1).setText(user.get('name'))
            # кубиков всего
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 2, item)
            self.ui.tableWidget_uch.item(user_number - 1, 2).setText(str(user.get('allPoints')))
            # кубикорубли
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 3, item)
            self.ui.tableWidget_uch.item(user_number - 1, 3).setText(str(user.get('points')))
            # достижений
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 4, item)
            achiv_counter = 0
            # print(users_list.get('achiv_progress'))

            for achiv_count in user.get('achivProgress').values():

                if len(achiv_count) >= 6:  # todo len(achiv_count) >=6:
                    achiv_counter += 1
            self.ui.tableWidget_uch.item(user_number - 1, 4).setText(str(achiv_counter))

            # часов всего
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 5, item)
            self.ui.tableWidget_uch.item(user_number - 1, 5).setText(str(user.get('hours')))
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 6, item)
            self.ui.tableWidget_uch.item(user_number - 1, 6).setText(str(user.get('cardId')))

            #print(user_number)
            rowPosition = self.ui.tableWidget_leaderboard.rowCount()
            if rowPosition < user_number:
                self.ui.tableWidget_leaderboard.insertRow(rowPosition)
            # таблица лидеров
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)
            self.ui.tableWidget_leaderboard.item(user_number - 1, 0).setText(str(user.get('userId')))
            # Фио
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)
            self.ui.tableWidget_leaderboard.item(user_number - 1, 0).setText(user.get('name'))
            # кубиков всего
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 1, item)
            self.ui.tableWidget_leaderboard.item(user_number - 1, 1).setText(str(user.get('allPoints')))
            user_number += 1

        # достижения
        achivments = db.collection('achivments').stream()
        achiv_number = 1
        for achivment in achivments:

            # print(lenght)
            rowPosition = self.ui.tableWidget_achiv.rowCount()
            # print(rowPosition)

            if rowPosition < achiv_number:
                self.ui.tableWidget_achiv.insertRow(rowPosition)

            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 0, item)
            self.ui.tableWidget_achiv.item(achiv_number - 1, 0).setText(str(achivment.get('achivID')))
            # название
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 1, item)
            self.ui.tableWidget_achiv.item(achiv_number - 1, 1).setText(achivment.get('name'))
            # награда
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 2, item)
            self.ui.tableWidget_achiv.item(achiv_number - 1, 2).setText(str(achivment.get('point')))
            # тип
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 3, item)
            self.ui.tableWidget_achiv.item(achiv_number - 1, 3).setText(achivment.get('type'))
            # ученики
            '''
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achivment, 4, item)
            string_for_achivments=""
            for j in range(len(achivments_list[6][1])):
                if len(achivments_list[6][1][j]) <=8:
                    pass
                else:
                    #print(j)
                    #print('check',' ',users.get(list(users.keys())[j]))
                    users_list = users.get(list(users.keys())[j])
                    string_for_achivments+=str(users_list.get('user_ID'))+' '

            self.ui.tableWidget_achiv.item(achivment, 4).setText(string_for_achivments)
            '''
            # %учеников
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 5, item)
            # print('users',Counter(achivments_list[5][1])["None"])
            counter = 0
            users_count = 0
            users = db.collection('users').stream()
            for user in users:
                users_count += 1

                if len(user.get('achivProgress').get(achivment.get('achivID'))) >= 8:
                    counter += 1
            self.ui.tableWidget_achiv.item(achiv_number - 1, 5).setText(str(round(counter / users_count * 100)))

            achiv_number += 1

        print(datetime.now() - start)

    # открытие карточки достижения
    def open_achiv_Window(self):
        row = self.ui.tableWidget_achiv.currentIndex().row()
        column = self.ui.tableWidget_achiv.currentIndex().column()
        print(row, column)
        achiv_id = self.ui.tableWidget_achiv.item(row, 0).text()

        users = db.collection('users').stream()

        user_number = 1

        achiv_counter = 0
        for i in db.collection('achivments').where(u'achivID', u'==', achiv_id).stream():
            achiv_info = i.to_dict()
        # print(achiv_info)
        for user in users:

            rowPosition = self.achiv_info.ui.tableWidget.rowCount()
            print(rowPosition)
            if rowPosition < user_number:
                self.achiv_info.ui.tableWidget.insertRow(rowPosition)

            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 0, item)
            self.achiv_info.ui.tableWidget.item(user_number - 1, 0).setText(user.get('userId'))
            # Фио
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 1, item)
            self.achiv_info.ui.tableWidget.item(user_number - 1, 1).setText(user.get('name'))
            # Прогресс
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEnabled)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 2, item)

            if len(user.get('achivProgress').get(achiv_id)) >= 8:
                self.achiv_info.ui.tableWidget.item(user_number - 1, 2).setText(str(achiv_info.get('pointsNeed')))
            else:
                self.achiv_info.ui.tableWidget.item(user_number - 1, 2).setText(user.get('achivProgress').get(achiv_id))

            # награда
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 3, item)

            if len(user.get('achivProgress').get(achiv_id)) >= 8:
                self.achiv_info.ui.tableWidget.item(user_number - 1, 3).setText(str(achiv_info.get('point')))
            else:
                self.achiv_info.ui.tableWidget.item(user_number - 1, 3).setText('0')

            # достижение
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.CheckState.Checked)

            if len(user.get('achivProgress').get(achiv_id)) >= 8:
                item.setCheckState(QtCore.Qt.CheckState.Checked)
                self.achiv_info.ui.tableWidget.setItem(user_number - 1, 4, item)
                achiv_counter += 1
            else:
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.achiv_info.ui.tableWidget.setItem(user_number - 1, 4, item)

            # дата
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 5, item)
            if len(user.get('achivProgress').get(achiv_id)) >= 8:
                self.achiv_info.ui.tableWidget.item(user_number - 1, 5).setText(user.get('achivProgress').get(achiv_id))

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.achiv_info.ui.tableWidget.setItem(user_number - 1, 6, item)
            self.achiv_info.ui.tableWidget.item(user_number - 1, 6).setText(user.get('cardId'))

            user_number += 1

        self.achiv_info.ui.groupBox_4.setTitle(achiv_info.get('name'))
        self.achiv_info.ui.label_31.setText(str(achiv_counter))
        self.achiv_info.ui.progressBar_3.setValue(int(self.ui.tableWidget_achiv.item(row, 5).text()))
        # self.achiv_info.ui.pushButton_9.clicked.connect(partial(self.saveAchivInfo,achivments_list))
        # self.achiv_info.ui.pushButton.clicked.connect(partial(self.add_user_in_achiv,achivments_list))
        self.achiv_info.displayInfo()

    # сохранение
    def saveAchivInfo(self, achivments_list):
        item_list = []
        print("on_submit")
        print(self.achiv_info.ui.lineEdit_2.text())

        for i in range(self.achiv_info.ui.tableWidget.rowCount()):
            print(i)
            item_id = self.achiv_info.ui.tableWidget.item(i, 4)
            print(self.achiv_info.ui.tableWidget.item(i, 1).text())
            item_text = self.achiv_info.ui.tableWidget.item(i, 0).text()
            print(self.achiv_info.ui.tableWidget.item(i, 5).text())
            if item_id.checkState() == QtCore.Qt.Checked and self.achiv_info.ui.tableWidget.item(i, 5).text() == '':

                self.achiv_info.ui.tableWidget.item(i, 2).setText(str(achivments_list[4][1]))
                self.achiv_info.ui.tableWidget.item(i, 5).setText(
                    str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year))

                item_list.append(item_text)


            else:
                print(" Noncheked")

        print(item_list)
        self.achiv_info.ui.pushButton_9.clicked.disconnect()

    # Добавление учеников карточками
    def update_uch(self, achivments_list):
        print(self.achiv_info.ui.lineEdit_2.text())

        users = db.reference('users').get()
        users_count = len(users)
        for i in range(users_count):
            users_list = users.get(list(users.keys())[i])
            if str(users_list.get("card_ID")) == self.achiv_info.ui.lineEdit_2.text():
                item_id = self.achiv_info.ui.tableWidget.item(i, 4)
                item_id.setCheckState(QtCore.Qt.CheckState.Checked)
                print(item_id.checkState())
                print("same")

        for i in range(self.achiv_info.ui.tableWidget.rowCount()):
            print(i)
            item_id = self.achiv_info.ui.tableWidget.item(i, 4)

            print(self.achiv_info.ui.tableWidget.item(i, 1).text())
            item_text = self.achiv_info.ui.tableWidget.item(i, 0).text()
            print(self.achiv_info.ui.tableWidget.item(i, 5).text())
            if item_id.checkState() == QtCore.Qt.Checked and self.achiv_info.ui.tableWidget.item(i, 5).text() == '':
                self.achiv_info.ui.tableWidget.item(i, 2).setText(str(achivments_list[4][1]))
                self.achiv_info.ui.tableWidget.item(i, 5).setText(
                    str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(
                        datetime.today().year))

        self.achiv_info.ui.lineEdit_2.clear()
        # self.achiv_info.ui.pushButton.clicked.disconnect()
        # self.achiv_info.ui.lineEdit_2.setEnabled(False)
        # self.achiv_info.ui.lineEdit_2.returnPressed.disconnect()

    # тоже добавление
    def add_user_in_achiv(self, achivments_list):
        self.achiv_info.ui.lineEdit_2.setEnabled(True)
        self.achiv_info.ui.lineEdit_2.setFocus()
        # self.achiv_info.ui.lineEdit_2.clear()
        print(self.achiv_info.ui.lineEdit_2.text())
        self.achiv_info.ui.lineEdit_2.returnPressed.connect(partial(self.update_uch, achivments_list))

        print("add")

    # открытие окна карточки ученика
    def open_uch_Window(self):
        row = self.ui.tableWidget_uch.currentIndex().row()
        column = self.ui.tableWidget_uch.currentIndex().column()
        print(row, column)

        users = db.collection('users').stream()

        user_table_ID = str(self.ui.tableWidget_uch.item(row, 0).text())
        print(user_table_ID)
        find_id = ''
        user_login = ''
        for user in users:
            if user.get('userId') == user_table_ID:
                user_login = user.get('login')
                self.uch_info.ui.groupBox.setTitle(user.get('name'))
                self.uch_info.ui.label_6.setText(str(user.get('allPoints')))
                self.uch_info.ui.label_17.setText(str(user.get('hours')))
                self.uch_info.ui.lineEdit_3.setText(str(user.get('password')))
                self.uch_info.ui.lineEdit_2.setText(str(user.get('login')))

                # find_id=db.reference('users').child(user_login).child("user_ID").get()
                '''
        #print('ID',user_table_ID,users.get(list(users.keys())[user_table_ID]).get('login'),find_id)
        users_list= db.reference('users').child(user_login).get()
    #   users_list = users.get(list(users.keys())[find_id])
        find_id=users_list.get('user_ID')
        #print('ученик1', users_list1)
        #print('ученик',find_id, users_list)
        achivments = db.reference('achivments').get()
        #print(achivments)
                '''

                achivments = db.collection('achivments').stream()
                # achivments_list = list(achivments[row].items())
                achiv_counter = 1
                for achiv in achivments:

                    self.uch_info.displayInfo()
                    rowPosition = self.uch_info.ui.tableWidget.rowCount()
                    # print(rowPosition)
                    if rowPosition < achiv_counter:
                        self.uch_info.ui.tableWidget.insertRow(rowPosition)
                    # achivments_list = achivments[i]
                    # print("achivments_list", ' ', achivments_list)
                    # добавление данных в ячейки
                    # ID
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 0, item)
                    self.uch_info.ui.tableWidget.item(achiv_counter - 1, 0).setText(str(achiv.get('achivID')))
                    # Название
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 1, item)
                    self.uch_info.ui.tableWidget.item(achiv_counter - 1, 1).setText(achiv.get('name'))
                    # Прогресс

                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEnabled)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 2, item)
                    if len(user.get('achivProgress').get(achiv.get('achivID'))) <= 7:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 2).setText(
                            str(user.get('achivProgress').get(achiv.get('achivID'))))
                    else:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 2).setText(str(achiv.get('pointsNeed')))
                    # награда
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 3, item)

                    if len(user.get('achivProgress').get(achiv.get('achivID'))) >= 8:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 3).setText(
                            str(user.get('achivProgress').get(achiv.get('achivID'))))
                    else:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 3).setText('0')
                    # достижение
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.CheckState.Checked)

                    if len(user.get('achivProgress').get(achiv.get('achivID'))) >= 8:
                        item.setCheckState(QtCore.Qt.CheckState.Checked)
                        self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 4, item)
                    else:
                        item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                        self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 4, item)
                    # дата

                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 5, item)
                    if len(user.get('achivProgress').get(achiv.get('achivID'))) >= 8:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 5).setText(
                            str(user.get('achivProgress').get(achiv.get('achivID'))))

                    achiv_counter += 1

                # rank

                for i in range(len(rank) - 1):
                    if user.get('allPoints') >= rank[i][1] and user.get('allPoints') < 1300 and user.get('allPoints') <= \
                            rank[i + 1][1]:
                        print("i", i)
                        self.uch_info.ui.label_8.setText(rank[i + 1][0])
                        self.uch_info.ui.label_13.setText(str(rank[i + 1][1] - user.get('allPoints')))
                        self.uch_info.ui.label_10.setText(str(rank[i][1]))
                        self.uch_info.ui.label_11.setText(str(rank[i + 1][1]))
                        self.uch_info.ui.progressBar.setValue(
                            int(100 - (rank[i + 1][1] - user.get('allPoints')) * 100 / (rank[i + 1][1] - rank[i][1])))
                        break
                self.uch_info.ui.pushButton_13.clicked.connect(self.toggle_password)
                self.uch_info.ui.lineEdit.setText(str(user.get('cardId')))
                self.uch_info.ui.pushButton.clicked.connect(partial(self.enable_card, user.get('login')))

                # image
                self.uch_info.ui.label.setMaximumSize(128, 128)
                image = QtGui.QImage()
                url_image = user.get("userImageUrl")
                if url_image == "None":
                    self.uch_info.ui.label.setPixmap(QtGui.QPixmap('logo.png'))
                else:
                    image.loadFromData(urlopen(url_image).read())
                    self.uch_info.ui.label.setPixmap(QtGui.QPixmap(image))

                # self.uch_info.ui.lineEdit.returnPressed.connect(partial(self.enable_card, users_list.get('login')))
                self.uch_info.ui.pushButton_2.clicked.connect(partial(self.delete_card, user.get('login')))
                self.uch_info.displayInfo()

    # добавление карты ученику
    def add_card_id(self, login):
        print('user', login)
        print(self.uch_info.ui.lineEdit.text())
        self.uch_info.ui.lineEdit.setEnabled(False)

        users = db.collection('users').where(u'login', u'==', login).stream()

        # users = db.reference('users')
        # users_ref = users.child(login)
        for user in users:
            db.collection('users').document(user.id).update({
                'cardId': int(self.uch_info.ui.lineEdit.text())
            })
            print(user.id)
        self.update_uch_data_from_db()
        # self.uch_info.ui.lineEdit.returnPressed.disconnect()

    # удаление карты
    def delete_card(self, login):
        print('login1', login)
        users = db.collection('users').where(u'login', u'==', login).stream()

        for user in users:
            db.collection('users').document(user.id).update({
                'cardId': "None"
            })
            print(user.id)
        self.uch_info.ui.lineEdit.setText("None")
        self.update_uch_data_from_db()

    # включение видимости карт
    def enable_card(self, login):
        print('users123', login)

        self.uch_info.ui.lineEdit.clear()
        self.uch_info.ui.lineEdit.setEnabled(True)
        self.uch_info.ui.lineEdit.setFocus()
        self.uch_info.ui.lineEdit.returnPressed.connect(partial(self.add_card_id, login))
        # self.uch_info.ui.pushButton.clicked.disconnect()

    # видимость пароля
    def toggle_password(self):
        if self.uch_info.ui.pushButton_13.text() == "Показать логин и пароль":

            self.uch_info.ui.lineEdit_2.setEchoMode(False)
            self.uch_info.ui.lineEdit_3.setEchoMode(False)
            self.uch_info.ui.lineEdit_2.setReadOnly(False)
            self.uch_info.ui.lineEdit_3.setReadOnly(False)
            self.uch_info.ui.pushButton_13.setText("Скрыть логин и пароль")
            self.uch_info.ui.lineEdit_2.setEnabled(True)
            self.uch_info.ui.lineEdit_3.setEnabled(True)
        else:
            self.uch_info.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.uch_info.ui.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
            self.uch_info.ui.lineEdit_2.setReadOnly(True)
            self.uch_info.ui.lineEdit_3.setReadOnly(True)

            self.uch_info.ui.pushButton_13.setText("Показать логин и пароль")
            self.uch_info.ui.lineEdit_2.setEnabled(False)
            self.uch_info.ui.lineEdit_3.setEnabled(False)

    # открытие
    def browseUch(self):
        print("clicked")
        self.w = uch_to_achiv()
        self.w.show()

    # удаление картинки
    def delete_image_2(self):
        print("clicked")
        # fname= QFileDialog.getOpenFileName(self,'open file','c\\', 'Image files (*.jpg *.png)')
        self.ui.label_achiv_image_2.setPixmap(QtGui.QPixmap('logo.png'))

    def delete_image_3(self):
        print("clicked")
        # fname = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'Image files (*.jpg *.png)')
        # imagePath = fname[0]
        self.ui.label_user_image_2.setPixmap(QtGui.QPixmap('logo.png'))

    # выбор картинки
    def browseImage_2(self):
        print("clicked")
        fname = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'Image files (*.jpg *.png)')
        global imagePath
        imagePath = fname[0]
        self.ui.label_achiv_image_2.setPixmap(QtGui.QPixmap(imagePath))

    def browseImage_3(self):
        print("clicked")
        fname = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'Image files (*.jpg *.png)')
        global user_imagePath
        user_imagePath = fname[0]
        self.ui.label_user_image_2.setPixmap(QtGui.QPixmap(user_imagePath))


    # поиск учеников
    def search_uch(self):

        if self.ui.lineEdit_uch_search.text() == "":
            for i in range(self.ui.tableWidget_uch.rowCount()):
                self.ui.tableWidget_uch.setRowHidden(i, False)
        else:
            # показ всех

            items_row = [itm.row() for itm in
                         self.ui.tableWidget_uch.findItems(self.ui.lineEdit_uch_search.text(), QtCore.Qt.MatchContains)]

            items1 = [itm.text() for itm in
                      self.ui.tableWidget_uch.findItems(self.ui.lineEdit_uch_search.text(), QtCore.Qt.MatchContains)]

            if len(items1) != 0:
                for i in range(self.ui.tableWidget_uch.rowCount()):
                    self.ui.tableWidget_uch.setRowHidden(i, False)

                # скрытие лишних
                for i in range(self.ui.tableWidget_uch.rowCount()):
                    if i != items_row[0]:
                        self.ui.tableWidget_uch.setRowHidden(i, True)

    # показ ачивок
    def show_achiv(self, final):
        print(1)
        print(final)
        if len(final) != 0:
            for i in range(self.ui.tableWidget_achiv.rowCount()):
                self.ui.tableWidget_achiv.setRowHidden(i, False)
            # скрытие лишних
            for i in range(self.ui.tableWidget_achiv.rowCount()):
                if i not in final:
                    self.ui.tableWidget_achiv.setRowHidden(i, True)

    # Поиск ачивок
    def search_achiv(self):
        # Поиск по всем признакам
        if self.ui.comboBox_type_search.currentText() != "Выбор типа..." and self.ui.lineEdit_achiv_search.text() != "" and self.ui.spinBox_reward_search.value() != 0:
            print("Поиск по всем признакам")
            # Тип
            # Тип
            items_type_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 3).text())
                if self.ui.tableWidget_achiv.item(i, 3).text().find(
                        str(self.ui.comboBox_type_search.currentText())) != -1:
                    items_type_row.append(i)
            # текст
            items_text_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 1).text())
                if self.ui.tableWidget_achiv.item(i, 1).text().find(str(self.ui.lineEdit_achiv_search.text())) != -1:
                    items_text_row.append(i)
            # баллы
            items_ball_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                if self.ui.tableWidget_achiv.item(i, 2).text() == str(self.ui.spinBox_reward_search.value()):
                    items_ball_row.append(i)
            items_final = []
            for i in range(100):
                if i in items_type_row and i in items_text_row and i in items_ball_row:
                    items_final.append(i)
            print("final", items_final)

            self.show_achiv(items_final)

        # Поиск по тексту и типу
        elif self.ui.comboBox_type_search.currentText() != "Выбор типа..." and self.ui.lineEdit_achiv_search.text() != "":
            print("Поиск по тексту и типу")
            print(self.ui.spinBox_reward_search.value())
            # Тип
            items_type_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 3).text())
                if self.ui.tableWidget_achiv.item(i, 3).text().find(
                        str(self.ui.comboBox_type_search.currentText())) != -1:
                    items_type_row.append(i)
            # текст
            items_text_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 1).text())
                if self.ui.tableWidget_achiv.item(i, 1).text().find(str(self.ui.lineEdit_achiv_search.text())) != -1:
                    items_text_row.append(i)

            items_final = []
            for i in range(100):
                if i in items_type_row and i in items_text_row:
                    items_final.append(i)
            print("final", items_final)
            self.show_achiv(items_final)
        # Поиск по тексту и баллам
        elif self.ui.lineEdit_achiv_search.text() != "" and self.ui.spinBox_reward_search.value() != 0:
            print("Поиск по тексту и баллам")
            # текст
            items_text_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 1).text())
                if self.ui.tableWidget_achiv.item(i, 1).text().find(str(self.ui.lineEdit_achiv_search.text())) != -1:
                    items_text_row.append(i)
            # баллы

            items_ball_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                if self.ui.tableWidget_achiv.item(i, 2).text() == str(self.ui.spinBox_reward_search.value()):
                    items_ball_row.append(i)

            print(items_ball_row)
            items_final = []
            for i in range(100):
                if i in items_text_row and i in items_ball_row:
                    items_final.append(i)
            print("final", items_final)

            self.show_achiv(items_final)
        # Поиск по типу и баллам
        elif self.ui.comboBox_type_search.currentText() != "Выбор типа..." and self.ui.spinBox_reward_search.value() != 0:
            print("Поиск по типу и баллам")
            # Тип
            items_type_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 3).text())
                if self.ui.tableWidget_achiv.item(i, 3).text().find(
                        str(self.ui.comboBox_type_search.currentText())) != -1:
                    items_type_row.append(i)

            # баллы

            items_ball_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                if self.ui.tableWidget_achiv.item(i, 2).text() == str(self.ui.spinBox_reward_search.value()):
                    items_ball_row.append(i)

            items_final = []
            for i in range(100):
                if i in items_type_row and i in items_ball_row:
                    items_final.append(i)
            print("final", items_final)

            self.show_achiv(items_final)
        # поиск по типу
        elif self.ui.comboBox_type_search.currentText() != "Выбор типа...":
            print("Поиск по типу")
            # Тип
            items_type_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 3).text())
                if self.ui.tableWidget_achiv.item(i, 3).text().find(
                        str(self.ui.comboBox_type_search.currentText())) != -1:
                    items_type_row.append(i)
            print(items_type_row)
            self.show_achiv(items_type_row)
        # Поиск тексту
        elif self.ui.lineEdit_achiv_search.text() != "":
            print("Поиск по тексту")

            # текст
            items_text_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                print(self.ui.tableWidget_achiv.item(i, 1).text())
                if self.ui.tableWidget_achiv.item(i, 1).text().find(str(self.ui.lineEdit_achiv_search.text())) != -1:
                    items_text_row.append(i)
            print(items_text_row)
            self.show_achiv(items_text_row)
        # Поиск по награде
        elif self.ui.spinBox_reward_search.value() != 0:
            print("Поиск по награде")
            items_ball_row = []
            rows = self.ui.tableWidget_achiv.rowCount()
            for i in range(rows):
                if self.ui.tableWidget_achiv.item(i, 2).text() == str(self.ui.spinBox_reward_search.value()):
                    items_ball_row.append(i)
            self.show_achiv(items_ball_row)
        # Показ всех
        else:
            for i in range(self.ui.tableWidget_achiv.rowCount()):
                self.ui.tableWidget_achiv.setRowHidden(i, False)

    # получение сообщения
    @QtCore.pyqtSlot(list)
    def update_messages(self, message_a):
        print("update_messages")
        # само сообщение
        print(message_a)

        self.message_a = message_a
        # Изменение количества строк
        lenght = self.ui.tableWidget_uch_in_achiv.rowCount()

        print(lenght)
        self.ui.tableWidget_uch_in_achiv.setRowCount(len(message_a))
        lenght = self.ui.tableWidget_uch_in_achiv.rowCount()

        print(lenght)

        users = db.reference('users').get()
        users_count = len(users)

        find_id = ''
        user_name = ''
        # Изменение текста в итеме
        for i in range(lenght):
            print("i=", i)
            print(message_a[i])
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch_in_achiv.setItem(i, 1, item)
            self.ui.tableWidget_uch_in_achiv.item(i, 1).setText(message_a[i])

            for j in range(users_count):
                if db.reference('users').child(users.get(list(users.keys())[j]).get('login')).child(
                        "name").get() == (message_a[i]):
                    find_id = db.reference('users').child(users.get(list(users.keys())[j]).get('login')).child(
                        "user_ID").get()
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch_in_achiv.setItem(i, 0, item)
            self.ui.tableWidget_uch_in_achiv.item(i, 0).setText(str(find_id))
            item = QtWidgets.QTableWidgetItem()
            # item.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled)
            self.ui.tableWidget_uch_in_achiv.setItem(i, 2, item)
            self.ui.tableWidget_uch_in_achiv.item(i, 2).setText('0')
        self.ui.tableWidget_uch_in_achiv.sortItems(0)
        # print('ID',user_table_ID,users.get(list(users.keys())[user_table_ID]).get('login'),find_id)

    def edit_messages(self):
        self.dialog = uch_to_achiv()
        # Отправка из основы во второе окно
        # self.dialog.set_messages(self.ui.tableWidget_2.item(0,0).text() )
        # получение из 2 в основу
        self.dialog.submitted.connect(self.update_messages)
        self.dialog.show()


# окно логина
class Login(QtWidgets.QMainWindow):
    # вход в систему
    def pass_reg(self):

        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()

        # проверка пароля
        if login == "admin" and password == "admin":
            # запуск основы
            print(1)
            self.show_new_window()
            # self.window = QtWidgets.QMainWindow()
            # self.ui = Ui_MainWindow()
            # self.ui.setup(self.window)

            # закрытие логина
            # self.window.show()
            # self.close()

        else:
            # ошибка
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неверный логин или пароль')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    # открытие мейна
    def show_new_window(self):
        self.close()
        self.w = main_window()
        self.w.show()

    def __init__(self):
        # инициализация логина
        print(5)
        super().__init__()

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.pushButton.clicked.connect(self.pass_reg)


def main():
    #print(QtWidgets.QStyleFactory.keys())
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle(QStyleFactory.create('Fusion'))
    application = main_window()
    application.show()

    sys.exit(app.exec())
    # main1()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


class Login(QtWidgets.QMainWindow):
    # вход в систему
    def pass_reg(self):

        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()

        # проверка пароля
        if login == "admin" and password == "admin":
            # запуск основы
            print(1)
            self.show_new_window()
            # self.window = QtWidgets.QMainWindow()
            # self.ui = Ui_MainWindow()
            # self.ui.setup(self.window)

            # закрытие логина
            # self.window.show()
            # self.close()

        else:
            # ошибка
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неверный логин или пароль')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    # открытие мейна
    '''
    def show_new_window(self):
        self.close()
        self.w = main_window()
        self.w.show()

'''

    def __init__(self):
        # инициализация логина
        super().__init__()

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.pushButton.clicked.connect(self.pass_reg)

'''
def main():
    app = QtWidgets.QApplication(sys.argv)

    application = main_window()
    application.show()

    sys.exit(app.exec())
    # main1()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем

    main()  # то запускаем функцию main()
'''