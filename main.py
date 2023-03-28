import sys  # sys нужен для передачи argv в QApplication
import os
import time
import httplib2

from urllib.request import urlopen
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QStyleFactory,QTableView
from PyQt5.QtGui import QMovie

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
#from firebase_admin import batch

import qrcode

import psutil
import threading
count=0
for proc in psutil.process_iter():
    name = proc.name()

    if name == "cubic.exe":
        count+=1
    if count>1:
        exit()
print("programm start")
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
        users = db.collection('users').stream()

        user_number = 1
        # print(users)
        for user in users:
            rowPosition = self.ui.tableWidget.rowCount()

            if rowPosition < user_number:
                self.ui.tableWidget.insertRow(rowPosition)

            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(user_number-1, 1, item)
            self.ui.tableWidget.item(user_number-1, 1).setText(str(user.get('userId')))
            # Фио
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(user_number-1, 0, item)
            self.ui.tableWidget.item(user_number-1, 0).setText(user.get('name'))
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget.setItem(user_number-1, 2, item)
            user_number+=1

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
            self.ui.pushButton_13.clicked.disconnect()
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
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self.ui = Ui_lessons()
        self.ui.setupUi(self)
        self.ui.label_3.hide()
    def closeEvent(self, a0: QtGui.QCloseEvent) :
        print("closed")
        #main_window() #todo добиться человеческого вызова при закрытии
        try:
            self.ui.lineEdit.returnPressed.disconnect()
        except Exception:
            pass
        try:
            main_window.ui.pushButton_lesson.clicked.disconnect()
        except Exception:
            pass
        try:
            main_window.ui.pushButton_intensiv.clicked.disconnect()
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
        print('main window ini')
        super(main_window, self).__init__(parent)
        self.achiv_info = achiv_info()
        self.uch_info = uch_info()
        self.add_lessons = add_lessons()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.get_data_from_db()

        self.add_lessons.ui.pushButton.clicked.connect(self.add_lessons_close)

        self.ui.pushButton_add_uch_to_achiv.clicked.connect(self.edit_messages)

        self.ui.pushButton_select_image_2.clicked.connect(self.browseImage_2)
        self.ui.pushButton_delete_image.clicked.connect(self.delete_image_2)

        self.ui.pushButton_select_image_3.clicked.connect(self.browseImage_3)
        self.ui.pushButton_delete_image_2.clicked.connect(self.delete_image_3)

        self.ui.pushButton.clicked.connect(self.browseImage_4)
        self.ui.pushButton_2.clicked.connect(self.delete_image_4)
        # поиск
        self.ui.pushButton_uch_search.clicked.connect(self.search_uch)
        self.ui.pushButton_achiv_search.clicked.connect(self.search_achiv)
        self.achiv_info.ui.pushButton_11.clicked.connect(self.search_uch_in_achiv)

        # открытие информации
        self.ui.tableWidget_achiv.cellDoubleClicked.connect(self.open_achiv_Window)
        self.ui.tableWidget_uch.cellDoubleClicked.connect(self.open_uch_Window)
        # новый пользователь
        self.ui.pushButton_password_generation.clicked.connect(self.generate_password)
        self.ui.pushButton_add_new_uch.clicked.connect(self.add_new_uch)
        # новое достижение
        self.ui.pushButton_add_achive_2.clicked.connect(self.add_new_achiv)

        # мероприятия
        self.ui.pushButton_3.clicked.connect(self.save_event)
        #добавление новой активности
        self.ui.pushButton_5.clicked.connect(self.add_new_activ)

        self.ui.tableWidget_2.itemChanged.connect(self.count_check)

    def count_check(self, item):
        if item.checkState() == 2:
            for i in range(self.ui.tableWidget_2.rowCount()):
                if self.ui.tableWidget_2.item(i, 2) != item:
                    self.ui.tableWidget_2.item(i, 2).setCheckState(QtCore.Qt.Unchecked)
    def lesson_new(self):


        self.add_lessons.ui.lineEdit.clear()
        # self.add_lessons.setWindowTitle(self.sender().text())
        self.add_lessons.ui.lineEdit.setFocus()
        qr_word = ''
        for x in range(20):  # Количество символов (16)
            qr_word = qr_word + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен qr-слово
        print("qr",qr_word)
        img = qrcode.make(qr_word)
        img.save("qr_code.png")
        db.collection('visits').document('qrCodes').update({
            'cabinet1': qr_word
        })
        self.add_lessons.ui.label.setPixmap(QtGui.QPixmap("qr_code.png"))
        self.add_lessons.ui.lineEdit.returnPressed.connect(partial(self.add_point_new,self.sender().text()))
        self.add_lessons.displayInfo()

    def add_point_new(self,activ_name): #todo оптимизировать
        counters= db.collection('counters').where('activ_name','==',activ_name).stream()
        self.add_lessons.ui.label_3.show()
        QtCore.QCoreApplication.processEvents()
        start = datetime.now()
        users = db.collection('users').where(u'cardId', u'==', self.add_lessons.ui.lineEdit.text()).stream()


        user_flag=0
        for user in users:
            user_flag=1
            for count in counters:
                print(datetime.now() - start)
                count_doc_id=count.id
                added_point=count.get('activ_point')
                user_id=user.get('userId')

                user_doc_id=user.id
                user_count=count.get('users').get(user.get('userId'))
        if user_flag==0:
            self.add_lessons.ui.label_3.hide()
            self.add_lessons.ui.lineEdit.clear()
            return
        print('clear', datetime.now() - start)

        #Проверка достижений

        achivments = db.collection('achivments').where('pointsNeed', '==', user_count + 1).stream()

        # пакетная запись
        batch = db.batch()
        for achiv in achivments:
            print('achiv search')
            achiv_point = achiv.get('point')
            added_point+=achiv_point
            achiv_id = achiv.get('achivID')
            #обновляем достижение у юзера
            batch.update(db.collection('users').document(user_doc_id), {
                'achivProgress.' + achiv_id: str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(
                    datetime.today().year)
            })


        #ученику очки
        batch.update(db.collection('users').document(user_doc_id), {
            'allPoints': user.get('allPoints') + added_point,
            'points': user.get('points') + added_point,
            'hours': user.get('hours')+1
        })
        #счетчик увеличиваем
        batch.update(db.collection('counters').document(count_doc_id), {
            'users.' + str(user_id): user_count + 1
        })

        batch.commit()
        print('clear1', datetime.now() - start)



        self.add_lessons.ui.label_3.hide()
        self.add_lessons.ui.lineEdit.clear()

    #добавление новой активности
    def add_new_activ(self):
        users_data = {

        }
        users = db.collection('users').stream()
        for user in users:
            users_data.update({user.get('userId'): 0})

        data={
            'activ_name':self.ui.lineEdit_3.text() ,
            'activ_point': self.ui.spinBox.value(),
            'users': users_data
        }
        counter = db.collection('counters').add(data)
        self.update_counters()

    #обновление активностей
    def update_counters(self):
        print('update_counters')
        counter = db.collection('counters').stream()
        count_counter=1
        for count in counter:
            rowPosition = self.ui.tableWidget.rowCount()
            if rowPosition < count_counter:
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget_2.insertRow(rowPosition)

                self.ui.pushButton_activ = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_2)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.pushButton_activ.sizePolicy().hasHeightForWidth())
                self.ui.pushButton_activ.setSizePolicy(sizePolicy)
                self.ui.pushButton_activ.setMinimumSize(QtCore.QSize(100, 100))
                self.ui.pushButton_activ.setObjectName("pushButton_activ")  # +str(count_counter-1))
                self.ui.pushButton_activ.setText(str(count.get('activ_name')))

                if self.ui.gridLayout_12.count() % 3 == 0:
                    self.ui.gridLayout_12.addWidget(self.ui.pushButton_activ, self.ui.gridLayout_12.rowCount(),
                                                    0, 1, 1)
                else:
                    self.ui.gridLayout_12.addWidget(self.ui.pushButton_activ, self.ui.gridLayout_12.rowCount() - 1,
                                                    self.ui.gridLayout_12.count() % 3, 1, 1)

            item = QtWidgets.QTableWidgetItem(str(count.get('activ_name')))
            item.setFlags(QtCore.Qt.ItemIsDragEnabled  | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(count_counter-1, 0, item)

            item = QtWidgets.QTableWidgetItem(str(count.get('activ_name')))
            item.setFlags(QtCore.Qt.ItemIsDragEnabled  | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_2.setItem(count_counter-1, 0, item)
            #выбран
            item = QtWidgets.QTableWidgetItem(str(count.get('activ_point')))
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            item.setFlags(QtCore.Qt.ItemIsSelectable  | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(count_counter-1, 1, item)

            item = QtWidgets.QTableWidgetItem(str(count.get('activ_point')))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_2.setItem(count_counter - 1, 1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget_2.setItem(count_counter - 1, 2, item)

            count_counter+=1

            self.ui.pushButton_activ.clicked.connect(self.lesson_new)

    #добавление ивента в БД
    def save_event(self):


        events=db.collection('events')

        id = ''
        for x in range(16):  # Количество символов (16)
            id = id + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))

        image_url = 'None'
        if imagePath != '':
            blob = bucket.blob("Events/event_" + id + ".png")
            blob.upload_from_filename(imagePath)
            blob.make_public()
            image_url = blob.public_url

        images=[image_url]
        data={
            'date':self.ui.calendarWidget.selectedDate().toString('dd.MM.yyyy'),
            'description':self.ui.textEdit.toPlainText(),
            'name': self.ui.lineEdit.text(),
            'eventId':'event-by-'+id,
            'images':images
        }
        events.add(data)

        #clean
        #self.ui.calendarWidget.clear()
        print('saved event')
        self.update_event_data_from_db(data)
        self.ui.textEdit.clear()
        self.ui.lineEdit.clear()

    #закрытие уроков и обновление бд
    def add_lessons_close(self):
        start=datetime.now()

        self.update_uch_data_from_db()
        self.update_achiv_data_from_db()
        print('update after close lessons', datetime.now() - start)
        os.remove('qr_code.png')
        self.add_lessons.close()
    #Функция для одноразового запуска другой функции
    def run_once(self,f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    # добавление нового достижения
    def add_new_achiv(self):

        name = self.ui.lineEdit_achiv_name_2.text()

        type = self.ui.comboBox_achiv_type.currentText()
        points_need = self.ui.spinBox_reward_search_3.value()
        image_url = 'None'
        achiv_counter=None


        point = 0
        achiv_id = ''
        for x in range(16):  # Количество символов (16)
            achiv_id = achiv_id + random.choice(list(
                '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен пароль
        if imagePath != '':
            blob = bucket.blob("Achivments/achivments_" + achiv_id + ".png")
            blob.upload_from_filename(imagePath)
            blob.make_public()
            image_url = blob.public_url

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
            point = int(self.ui.spinBox_reward_search_2.value())
        if self.ui.checkBox.isEnabled():
            for i in range(self.ui.tableWidget_2.rowCount()):
                if self.ui.tableWidget_2.item(i, 2).checkState()==2:
                    activ_name=self.ui.tableWidget_2.item(i, 0).text()
                    self.ui.tableWidget_2.item(i, 2).setCheckState(QtCore.Qt.Unchecked)
            for counter in db.collection('counters').where('activ_name','==',activ_name).stream():
                achiv_counter=counter.id
        achivment_data = {
            'achivID': achiv_id,
            'achivImageURL': image_url,
            'name': name,
            'counter':achiv_counter,
            'point': point,
            'pointsNeed': points_need,
            'type': type
        }

        db.collection('achivments').add(achivment_data)
        users = db.collection('users').stream()
        for user in users:
            db.collection('users').document(user.id).set({
                'achivProgress':{
                    achiv_id:"0"
                }
         }, merge=True)
        #clear
        self.ui.lineEdit_achiv_name_2.setText('')
        self.ui.checkBox.setCheckState(QtCore.Qt.Unchecked)
        self.ui.checkBox_achiv_type_2.setCheckState(QtCore.Qt.Unchecked)
        self.ui.spinBox_reward_search_3.setValue(0)
        self.ui.spinBox_reward_search_2.setValue(0)
        self.delete_image_2()

        self.update_uch_data_from_db()
        self.update_achiv_data_from_db()

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

        # Добавление в счетчики
        counters= db.collection("counters").stream()

        for count in counters:
            db.collection("counters").document(count.id).set(
                {
                    "users":{
                        user_id:0
                    }

                }, merge=True
            )

        #print('imagePath', user_imagePath, type(user_imagePath))
        # print(storage.child("users_image/logo.png").get_url(user['idToken']))
        if user_imagePath != '':
            print("put in db")
            blob = bucket.blob("UserImages/user_" + user_id + ".png")
            blob.upload_from_filename(user_imagePath)
            blob.make_public()
            image_url = blob.public_url

        user_data = {
            'achivProgress': achiv_progress,
            "cart": [],
            "likes": [],
            "orders": [],
            "allPoints": 0,
            "cardId": 'None',
            "hours": 0,
            "email": login + "@cubs.com" ,
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
        self.update_uch_data_from_db()
        self.update_achiv_data_from_db()

        # storage.child("users_image/logo.png").put(imagePath)   #put('logo1.png')
    #обновление учеников и достижений
    def update_uch_data_from_db(self):
        print("update from db")
        start=datetime.now()
        users = db.collection('users').stream()

        user_number = 1

        # Добавление учеников в список
        for user in users:
            lenght = self.ui.tableWidget_uch.rowCount()
            # print(lenght)
            rowPosition = user_number#self.ui.tableWidget_uch.rowCount()
            rowPosition = user_number#self.ui.tableWidget_uch.rowCount()
            # print(rowPosition)
            if rowPosition < user_number:
                self.ui.tableWidget_uch.insertRow(rowPosition)

            #print(user_number,rowPosition,self.ui.tableWidget_uch.rowCount())
            # добавление данных в ячейки
            # ID
            item = QtWidgets.QTableWidgetItem(user.get('userId'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 0, item)
            # Фио
            item = QtWidgets.QTableWidgetItem(user.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 1, item)

            # кубиков всего
            item = QtWidgets.QTableWidgetItem(str(user.get('allPoints')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 2, item)

            # кубикорубли
            item = QtWidgets.QTableWidgetItem(str(user.get('points')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 3, item)
            # достижений

            achiv_counter = 0
            for achiv in user.get('achivProgress'):
                # print('achiv_count',achiv_count)
                if len(achiv) >= 7:
                    achiv_counter += 1
            item = QtWidgets.QTableWidgetItem(str(achiv_counter))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 4, item)

            # часов всего
            item = QtWidgets.QTableWidgetItem(str(user.get('hours')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 5, item)

            # cardID
            item = QtWidgets.QTableWidgetItem(str(user.get('cardId')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 6, item)

            #self.ui.tableWidget_leaderboard.insertRow(user_number - 1)
            #leaderboard
            item = QtWidgets.QTableWidgetItem(str(user.get('userId')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)

            # Фио
            item = QtWidgets.QTableWidgetItem(user.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)

            # кубиков всего
            item = QtWidgets.QTableWidgetItem(str(user.get('allPoints')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 1, item)

            user_number += 1
        print(datetime.now() - start)


    def update_achiv_data_from_db(self):
        start = datetime.now()
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
            item = QtWidgets.QTableWidgetItem(str(achivment.get('achivID')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 0, item)
            # self.ui.tableWidget_achiv.item(achiv_number - 1, 0).setText(str(achivment.get('achivID')))
            # название
            item = QtWidgets.QTableWidgetItem(achivment.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 1, item)
            # self.ui.tableWidget_achiv.item(achiv_number - 1, 1).setText(achivment.get('name'))
            # награда
            item = QtWidgets.QTableWidgetItem(str(achivment.get('point')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 2, item)
            # self.ui.tableWidget_achiv.item(achiv_number - 1, 2).setText(str(achivment.get('point')))
            # тип
            item = QtWidgets.QTableWidgetItem(achivment.get('type'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 3, item)
            # self.ui.tableWidget_achiv.item(achiv_number - 1, 3).setText(achivment.get('type'))

            achiv_number += 1
        print('update_achiv',datetime.now() - start)
    #обновление мероприятий
    def update_event_data_from_db(self,data):

        print("event update",data)
        self.ui.groupBox = QtWidgets.QGroupBox(self.ui.scrollAreaWidgetContents)
        # политика изменения размера
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.groupBox.sizePolicy().hasHeightForWidth())
        self.ui.groupBox.setSizePolicy(sizePolicy)
        self.ui.groupBox.setMinimumSize(QtCore.QSize(210, 400))
        self.ui.groupBox.setSizeIncrement(QtCore.QSize(0, 0))

        self.ui.groupBox.setObjectName("groupBox")
        self.ui.groupBox.setTitle(data.get('name'))
        self.ui.gridLayout_9 = QtWidgets.QGridLayout(self.ui.groupBox)

        self.ui.label_8 = QtWidgets.QLabel(self.ui.groupBox)
        # политика изменения размера
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.label_8.sizePolicy().hasHeightForWidth())
        self.ui.label_8.setSizePolicy(sizePolicy)
        self.ui.label_8.setBaseSize(QtCore.QSize(0, 0))
        self.ui.label_8.setTextFormat(QtCore.Qt.AutoText)
        self.ui.label_8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.label_8.setObjectName("label_8")
        self.ui.label_8.setWordWrap(True)
        self.ui.label_8.setText("Описание:\n" + data.get('description'))
        self.ui.gridLayout_9.addWidget(self.ui.label_8, 2, 0, 1, 1)

        self.ui.widget_4 = QtWidgets.QWidget(self.ui.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.widget_4.sizePolicy().hasHeightForWidth())
        self.ui.widget_4.setSizePolicy(sizePolicy)
        self.ui.widget_4.setObjectName("widget_4")
        self.ui.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ui.widget_4)
        self.ui.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ui.label_7 = QtWidgets.QLabel(self.ui.widget_4)

        # политика изменения размера
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.label_7.sizePolicy().hasHeightForWidth())
        self.ui.label_7.setSizePolicy(sizePolicy)
        # self.ui.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.ui.label_7.setMinimumSize(200, 200)
        self.ui.label_7.setMaximumSize(QtCore.QSize(16777215, 200))
        self.ui.label_7.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.label_7.setText("")

        # изображение

        start = datetime.now()
        image = QtGui.QPixmap('logo1.png')
        url_image = data.get("images")[0]

        # response, content = h.request(url_image,"GET")
        # load_image=h.cache.get("content")
        # image.loadFromData(content)
        p = QtGui.QPixmap('logo1.png')



        # ширина высота
        self.ui.label_7.setPixmap(p.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                           QtCore.Qt.TransformationMode.SmoothTransformation))
        print(count, datetime.now() - start)

        # self.ui.label_7.setScaledContents(True)
        self.ui.label_7.setObjectName("label_7")
        self.ui.gridLayout_9.addWidget(self.ui.widget_4, 0, 0, 1, 1)

        self.ui.label_6 = QtWidgets.QLabel(self.ui.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.label_6.sizePolicy().hasHeightForWidth())
        self.ui.label_6.setSizePolicy(sizePolicy)
        self.ui.label_6.setObjectName("label_6")
        self.ui.label_6.setText("Дата: " + data.get('date'))
        self.ui.gridLayout_9.addWidget(self.ui.label_6, 1, 0, 1, 1)

        if self.ui.gridLayout_8.count() % 3 == 0:
            self.ui.gridLayout_8.addWidget(self.ui.groupBox, self.ui.gridLayout_8.rowCount(),
                                           0, 1, 1)
        else:
            self.ui.gridLayout_8.addWidget(self.ui.groupBox, self.ui.gridLayout_8.rowCount() - 1,
                                           self.ui.gridLayout_8.count() % 3, 1, 1)
        self.load(self.ui.label_7, url_image)
    # данные из бд
    #@run_once
    def get_data_from_db(self):

        start = datetime.now()

        print("get from db")

        users = db.collection('users').stream()
        user_number = 1
        # print(users)
        for user in users:

            # Добавление учеников в список
            self.ui.tableWidget_uch.insertRow(user_number-1)

            # добавление данных в ячейки
            # ID

            item = QtWidgets.QTableWidgetItem(user.get('userId'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 0, item)
            # Фио
            item = QtWidgets.QTableWidgetItem(user.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 1, item)

            # кубиков всего
            item = QtWidgets.QTableWidgetItem(str(user.get('allPoints')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 2, item)

            # кубикорубли
            item = QtWidgets.QTableWidgetItem(str(user.get('points')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 3, item)

            # достижений
            achiv_counter = 0
            for achiv_count in user.get('achivProgress').values():
                if len(achiv_count) >= 6:
                    achiv_counter += 1
            item = QtWidgets.QTableWidgetItem(str(achiv_counter))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 4, item)



            # часов всего
            item = QtWidgets.QTableWidgetItem(str(user.get('hours')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 5, item)

            #cardID
            item = QtWidgets.QTableWidgetItem(str(user.get('cardId')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch.setItem(user_number - 1, 6, item)


            self.ui.tableWidget_leaderboard.insertRow(user_number-1)
            # таблица лидеров
            # ID
            item = QtWidgets.QTableWidgetItem(str(user.get('userId')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)

            # Фио
            item = QtWidgets.QTableWidgetItem(user.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 0, item)

            # кубиков всего
            item = QtWidgets.QTableWidgetItem(str(user.get('allPoints')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_leaderboard.setItem(user_number - 1, 1, item)

            user_number += 1
        print(datetime.now() - start)
        start = datetime.now()
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
            item = QtWidgets.QTableWidgetItem(str(achivment.get('achivID')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 0, item)
            #self.ui.tableWidget_achiv.item(achiv_number - 1, 0).setText(str(achivment.get('achivID')))
            # название
            item = QtWidgets.QTableWidgetItem(achivment.get('name'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 1, item)
            #self.ui.tableWidget_achiv.item(achiv_number - 1, 1).setText(achivment.get('name'))
            # награда
            item = QtWidgets.QTableWidgetItem(str(achivment.get('point')))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 2, item)
            #self.ui.tableWidget_achiv.item(achiv_number - 1, 2).setText(str(achivment.get('point')))
            # тип
            item = QtWidgets.QTableWidgetItem(achivment.get('type'))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_achiv.setItem(achiv_number - 1, 3, item)
            #self.ui.tableWidget_achiv.item(achiv_number - 1, 3).setText(achivment.get('type'))


            achiv_number += 1
        print(datetime.now() - start)
        #Меропрития
        events=db.collection('events').stream()
        count=1


        threads = []
        h = httplib2.Http('.cache')
        for event in events:


            self.ui.groupBox = QtWidgets.QGroupBox(self.ui.scrollAreaWidgetContents)
            # политика изменения размера
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.groupBox.sizePolicy().hasHeightForWidth())
            self.ui.groupBox.setSizePolicy(sizePolicy)
            self.ui.groupBox.setMinimumSize(QtCore.QSize(210, 400))
            self.ui.groupBox.setSizeIncrement(QtCore.QSize(0, 0))

            self.ui.groupBox.setObjectName("groupBox")
            self.ui.groupBox.setTitle(event.get('name'))
            self.ui.gridLayout_9 = QtWidgets.QGridLayout(self.ui.groupBox)

            self.ui.label_8 = QtWidgets.QLabel(self.ui.groupBox)
            # политика изменения размера
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.label_8.sizePolicy().hasHeightForWidth())
            self.ui.label_8.setSizePolicy(sizePolicy)
            self.ui.label_8.setBaseSize(QtCore.QSize(0, 0))
            self.ui.label_8.setTextFormat(QtCore.Qt.AutoText)
            self.ui.label_8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.ui.label_8.setObjectName("label_8")
            self.ui.label_8.setWordWrap(True)
            self.ui.label_8.setText("Описание:\n"+ event.get('description'))
            self.ui.gridLayout_9.addWidget(self.ui.label_8, 2, 0, 1, 1)

            self.ui.widget_4 = QtWidgets.QWidget(self.ui.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.widget_4.sizePolicy().hasHeightForWidth())
            self.ui.widget_4.setSizePolicy(sizePolicy)
            self.ui.widget_4.setObjectName("widget_4")
            self.ui.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ui.widget_4)
            self.ui.verticalLayout_4.setObjectName("verticalLayout_4")
            self.ui.label_7 = QtWidgets.QLabel(self.ui.widget_4)



            # политика изменения размера
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.label_7.sizePolicy().hasHeightForWidth())
            self.ui.label_7.setSizePolicy(sizePolicy)
            #self.ui.label_7.setFrameShape(QtWidgets.QFrame.Box)
            self.ui.label_7.setMinimumSize(200, 200)
            self.ui.label_7.setMaximumSize(QtCore.QSize(16777215, 200))
            self.ui.label_7.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.ui.label_7.setText("")

            #изображение

            start = datetime.now()
            image = QtGui.QPixmap('logo1.png.png')
            url_image = event.get("images")[0]

            #response, content = h.request(url_image,"GET")
            #load_image=h.cache.get("content")
            #image.loadFromData(content)
            p=QtGui.QPixmap('logo.png')


                                            #ширина высота
            self.ui.label_7.setPixmap(p.scaled(200,200,QtCore.Qt.AspectRatioMode.KeepAspectRatio,QtCore.Qt.TransformationMode.SmoothTransformation))
            print(count, datetime.now() - start)


            #self.ui.label_7.setScaledContents(True)
            self.ui.label_7.setObjectName("label_7")
            self.ui.gridLayout_9.addWidget(self.ui.widget_4, 0, 0, 1, 1)


            self.ui.label_6 = QtWidgets.QLabel(self.ui.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.label_6.sizePolicy().hasHeightForWidth())
            self.ui.label_6.setSizePolicy(sizePolicy)
            self.ui.label_6.setObjectName("label_6")
            self.ui.label_6.setText("Дата: "+ event.get('date'))
            self.ui.gridLayout_9.addWidget(self.ui.label_6, 1, 0, 1, 1)


            count+=1
            threads.append(threading.Thread(target=self.load, args=(self.ui.label_7, url_image)))
            if self.ui.gridLayout_8.count() % 3 == 0:
                self.ui.gridLayout_8.addWidget(self.ui.groupBox, self.ui.gridLayout_8.rowCount(),
                                               0, 1, 1)
            else:
                self.ui.gridLayout_8.addWidget(self.ui.groupBox, self.ui.gridLayout_8.rowCount() - 1,
                                               self.ui.gridLayout_8.count() % 3, 1, 1)

        for thread in threads:
            thread.start()  # каждый поток должен быть запущен
        for thread in threads:
            thread.join()
        #счетчики
        counter = db.collection('counters').stream()
        count_counter = 1
        for count in counter:
            rowPosition = self.ui.tableWidget.rowCount()
            # print(rowPosition)
            if rowPosition < count_counter:
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget_2.insertRow(rowPosition)
            item = QtWidgets.QTableWidgetItem(str(count.get('activ_name')))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(count_counter - 1, 0, item)

            item = QtWidgets.QTableWidgetItem(str(count.get('activ_name')))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_2.setItem(count_counter - 1, 0, item)

            # выбран
            item = QtWidgets.QTableWidgetItem(str(count.get('activ_point')))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget.setItem(count_counter - 1, 1, item)

            item = QtWidgets.QTableWidgetItem(str(count.get('activ_point')))
            item.setFlags(QtCore.Qt.ItemIsSelectable  | QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_2.setItem(count_counter - 1, 1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget_2.setItem(count_counter - 1, 2, item)


            count_counter += 1

            self.ui.pushButton_activ = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_2)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.pushButton_activ.sizePolicy().hasHeightForWidth())
            self.ui.pushButton_activ.setSizePolicy(sizePolicy)
            self.ui.pushButton_activ.setMinimumSize(QtCore.QSize(100, 100))
            self.ui.pushButton_activ.setObjectName("pushButton_activ")#+str(count_counter-1))
            self.ui.pushButton_activ.setText(str(count.get('activ_name')))
            if self.ui.gridLayout_12.count() % 3 == 0:
                self.ui.gridLayout_12.addWidget(self.ui.pushButton_activ, self.ui.gridLayout_12.rowCount(),
                                               0, 1, 1)
            else:
                self.ui.gridLayout_12.addWidget(self.ui.pushButton_activ, self.ui.gridLayout_12.rowCount() - 1,
                                               self.ui.gridLayout_12.count() % 3, 1, 1)
            self.ui.pushButton_activ.clicked.connect(self.lesson_new)



        print(datetime.now() - start)

    #print(self.ui.gridLayout_8.count())

    # поменял функцию ресайза на свою
    # Мультипоточная загрузка картинок
    def load(self, Label_obj, url_image):
        # print("loaded",Label_obj,url_image)
        image = QtGui.QPixmap()
        h = httplib2.Http('.cache')
        response, content = h.request(url_image, "GET")
        load_image = h.cache.get("content")
        image.loadFromData(content)
        p = QtGui.QPixmap(image)
        w=p.width()
        h=p.height()

        if w>h:

            cropped= p.copy( w//2-h//2,0,w,h )

        else:
            cropped = p.copy(0, h // 2 - w // 2, w, h)

        Label_obj.setPixmap(cropped.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                         QtCore.Qt.TransformationMode.SmoothTransformation))


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

        counter =db.collection('counters').document(achiv_info.get('counter')).get().get('users')
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
                self.achiv_info.ui.tableWidget.item(user_number - 1, 2).setText(str(counter.get(user.get('userId'))))


            #print(user.get('userId'),counter.get(user.get('userId')))

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

        counter = 0
        users_count = 0
        users = db.collection('users').stream()
        for user in users:
            users_count += 1

            if len(user.get('achivProgress').get(achiv_info.get('achivID'))) >= 8:
                counter += 1
        self.achiv_info.ui.groupBox_4.setTitle(achiv_info.get('name'))
        self.achiv_info.ui.label_31.setText(str(achiv_counter))
        self.achiv_info.ui.progressBar_3.setValue(round(counter / users_count * 100))
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
    def update_uch(self, achivments_list): #todo не пашет, изменить
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
        achivments = db.collection('achivments').stream()



        for user in users:
            if user.get('userId') == user_table_ID:
                user_login = user.get('login')
                self.uch_info.ui.groupBox.setTitle(user.get('name'))
                self.uch_info.ui.label_6.setText(str(user.get('allPoints')))
                self.uch_info.ui.label_17.setText(str(user.get('hours')))
                self.uch_info.ui.lineEdit_3.setText(str(user.get('password')))
                self.uch_info.ui.lineEdit_2.setText(str(user.get('login')))


                #achivments = db.collection('achivments').stream()
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
                    counter = db.collection('counters').document(achiv.get('counter')).get()
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEnabled)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 2, item)
                    if len(user.get('achivProgress').get(achiv.get('achivID'))) <= 7:

                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 2).setText(
                            str(counter.get('users').get(user.get('userId'))))
                    else:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 2).setText(str(achiv.get('pointsNeed')))

                    # награда
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    self.uch_info.ui.tableWidget.setItem(achiv_counter - 1, 3, item)

                    if len(user.get('achivProgress').get(achiv.get('achivID'))) >= 7:
                        self.uch_info.ui.tableWidget.item(achiv_counter - 1, 3).setText(
                            str(achiv.get('point')))
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
                self.uch_info.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
                self.uch_info.ui.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
                self.uch_info.ui.lineEdit_2.setReadOnly(True)
                self.uch_info.ui.lineEdit_3.setReadOnly(True)
                self.uch_info.ui.pushButton_13.setText("Показать логин и пароль")
                self.uch_info.ui.lineEdit_2.setEnabled(False)
                self.uch_info.ui.lineEdit_3.setEnabled(False)
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
                'cardId': self.uch_info.ui.lineEdit.text()
            })
            print(user.id)
        self.update_uch_data_from_db()
        self.update_achiv_data_from_db()
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
        self.update_achiv_data_from_db()

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

    def delete_image_4(self):
        print("clicked")
        # fname = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'Image files (*.jpg *.png)')
        # imagePath = fname[0]
        self.ui.label_5.setPixmap(QtGui.QPixmap('logo.png'))


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

    def browseImage_4(self):
        print("clicked")
        fname = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'Image files (*.jpg *.png)')
        global imagePath
        imagePath = fname[0]
        self.ui.label_5.setPixmap(QtGui.QPixmap(imagePath))

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

    #поиск учеников в информации о достижении
    def search_uch_in_achiv(self):
        print("searched")

        if self.achiv_info.ui.lineEdit.text() != "":
            print("Поиск по тексту")

            # текст
            items_text_row = []
            rows = self.achiv_info.ui.tableWidget.rowCount()
            for i in range(rows):
                print(self.achiv_info.ui.tableWidget.item(i, 1).text())
                if self.achiv_info.ui.tableWidget.item(i, 1).text().find(str(self.achiv_info.ui.lineEdit.text())) != -1:
                    items_text_row.append(i)
            print(items_text_row)

            if len(items_text_row) != 0:
                for i in range(self.achiv_info.ui.tableWidget.rowCount()):
                    self.achiv_info.ui.tableWidget.setRowHidden(i, False)
                # скрытие лишних
                for i in range(self.achiv_info.ui.tableWidget.rowCount()):
                    if i not in items_text_row:
                        self.achiv_info.ui.tableWidget.setRowHidden(i, True)
        else:
            for i in range(self.achiv_info.ui.tableWidget.rowCount()):
                self.achiv_info.ui.tableWidget.setRowHidden(i, False)


    # получение сообщения
    @QtCore.pyqtSlot(list)
    def update_messages(self, message_a):
        print("update_messages")
        # само сообщение
        print(message_a)
        self.message_a = message_a
        # Изменение количества строк

        self.ui.tableWidget_uch_in_achiv.setRowCount(len(message_a))
        lenght = self.ui.tableWidget_uch_in_achiv.rowCount()

        #users = db.reference('users').get()
        #users_count = len(users)

        find_id = ''
        user_name = ''
        # Изменение текста в итеме
        for i in range(lenght):
            print(message_a[i])
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_uch_in_achiv.setItem(i, 1, item)
            self.ui.tableWidget_uch_in_achiv.item(i, 1).setText(message_a[i])


            users=db.collection('users').where(u'name', u'==', message_a[i]).stream()
            for user in users:
                find_id= user.id
            print('find_id',find_id)

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
    print('main')
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