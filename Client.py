import json
import os
import random
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
import sys
import csv
from cypherPass import encrypt_string
import pyperclip
from getAccNumber import get_rnd_acc_number

"""
Ceci un projet de banque, d'interface d'une banque.

Pour l'instant elle possède un problème: on peut injecter du code html et C++ via les boites d'entrées de text
Je ne sais pas si cela pose un vrai problème mais c'est à notifier.
J'ai fait quelques test et cela ne semble poser aucun problème niveau sécurité, on ne peut pas obtenir d'information
via ces injections (selon mes test bien-sûr)









"""

class MainWindow(QMainWindow):
    def __init__(self):
        self.e_boxes_w, self.e_boxes_h = 175, 30
        self.buttons_w, self.buttons_h = 90, 30

        super().__init__()
        self.setWindowTitle("KnoxBank Login Page")
        self.setFixedSize(400, 350)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()
        self._init_pos()

        self._set_entry_boxes()
        self._set_buttons()
        self._set_label()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5
        self.registering = False

    def hide_error(self):
        self.error_label.setVisible(False)

    def _init_pos(self):
        self.e_box1_gap = (0, 100)
        self.e_box1 = (self.width()//2 - self.e_boxes_w//2, self.height()//2 - self.e_boxes_h//2 - self.e_box1_gap[1])
        
        self.e_box2_gap = (0, 50)
        self.e_box2 = (self.width()//2 - self.e_boxes_w//2, self.height()//2 - self.e_boxes_h//2 - self.e_box2_gap[1])

        self.l_button_gap = (0, 0)
        self.l_button = (self.width()//2 - self.buttons_w//2 - self.l_button_gap[0], self.height()//2 - self.buttons_h//2)

        size_label = QtWidgets.QLabel(self)
        size_label.setVisible(False)
        size_label.setText("Not a member yet? Register now!")
        size_label.adjustSize()
        w_r_label = size_label.width()
        self.x_r_label = self.width()//2 - w_r_label//2

        size_label = QtWidgets.QLabel(self)
        size_label.setVisible(False)
        size_label.setText("Already a member? Login now!")
        size_label.adjustSize()
        w_r_label = size_label.width()
        self.x_r_label1 = self.width()//2 - w_r_label//2

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y() - 100)

    def _set_entry_boxes(self):
        self.user_box = QtWidgets.QLineEdit(self)
        self.user_box.move(self.e_box1[0], self.e_box1[1])
        self.user_box.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.user_box.setPlaceholderText("Username")
        self.user_box.setMaxLength(30)

        self.password_box = QtWidgets.QLineEdit(self)
        self.password_box.move(self.e_box2[0], self.e_box2[1])
        self.password_box.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.password_box.setPlaceholderText("Password")
        self.password_box.setEchoMode(QLineEdit.Password)

        self.password_box1 = QtWidgets.QLineEdit(self)
        self.password_box1.move(self.e_box2[0], self.e_box2[1] + 50)
        self.password_box1.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.password_box1.setPlaceholderText("Confirm Password")
        self.password_box1.setEchoMode(QLineEdit.Password)
        self.password_box1.setVisible(False)

    def _set_buttons(self):
        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setText("Login")
        self.login_button.setFixedSize(self.buttons_w, self.buttons_h)
        self.login_button.move(self.l_button[0], self.l_button[1])
        self.login_button.clicked.connect(lambda:self._button_log_clicked(self.user_box.text(), self.password_box.text()))

        self.register_button = QtWidgets.QPushButton(self)
        self.register_button.setText("Register")
        self.register_button.setFixedSize(self.buttons_w, self.buttons_h)
        self.register_button.move(self.l_button[0], self.l_button[1] + 50)
        self.register_button.clicked.connect(lambda:self._button_reg_clicked(self.user_box.text(), self.password_box.text(), self.password_box1.text()))
        self.register_button.setVisible(False)

    def _set_label(self):
        self.register1 = QtWidgets.QLabel(self)
        self.register1.setText("Not a member yet? ")
        self.register1.adjustSize()
        self.register1.move(self.x_r_label, self.height()-30)    #self.login_button.y()+self.login_button.height()+10 To put just under login

        self.register2 = QtWidgets.QLabel(self)
        self.register2.setText("Register now!")
        self.register2.adjustSize()
        self.register2.move(self.register1.x()+self.register1.width(), self.register1.y())
        self.register2.setStyleSheet("text-decoration: underline;")
        self.register2.setCursor(QtCore.Qt.PointingHandCursor)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("Please check your username and password !")
        self.error_label.adjustSize()
        self.e_w, self.e_h = self.error_label.width(), self.error_label.height()
        self.error_label.move(self.login_button.x() + self.login_button.width()//2 - self.e_w//2, self.login_button.y() + self.login_button.height()+10)
        self.error_label.setVisible(False)

        self.login1 = QtWidgets.QLabel(self)
        self.login1.setText("Already a member? ")
        self.login1.adjustSize()
        self.login1.move(self.x_r_label1, self.height()-30) 
        self.login1.setVisible(False)

        self.login2 = QtWidgets.QLabel(self)
        self.login2.setText("Login now!")
        self.login2.adjustSize()
        self.login2.move(self.login1.x()+self.login1.width(), self.login1.y())
        self.login2.setStyleSheet("text-decoration: underline;")
        self.login2.setCursor(QtCore.Qt.PointingHandCursor)
        self.login2.setVisible(False)

    def mousePressEvent(self, event):
        rect = self.register2.geometry()
        if rect.contains(event.pos()):
            if not self.registering:
                self.register()
            else:
                self.login()

    def show_error(self):
        self.error_label.adjustSize()
        self.e_w, self.e_h = self.error_label.width(), self.error_label.height()
        if self.registering:
            self.error_label.move(self.login_button.x() + self.login_button.width()//2 - self.e_w//2, self.login_button.y() + self.login_button.height()+60)
        else:
            self.error_label.move(self.login_button.x() + self.login_button.width()//2 - self.e_w//2, self.login_button.y() + self.login_button.height()+10)
        self.error_label.setVisible(True)
        self.timer.start(int(self.time*1000))

    def _button_log_clicked(self, log_user, password):
        data = self._get_data()
        for i,th in enumerate(data):
            if th[0] == log_user:
                self._check_password(i, password)
                break
        else:
            self.error_label.setText("Please check your username and password !")
            self.show_error()
            self.error_label.setVisible(True)

    def _button_reg_clicked(self, username, passw, passw1):
        data = self._get_data()
        if len(username) == 0:
            self.error_label.setText("Username cant be empty!")
            self.show_error()
            return
        
        test = 0
        for ch in username:
            if ch == " ":
                test = 1
            else:
                test = 0
                break
        if test == 1:
            self.error_label.setText("Username cant be empty!")
            self.show_error()
            return
        
        for th in data:
            if th[0] == username:
                self.error_label.setText("Username already taken!")
                self.show_error()
                return

        if passw == passw1 and len(passw) >= 7:
                self._register(username, encrypt_string(passw))
        elif passw == "" or len(passw) < 7:
                self.error_label.setText("The password must be 7 or more characters long!")
                self.show_error()
        else:
            self.error_label.setText("The passwords are not the same!")
            self.show_error()

    def _check_password(self, index, password):
        data = self._get_data()
        if data[index][1] == encrypt_string(password):
            self.grant_access()
        else:
            self.show_error()
            self.error_label.setVisible(True)

    def _get_data(self):
        with open("Data/UserData.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

            return data
        
    def _get_ibans(self):
        data = self._get_data()
        ibans = []
        try:
            for th in data:
                ibans.append(th[3])
            return ibans
        except:
            return []

    def _get_rnd_iban(self):
        ibans=self._get_ibans()
        iban=""
        while iban in ibans or iban == "":
            iban = "FR" + str(random.randint(0, 9)) + str(random.randint(0, 9)) + "-"
            for i in range(5):
                iban+=str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+"-"
            iban+=str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))
        return iban
        
    def _register(self, user, password):
        id = get_rnd_acc_number()
        iban = self._get_rnd_iban()
        with open("Data/UserData.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

        with open("Data/UserData.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
            writer.writerow([user, password, id, encrypt_string(iban)])

        os.mkdir("Data/Users/"+str(user))
        os.mkdir("Data/Users/"+str(user)+"/Accounts")

        with open("Data/Users/"+user+"/data.json", "w") as w:
            json.dump({"Name": user, "Client-Number": id, "Password": password, "IBAN": iban}, w)

        with open("Data/Users/"+user+"/lastTransactions.json", "w") as w:
            json.dump({}, w)

        with open("Data/Users/"+user+"/Accounts/Main.json", "w") as w:
            json.dump({"Name": "Main", "Account-Number": id, "Balance": 0.0}, w)

        with open("Data/Users/"+user+"/Accounts/ids.csv", "w", newline='') as w:
            writer = csv.writer(w)
            writer.writerow([str(id), "Main"])

        window = MainWindow()
        self.hide()
        window.show()
    
    def get_whole_data(self, username):
        with open("Data/Users/"+username+"/data.json", "r") as r:
            return json.load(r)
        
    def get_acc_data(self, username):
        with open("Data/Users/"+username+"/Accounts/Main.json", "r") as r:
            return json.load(r)

    def grant_access(self):
        self.account_window = Account(self.user_box.text(), self.get_acc_data(self.user_box.text()), self.get_whole_data(self.user_box.text())) #self.user_box.text(), self._get_data()
        self.account_window.show()
        self.hide()

    def register(self):
        self.reset_content()
        self.set_visible_all(False)

    def login(self):
        self.reset_content()
        self.set_visible_all(True)

    def reset_content(self):
        self.password_box.setText("")
        self.password_box1.setText("")
        self.user_box.setText("")

    def set_visible_all(self, condition):
        self.login_button.setVisible(condition)
        self.register_button.setVisible(not condition)
        self.password_box1.setVisible(not condition)
        self.error_label.setVisible(False)
        self.register1.setVisible(condition)
        self.register2.setVisible(condition)
        self.registering = not condition

        self.login1.setVisible(not condition)
        self.login2.setVisible(not condition)

class Account(QMainWindow):
    def __init__(self, username, acc_data: dict, whole_data: dict):
        self.username = username
        self.acc_data = acc_data
        self.whole_data = whole_data

        super().__init__()
        self.setWindowTitle("KnoxBank Account Page")
        self.setFixedSize(1400, 800)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self.activateWindow()

        self.padx = 60
        self.pady = 60

        self.icon_w, self.icon_h = 80, 80
        self._basic_ui_window()
        self._put_icon()
        self._put_labels()

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _basic_ui_window(self):
        self.label = QtWidgets.QLabel(self)
        self.label.move(self.width()-self.padx*2-self.icon_w, 0)
        self.label.setFixedSize(self.width()-self.label.x(), self.height()-self.label.y())
        self.label.setStyleSheet("background-color: lightgrey")

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setFixedSize(self.width()-self.label.width(), self.height()-self.label2.y())
        self.label2.setStyleSheet("background-color: lightgrey")

        self.line = QtWidgets.QLabel(self)
        self.line.move(self.label.x()-1, 0)
        self.line.setFixedSize(2, self.height()-self.label.y())
        self.line.setStyleSheet("background-color: black")

        self.line1 = QtWidgets.QLabel(self)
        self.line1.move(0, 150)
        self.line1.setFixedSize(self.line.x()-self.line1.x(), 2)
        self.line1.setStyleSheet("background-color: black")

    def _get_transactions(self):
        with open("Data/Users/"+self.username+"/lastTransactions.json", "r") as r:
            return json.load(r)

    def _put_labels(self):
        self.user_label = QtWidgets.QLabel(self)
        self.user_label.move(50, 0)
        self.user_label.setFixedHeight(self.line1.y())
        self.user_label.setText("Welcome back " + self.username + " !")
        self.user_label.setStyleSheet("font-size: 40px")
        self.user_label.adjustSize()

        self.balance_label = QtWidgets.QLabel(self)
        self.balance_label.move(50, self.line1.y()+50)
        self.balance_label.setText("Balance: " + str(self.acc_data.get("Balance")))
        self.balance_label.setStyleSheet("font-size: 34px")
        self.balance_label.adjustSize()

        transac = self._get_transactions()
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.scroll_area.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)

        transac_text = ""
        for th in reversed(transac):
            if transac.get(th)[0]<0:
                transac_text+=f"""<p>{self._rmv_chars(th, 15)}: <font color="red">{transac.get(th)[0]}</font> : {transac.get(th)[1]}<p>"""
            else:
                transac_text+=f"""<p>{self._rmv_chars(th, 15)}: <font color="green">+{transac.get(th)[0]}</font> : {transac.get(th)[1]}<p>"""
            
        label = QLabel()
        label.setText(transac_text)
        label.setStyleSheet("font-size: 14px;")  

        layout.addWidget(label)

        self.scroll_area.move(self.balance_label.x()+50, self.balance_label.y()+self.balance_label.height()+20)
        self.scroll_area.setFixedSize(300, 400)
        self.scroll_area.setStyleSheet("background-color: lightgray;")
    
    def _rmv_chars(self, text, chars):
        sec_text = ""
        for i in range(len(text)-chars):
            sec_text += text[i]
        return sec_text 

    def _put_icon(self):
        self.acc_label = QtWidgets.QLabel(self)
        acc = QPixmap("GUI/account.png")
        acc = acc.scaled(self.icon_w, self.icon_h)
        self.acc_label.setPixmap(acc)
        self.acc_label.resize(acc.width(), acc.height())
        self.acc_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.info_label = QtWidgets.QLabel(self)
        info = QPixmap("GUI/info.png")
        info = info.scaled(self.icon_w, self.icon_h)
        self.info_label.setPixmap(info)
        self.info_label.resize(info.width(), info.height())
        self.info_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.settings_label = QtWidgets.QLabel(self)
        sett = QPixmap("GUI/settings.png")
        sett = sett.scaled(self.icon_w, self.icon_h)
        self.settings_label.setPixmap(sett)
        self.settings_label.resize(sett.width(), sett.height())
        self.settings_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.transfert_label = QtWidgets.QLabel(self)
        transf = QPixmap("GUI/transfert.png")
        transf = transf.scaled(self.icon_w, self.icon_h)
        self.transfert_label.setPixmap(transf)
        self.transfert_label.resize(transf.width(), transf.height())
        self.transfert_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.logout_label = QtWidgets.QLabel(self)
        logout = QPixmap("GUI/logout.png")
        logout = logout.scaled(self.icon_w, self.icon_h)
        self.logout_label.setPixmap(logout)
        self.logout_label.resize(logout.width(), logout.height())
        self.logout_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.acc_label.move(self.width() - self.acc_label.width() - self.padx, self.pady)
        self.transfert_label.move(self.width() - self.transfert_label.width() - self.padx, self.acc_label.y() + self.acc_label.height() + self.pady)
        self.info_label.move(self.width() - self.info_label.width() - self.padx, self.transfert_label.y() + self.acc_label.height() + self.pady)
        self.settings_label.move(self.width() - self.settings_label.width() - self.padx, self.info_label.y() + self.acc_label.height() + self.pady)
        self.logout_label.move(self.width() - self.logout_label.width() - self.padx, self.settings_label.y() + self.acc_label.height() + self.pady)

    def mousePressEvent(self, event):
        acc_rect = self.acc_label.geometry()
        transfert_rect = self.transfert_label.geometry()
        info_rect = self.info_label.geometry()
        settings_rect = self.settings_label.geometry()
        logout_rect = self.logout_label.geometry()

        if acc_rect.contains(event.pos()):
            self.acc_clicked()
        elif transfert_rect.contains(event.pos()):
            self.transfert_clicked()
        elif info_rect.contains(event.pos()):
            self.info_clicked()
        elif settings_rect.contains(event.pos()):
            self.settings_clicked()
        elif logout_rect.contains(event.pos()):
            self.logout_clicked()

    def acc_clicked(self):
        self.account = Accounts(self.username, self.acc_data, self.whole_data)
        self.account.show()
        self.hide()

    def transfert_clicked(self):
        self.hide()
        self.transfert_window = Transfert(self.username, self.acc_data, self.whole_data)
        self.transfert_window.show()
            
    def info_clicked(self):
        self.info = Info(self.username, self.acc_data, self.whole_data)
        self.hide()
        self.info.show()

    def settings_clicked(self):
        self.settings = Setting(self.username, self.acc_data, self.whole_data)
        self.hide()
        self.settings.show()

    def logout_clicked(self):   
        self.window_ = MainWindow() #self.user_box.text(), self._get_data()
        self.window_.show()
        self.hide()

class Transfert(QMainWindow):
    def __init__(self, username, acc_data, whole_data):
        self.e_boxes_w, self.e_boxes_h = 300, 30
        self.button_w, self.button_h = 100, 30

        super().__init__()
        self.setWindowTitle(f"{username}'s Transfert Window")
        self.setFixedSize(400, 450)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self.username = username
        self.acc_data = acc_data
        self.whole_data = whole_data

        self._set_boxes()
        self._init_label()
        self._init_button()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def hide_error(self):
        self.error_label.setText("")

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _set_boxes(self):
        self.iban_box = QtWidgets.QLineEdit(self)
        self.iban_box.setPlaceholderText("IBAN: FR00-1234-1234-1234-1234-1234-123")
        self.iban_box.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.iban_box.move(self.width()//2-self.iban_box.width()//2, 160)

        self.amount_box = QtWidgets.QLineEdit(self)
        self.amount_box.setPlaceholderText("Amount: Minimum 5€ (5, 10, 15...)")
        self.amount_box.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.amount_box.move(self.width()//2-self.iban_box.width()//2, self.iban_box.y()+50)

        self.object_box = QtWidgets.QLineEdit(self)
        self.object_box.setPlaceholderText("Object: (optional)")
        self.object_box.setFixedSize(self.e_boxes_w, self.e_boxes_h)
        self.object_box.move(self.width()//2-self.iban_box.width()//2, self.amount_box.y()+50)

    def _init_label(self):
        self.balance_label = QtWidgets.QLabel(self)
        self.balance_label.setText("Current Balance: " + str(self.acc_data.get("Balance")))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, self.iban_box.y()-50)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.move(self.width()//2, self.object_box.y()+50)

    def _updt_balance(self):
        self.balance_label.setText("Current Balance: " + str(self.acc_data.get("Balance")))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, self.iban_box.y()-50)

    def _update_error_label(self, text):
        self.error_label.setText(text)
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.error_label.y())
        self.timer.start(int(self.time*1000))

    def _init_button(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.pressed.connect(self._back_clicked)
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()-10, self.height()-50)

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setText("Send")
        self.submit_button.pressed.connect(self._sub_clicked)
        self.submit_button.setFixedSize(self.button_w, self.button_h)
        self.submit_button.move(self.back_button.x()+self.back_button.width()+20, self.height()-50)

    def _back_clicked(self):
        self.window_ = Account(self.username, self.acc_data, self.whole_data)
        self.hide()
        self.window_.show()

    def get_data(self, username):
        with open("Data/Users/"+username+"/Accounts/Main.json", "r") as r:
            return json.load(r)
        
    def get_transactions(self, username):
        with open("Data/Users/"+username+"/lastTransactions.json", "r") as r:
            return json.load(r)

    def _sub_clicked(self):
        if self.iban_box.text() == "" or encrypt_string(self.iban_box.text()) not in self._get_ibans():
            self._update_error_label("Please, enter a correct IBAN number.")
        elif self.amount_box.text() == "":
            self._update_error_label("Please, enter a correct amount number.")
        else:
            try:
                amount = float(self.amount_box.text())
                if amount < 5:
                    self._update_error_label("Your transfert must be superior than 5€")
                elif amount<=self.acc_data.get("Balance"):
                    if self.iban_box.text() == self.whole_data.get("IBAN"):
                        self._update_error_label("You can't send money to yourself..")
                    else:
                        self._transfert(self.iban_box.text(), amount)
                        self._update_error_label("Transfert succeed!")
                else:
                    self._update_error_label("You dont have enough money..")
            except:
                self._update_error_label("Please, enter a correct amount number.")

            
    def _transfert(self, iban, amount):
        self.acc_data["Balance"] = self.acc_data.get("Balance")-amount
        self._write(self.acc_data, amount)
        self.give_mney(iban, amount)
        self._updt_balance()

        self.iban_box.setText("")
        self.object_box.setText("")
        self.amount_box.setText("")
        
    def get_date(self):
        lc_time = time.localtime()
        d = lc_time[2]
        m = lc_time[1]
        y = lc_time[0]
        minu = lc_time[4]
        ho = lc_time[3]
        id = time.monotonic_ns()

        if len(str(d)) == 1:
            d = "0"+str(d)
        if len(str(m)) == 1:
            m = "0"+str(m)
        if len(str(minu)) == 1:
            minu = "0"+str(minu)
        if len(str(ho)) == 1:
            ho = "0"+str(ho)

        date = f"{d}-{m}-{y}-{ho}h{minu}-{id}"
        return date 

    def give_mney(self, iban, amount):
        data = self._get_data()
        for th in data:
            if encrypt_string(iban) == th[3]:
                user = th[0]
                u_data = self.get_data(user)
                u_data["Balance"] = u_data.get("Balance")+amount
                with open("Data/Users/"+user+"/Accounts/Main.json", "w") as w:
                    json.dump(u_data, w)

                l_transact = self.get_transactions(user)
                l_transact[self.get_date()] = [amount, self._get_obj()]

                with open("Data/Users/"+user+"/lastTransactions.json", "w") as w:
                    json.dump(l_transact, w)

    def _get_ibans(self):
        data = self._get_data()
        ibans = []
        try:
            for th in data:
                ibans.append(th[3])
            return ibans
        except:
            return []
        
    def _get_data(self):
        with open("Data/UserData.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

            return data
        
    def _get_transactions(self):
        with open("Data/Users/"+self.username+"/lastTransactions.json", "r") as r:
            return json.load(r)
        
    def _get_obj(self):
        if self.object_box.text()=="":
            return "None"
        return self.object_box.text()
        
    def _write(self, data, transfert):
        transacs = self._get_transactions()
        obj = self._get_obj()
        date = self.get_date()
        transacs[date]=[-transfert, obj]
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "w") as w:
            json.dump(data, w)

        with open("Data/Users/"+self.username+"/lastTransactions.json", "w") as w:
            json.dump(transacs, w)

class Info(QMainWindow):
    def __init__(self, username, acc_data, whole_data):
        super().__init__()
        self.setWindowTitle(f"{username}'s Info Window")
        self.setFixedSize(400, 450)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self.username = username
        self.whole_data = whole_data
        self.acc_data = acc_data

        self.e_boxes_w, self.e_boxes_h = 300, 30
        self.button_w, self.button_h = 100, 30

        self._init_button()
        self._init_labels()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _init_button(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, 380)
        self.back_button.pressed.connect(self.back_button_clicked)

    def _init_labels(self):
        test1 = QtWidgets.QLabel(self)
        test1.setText("IBAN: FR00-0000-0000-0000-0000-0000-000")
        test1.adjustSize()
        test1.setVisible(False)

        self.IBAN1_label = QtWidgets.QLabel(self)
        self.IBAN1_label.setText(f"IBAN: ")
        self.IBAN1_label.adjustSize()
        self.IBAN1_label.move(self.width()//2-test1.width()//2, 50)

        self.IBAN_label = QtWidgets.QLabel(self)
        self.IBAN_label.setText(f"""<font color="blue">{self.whole_data.get("IBAN")}</font>""")
        self.IBAN_label.move(self.IBAN1_label.x()+self.IBAN1_label.width(), self.IBAN1_label.y())
        self.IBAN_label.setStyleSheet("text-decoration: underline;")
        self.IBAN_label.adjustSize()
        self.IBAN_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.user1_label = QtWidgets.QLabel(self)
        self.user1_label.setText(f"Account Name: ")
        self.user1_label.adjustSize()
        self.user1_label.move(self.width()//2-test1.width()//2, self.IBAN1_label.y()+50)

        self.user_label = QtWidgets.QLabel(self)
        self.user_label.setText(f"""<font color="blue">{self.whole_data.get("Name")}</font>""")
        self.user_label.move(self.user1_label.x()+self.user1_label.width(), self.user1_label.y())
        self.user_label.setStyleSheet("text-decoration: underline;")
        self.user_label.adjustSize()
        self.user_label.setCursor(QtCore.Qt.PointingHandCursor)

        self.id1_account = QtWidgets.QLabel(self)
        self.id1_account.setText(f"Account ID: ")
        self.id1_account.adjustSize()
        self.id1_account.move(self.width()//2-test1.width()//2, self.user1_label.y()+50)

        self.id_account = QtWidgets.QLabel(self)
        self.id_account.setText(f"""<font color="blue">{self.whole_data.get("Client-Number")}</font>""")
        self.id_account.move(self.id1_account.x()+self.id1_account.width(), self.id1_account.y())
        self.id_account.setStyleSheet("text-decoration: underline;")
        self.id_account.adjustSize()
        self.id_account.setCursor(QtCore.Qt.PointingHandCursor)

        self.infos_label = QtWidgets.QLabel(self)
        self.infos_label.move(self.width()//2, self.back_button.y()-50)

    def _updt_info_label(self, info):
        self.infos_label.setText(info)
        self.infos_label.adjustSize()
        self.infos_label.move(self.width()//2-self.infos_label.width()//2, self.back_button.y()-50)
        self.timer.start(int(self.time*1000))

    def back_button_clicked(self):
        self.account = Account(self.username, self.acc_data, self.whole_data)
        self.hide()
        self.account.show()

    def hide_error(self):
        self.infos_label.setText("")

    def mousePressEvent(self, event):
        iban = self.IBAN_label.geometry()
        username = self.user_label.geometry()
        id_acc = self.id_account.geometry()
        if iban.contains(event.pos()):
            pyperclip.copy(self.whole_data.get("IBAN"))
            self._updt_info_label("IBAN copied!")
        elif username.contains(event.pos()):
            pyperclip.copy(self.whole_data.get("Name"))
            self._updt_info_label("Username copied!")
        elif id_acc.contains(event.pos()):
            pyperclip.copy(self.whole_data.get("Client-Number"))
            self._updt_info_label("Account ID copied!")

class Setting(QMainWindow):
    def __init__(self, username, acc_data, whole_data):
        self.username = username
        self.acc_data = acc_data
        self.whole_data = whole_data

        self.button_w, self.button_h = 150, 30

        super().__init__()
        self.setWindowTitle(f"{username}'s Settings Window")
        self.setFixedSize(400, 450)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._updt_label()
        self._init_buttons()

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _updt_label(self):
        self.user_change_label = QtWidgets.QLabel(self)
        self.user_change_label.setText("Current Username: " + f"""<u>{self.username}<u>""")
        self.user_change_label.adjustSize()
        self.user_change_label.move(self.width()//2-self.user_change_label.width()//2, 50)

    def _init_buttons(self):
        self.user_change_button = QtWidgets.QPushButton(self)
        self.user_change_button.setText("Change Username")
        self.user_change_button.setFixedSize(self.button_w, self.button_h)
        self.user_change_button.move(self.width()//2-self.user_change_button.width()//2, self.user_change_label.y()+25)
        self.user_change_button.pressed.connect(lambda:self._ch_user_pressed(True))

        self.password_change_button = QtWidgets.QPushButton(self)
        self.password_change_button.setText("Change Password")
        self.password_change_button.setFixedSize(self.button_w, self.button_h)
        self.password_change_button.move(self.width()//2-self.password_change_button.width()//2, 130)
        self.password_change_button.pressed.connect(lambda:self._ch_user_pressed(False))

        self.delete_acc_button = QtWidgets.QPushButton(self)
        self.delete_acc_button.setText("Delete Account")
        self.delete_acc_button.setFixedSize(self.button_w, self.button_h)
        self.delete_acc_button.move(self.width()//2-self.delete_acc_button.width()//2, 170)
        self.delete_acc_button.pressed.connect(self.delete_acc_pressed)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w//15*10, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-60)
        self.back_button.pressed.connect(self._back_pressed)

    def _back_pressed(self):
        self.acc = Account(self.username, self.acc_data, self.whole_data)
        self.hide()
        self.acc.show()

    def _ch_user_pressed(self, user):
        self.popup = PopUpChange(self.username, self.whole_data, user, self)
        self.popup.show()

    def delete_acc_pressed(self):
        self.win = DeleteAccount(self.username, self.acc_data, self)
        self.win.show()

class DeleteAccount(QMainWindow):
    def __init__(self, username, acc_data, window):
        self.username = username
        self.acc_data = acc_data
        self.window_ = window
        self.window_.hide()

        self.button_w, self.button_h = 200, 100

        super().__init__()
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.setWindowTitle("Delete Account?")
        self.center()

        self._init_buttons()
        self._init_labels()

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _init_labels(self):
        warning_label = QtWidgets.QLabel(self)
        warning_label.setText("Are you sure you want to delete your account?")
        warning_label.setStyleSheet("font-size: 20px")
        warning_label.adjustSize()
        warning_label.move(self.width()//2-warning_label.width()//2, 50)

        warning_label2 = QtWidgets.QLabel(self)
        warning_label2.setText("This action is irreversible.")
        warning_label2.setStyleSheet("font-size: 20px")
        warning_label2.adjustSize()
        warning_label2.move(self.width()//2-warning_label2.width()//2, 80)

        warning_label3 = QtWidgets.QLabel(self)
        warning_label3.setText("You will loose all your data, ")
        warning_label3.setStyleSheet("font-size: 20px")
        warning_label3.adjustSize()
        warning_label3.move(self.width()//2-warning_label3.width()//2, 110)

        warning_label4 = QtWidgets.QLabel(self)
        warning_label4.setText("including your balance: " + (str(self.acc_data.get("Balance")) + "€."))
        warning_label4.setStyleSheet("font-size: 20px")
        warning_label4.adjustSize()
        warning_label4.move(self.width()//2-warning_label4.width()//2, 140)

    def _init_buttons(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.setText("BACK")
        self.back_button.move(40, self.height()-self.button_h-50)
        self.back_button.pressed.connect(self.back_clicked)

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setFixedSize(self.button_w, self.button_h)
        self.delete_button.setText("DELETE ACCOUNT \n(Erase all data)")
        self.delete_button.move(self.width()-self.button_w-40, self.height()-self.button_h-50)
        self.delete_button.pressed.connect(self.delete_clicked)

    def back_clicked(self):
        self.hide()
        self.window_.show()

    def _get_data(self):
        with open("Data/UserData.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

            return data

    def delete_clicked(self):
        data = self._get_data()
        things = []
        for th in data:
            if th[0] != self.username:
                things.append(th)

        with open("Data/UserData.csv", "w", newline='') as writer:
            write = csv.writer(writer)
            write.writerows(things)

        os.remove("Data/Users/"+self.username+"/data.json")
        os.remove("Data/Users/"+self.username+"/lastTransactions.json")

        for file in os.listdir("Data/Users/"+self.username+"/Accounts"):
            os.remove("Data/Users/"+self.username+"/Accounts/"+file)

        os.rmdir("Data/Users/"+self.username+"/Accounts")
        os.rmdir("Data/Users/"+self.username)
        
        self.hide()
        self.win = MainWindow()
        self.win.show()

class PopUpChange(QMainWindow):
    def __init__(self, username, data, ch_user_or_pass, window):
        self.username = username
        self.data = data

        self.window_ = window
        self.window_.hide()

        self.button_w, self.button_h = 150, 30
        self.boxes_w, self.boxes_h = 150, 30

        self.user_change = ch_user_or_pass

        super().__init__()
        if ch_user_or_pass: 
            self.setWindowTitle(f"Username")
        else:
            self.setWindowTitle(f"Password")

        self.setFixedSize(300, 350)
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_buttons()
        self._init_labels()
        self._init_boxes()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def hide_error(self):
        self.error_label.setText("")

    def _init_boxes(self):
        self.user_box = QtWidgets.QLineEdit(self)
        self.user_box.setPlaceholderText("New Username")
        self.user_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.user_box.move(self.label_n_user.x()+self.label_n_user.width()+5, self.label_n_user.y()+self.label_n_user.height()//2-self.user_box.height()//2)
        self.user_box.setMaxLength(30)

        self.l_password_box = QtWidgets.QLineEdit(self)
        self.l_password_box.setPlaceholderText("Current Password")
        self.l_password_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.l_password_box.move(self.password_label.x()+self.password_label.width()+5, self.password_label.y()+self.password_label.height()//2-self.l_password_box.height()//2)
        self.l_password_box.setEchoMode(QLineEdit.Password)

        self.n_password_box = QtWidgets.QLineEdit(self)
        self.n_password_box.setPlaceholderText("New Password")
        self.n_password_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.n_password_box.move(self.n_password_label.x()+self.n_password_label.width()+5, self.n_password_label.y()+self.n_password_label.height()//2-self.n_password_box.height()//2)
        self.n_password_box.setEchoMode(QLineEdit.Password)

        self.nc_password_box = QtWidgets.QLineEdit(self)
        self.nc_password_box.setPlaceholderText("Confirm Password")
        self.nc_password_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.nc_password_box.move(self.nc_password_label.x()+self.nc_password_label.width()+5, self.nc_password_label.y()+self.nc_password_label.height()//2-self.nc_password_box.height()//2)
        self.nc_password_box.setEchoMode(QLineEdit.Password)

        if self.user_change:
            self.l_password_box.hide()
            self.n_password_box.hide()
            self.nc_password_box.hide()
        else:
            self.user_box.hide()

    def _init_labels(self):
        self.label_n_user = QtWidgets.QLabel(self)
        self.label_n_user.setText("New Username: ")
        self.label_n_user.adjustSize()
        self.label_n_user.move(self.width()//2-self.label_n_user.width()//2-self.boxes_w//2, 50)

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("Current Password: ")
        self.password_label.adjustSize()
        self.password_label.move(self.width()//2-self.password_label.width()//2-self.boxes_w//2, 50)

        self.n_password_label = QtWidgets.QLabel(self)
        self.n_password_label.setText("New Password: ")
        self.n_password_label.adjustSize()
        self.n_password_label.move(self.width()//2-self.n_password_label.width()//2-self.boxes_w//2, 100)

        self.nc_password_label = QtWidgets.QLabel(self)
        self.nc_password_label.setText("New Password: ")
        self.nc_password_label.adjustSize()
        self.nc_password_label.move(self.width()//2-self.nc_password_label.width()//2-self.boxes_w//2, 150)

        if self.user_change:
            self.password_label.hide()
            self.n_password_label.hide()
            self.nc_password_label.hide()
        else:
            self.label_n_user.hide()

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.submit_button.y()-50)

    def _updt_error_label(self, error):
        self.error_label.setText(error)
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.error_label.y())

    def _init_buttons(self):
        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setText("Submit")
        self.submit_button.setFixedSize(self.button_w, self.button_h)
        self.submit_button.move(self.width()//2-self.submit_button.width()//2, self.height()-90)
        self.submit_button.pressed.connect(self._submit_clicked)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(int(self.button_w//1.5), self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-50)
        self.back_button.pressed.connect(self._back_clicked)

    def _back_clicked(self):
        self.hide()
        self.window_.show()

    def _submit_clicked(self):
        if self.user_change:
            n_username = self.user_box.text()
            data = self._get_data()

            if n_username == "":
                self._updt_error_label("Username cant be empty!")
                self.timer.start(int(self.time*1000))
                return
            
            test = 0
            for ch in n_username:
                if ch == " ":
                    test = 1
                else:
                    test = 0
                    break
            if test == 1:
                self._updt_error_label("Username cant be empty!")
                self.timer.start(int(self.time*1000))
                return

            for th in data:
                if th[0] == n_username:
                    self._updt_error_label("Username already used!")
                    self.timer.start(int(self.time*1000))
                    return
            if self.user_change:
                self.data["Name"] = n_username

            self._write_data(self.username)
            self.hide()
            self.window_.show()
            self.window_.username = n_username
            self.window_.data = self.data
            self.window_._updt_label(n_username)
            self.window_.setWindowTitle(f"{n_username}'s Settings Window")
        else:
            n_password = self.n_password_box.text()
            nc_password = self.nc_password_box.text()

            l_password = self.l_password_box.text()
            data = self._get_data()
            
            if encrypt_string(l_password) != self.data.get("Password"):
                self._updt_error_label("Incorrect current password!")
                self.timer.start(int(self.time*1000))
            elif len(n_password) < 7 or len(nc_password) < 7:
                self._updt_error_label("Password must be at least 7 characters long!")
                self.timer.start(int(self.time*1000))
            elif n_password != nc_password:
                self._updt_error_label("New passwords dont correspond..")
                self.timer.start(int(self.time*1000))
            else:
                self.data["Password"] = encrypt_string(n_password)
                self.window_.data = self.data
                self._change_user_csv()
                self.window_.show()
                self.hide()

    def _write_data(self, username):
        with open("Data/Users/"+username+"/data.json", "w") as w:
            json.dump(self.data, w)

        os.rename("Data/Users/"+username, "Data/Users/"+self.data.get("Name"))
        self._change_user_csv()

    def _change_user_csv(self):
        data = self._get_data()
        for i,th in enumerate(data):
            if th[0] == self.username:
                with open("Data/UserData.csv", "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for j,row in enumerate(data):
                        if i != j:
                            writer.writerow(row)
                        else:
                            writer.writerow([self.data.get("Name"), self.data.get("Password"), self.data.get("Account-Number"), encrypt_string(self.data.get("IBAN"))])

    def _get_data(self):
        with open("Data/UserData.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

            return data

class Accounts(QMainWindow):
    def __init__(self, username, acc_data, whole_data):
        self.username = username
        self.acc_data = acc_data
        self.whole_data = whole_data

        self.button_w, self.button_h = 130, 30

        super().__init__()

        self.setFixedSize(350, 350)
        self.setWindowTitle(f"{self.username}'s Accounts' Action page")
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_buttons()

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)
        
    def _init_buttons(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-self.back_button.height()-20)
        self.back_button.pressed.connect(self._back_pressed)

        self.manage_acc = QtWidgets.QPushButton(self)
        self.manage_acc.setText("Manage Accounts")
        self.manage_acc.setFixedSize(self.button_w+40, self.button_h)
        self.manage_acc.move(self.width()//2-self.manage_acc.width()//2, 40)
        self.manage_acc.pressed.connect(self._manage_acc_pressed)

        self.acc_transfert = QtWidgets.QPushButton(self)
        self.acc_transfert.setText("Account Transfert")
        self.acc_transfert.setFixedSize(self.button_w+40, self.button_h)
        self.acc_transfert.move(self.width()//2-self.acc_transfert.width()//2, 80)
        self.acc_transfert.pressed.connect(self._acc_transfert_pressed)

        self.create_acc = QtWidgets.QPushButton(self)
        self.create_acc.setText("Create Account")
        self.create_acc.setFixedSize(self.button_w+40, self.button_h)
        self.create_acc.move(self.width()//2-self.create_acc.width()//2, 120)
        self.create_acc.pressed.connect(self._create_acc_pressed)

        self.loans = QtWidgets.QPushButton(self)
        self.loans.setText("Loans")
        self.loans.setFixedSize(self.button_w+40, self.button_h)
        self.loans.move(self.width()//2-self.loans.width()//2, 190)
        self.loans.pressed.connect(self._loan_pressed)

    def _back_pressed(self):
        self.account = Account(self.username, self.acc_data, self.whole_data)
        self.account.show()
        self.hide()

    def _manage_acc_pressed(self):
        self.macc = AccountsManager(self.username, self.whole_data)
        self.macc.show()
        self.hide()

    def _acc_transfert_pressed(self):
        self.tra = AccountsTranfert(self.username, self.whole_data)
        self.tra.show()
        self.hide()

    def _create_acc_pressed(self):
        self.crea = AccountsCreation(self.username, self.whole_data)
        self.crea.show()
        self.hide()

    def _loan_pressed(self):
        self.loan = AccountsLoan(self.username, self.whole_data)
        self.loan.show()
        self.hide()

class AccountsManager(QMainWindow):
    def __init__(self, username, whole_data):
        self.username = username
        self.whole_data = whole_data

        self.button_w, self.button_h = 130, 30

        super().__init__()

        self.setFixedSize(500, 400)
        self.setWindowTitle(f"{self.username}'s Accounts Management page")
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_combo_box()
        self._init_buttons()
        self._init_labels()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def hide_error(self):
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.delete_acc.y()-25)
    
    def _updt_error_label(self, error):
        self.error_label.setText(error)
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.delete_acc.y()-25)
        self.timer.start(int(self.time*1000))

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def _updt_label(self):
        with open("Data/Users/"+self.username+"/Accounts/"+self.acc_combo_box.currentText()+".json", "r") as r:
            acc_data = json.load(r)
        self.balance_label.setText(f"{self.acc_combo_box.currentText()}'s Balance : "+str(acc_data["Balance"]))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, self.acc_combo_box.y()+self.acc_combo_box.height()+20)

    def _get_acc_names(self):
        names = []
        with open("Data/Users/"+self.username+"/Accounts/ids.csv", 'r') as r:
            reader = csv.reader(r)
            for th in reader:
                names.append(th[1])
            return names

    def _get_all_accs(self):
        names = []
        with open("Data/Users/"+self.username+"/Accounts/ids.csv", 'r') as r:
            reader = csv.reader(r)
            for th in reader:
                names.append(th)
            return names

    def get_acc_data(self):
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "r") as r:
            return json.load(r)

    def _init_labels(self):
        with open("Data/Users/"+self.username+"/Accounts/"+self.acc_combo_box.currentText()+".json", "r") as r:
            acc_data = json.load(r)
        self.balance_label = QtWidgets.QLabel(self)
        self.balance_label.setText(f"{self.acc_combo_box.currentText()}'s Balance : "+str(acc_data["Balance"]))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, self.acc_combo_box.y()+self.acc_combo_box.height()+20)

        self.info_label = QtWidgets.QLabel(self)
        self.info_label.setText("If you delete this account, its balance will be transfered")
        self.info_label.adjustSize()
        self.info_label.move(self.width()//2-self.info_label.width()//2, self.delete_acc.y()+self.delete_acc.height()+10)

        self.info_label1 = QtWidgets.QLabel(self)
        self.info_label1.setText("to your main account.")
        self.info_label1.adjustSize()
        self.info_label1.move(self.width()//2-self.info_label1.width()//2, self.delete_acc.y()+self.delete_acc.height()+25)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, self.delete_acc.y()-25)

    def _init_buttons(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-self.back_button.height()-20)
        self.back_button.pressed.connect(self._back_pressed)

        self.delete_acc = QtWidgets.QPushButton(self)
        self.delete_acc.setText("Delete Account")
        self.delete_acc.setFixedSize(self.button_w+40, self.button_h)
        self.delete_acc.move(self.width()//2-self.delete_acc.width()//2, self.height()-self.delete_acc.height()-100)
        self.delete_acc.pressed.connect(self._delete_pressed)

    def _delete_pressed(self):
        if self.acc_combo_box.currentText() == "Main":
            self._updt_error_label("You cant delete your Main account..")
            return
        with open("Data/Users/"+self.username+"/Accounts/"+self.acc_combo_box.currentText()+".json", "r") as r:
            data = json.load(r)
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "r") as r:
            main_data = json.load(r)

        main_data["Balance"]+=data["Balance"]

        with open("Data/Users/"+self.username+"/Accounts/Main.json", "w") as w:
            json.dump(main_data, w)

        with open("Data/Users/"+self.username+"/Accounts/ids.csv", "r") as r:
            reader = csv.reader(r)
            rows = []
            for th in reader:
                rows.append(th)
        with open("Data/Users/"+self.username+"/Accounts/ids.csv", "w", newline='') as w:
            writer = csv.writer(w)
            check_data = [str(data["Account-Number"]), data["Name"]]
            for row in rows:
                if check_data != row:
                    writer.writerow(row)

        os.remove("Data/Users/"+self.username+"/Accounts/"+self.acc_combo_box.currentText()+".json")
                
        self._back_pressed()

    def _back_pressed(self):
        self.acc = Accounts(self.username, self.get_acc_data(), self.whole_data)
        self.acc.show()
        self.hide()

    def _init_combo_box(self):
        self.acc_combo_box = QtWidgets.QComboBox(self)
        self.acc_combo_box.addItems(self._get_acc_names())
        self.acc_combo_box.setFixedSize(140, 40)
        self.acc_combo_box.move(self.width()//2-self.acc_combo_box.width()//2, 50)
        self.acc_combo_box.currentTextChanged.connect(self._updt_label)

class AccountsTranfert(QMainWindow):
    def __init__(self, username, whole_data):
        self.username = username
        self.whole_data = whole_data

        self.button_w, self.button_h = 130, 30

        super().__init__()

        self.setFixedSize(700, 400)
        self.setWindowTitle(f"{self.username}'s Tranfert page")
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_buttons()
        self._init_boxes()
        self._init_combo_box()
        self._init_labels()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def hide_error(self):
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.amount_box.x()+self.amount_box.width()//2-self.error_label.width()//2, self.amount_box.y()+self.amount_box.height()+15)

    def _updt_error_label(self, error):
        self.error_label.setText(error)
        self.error_label.adjustSize()
        self.error_label.move(self.amount_box.x()+self.amount_box.width()//2-self.error_label.width()//2, self.amount_box.y()+self.amount_box.height()+15)
        self.timer.start(int(self.time*1000))

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def get_acc_data(self):
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "r") as r:
            return json.load(r)

    def _back_pressed(self):
        self.account = Accounts(self.username, self.get_acc_data(), self.whole_data)
        self.account.show()
        self.hide()

    def _get_accs_name(self):
        names = []
        with open("Data/Users/"+self.username+"/Accounts/ids.csv", 'r') as r:
            reader = csv.reader(r)
            for th in reader:
                names.append(th[1])
            return names

    def _init_buttons(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-self.back_button.height()-20)
        self.back_button.pressed.connect(self._back_pressed)

        self.send_button = QtWidgets.QPushButton(self)
        self.send_button.setText("Send Money")
        self.send_button.setFixedSize(self.button_w+40, self.button_h)
        self.send_button.move(self.width()//2-self.send_button.width()//2, self.height()-self.send_button.height()-60)
        self.send_button.pressed.connect(self._submit_pressed)

    def _init_boxes(self):
        self.amount_box = QtWidgets.QLineEdit(self)
        self.amount_box.setPlaceholderText("Transfert amount")
        self.amount_box.setFixedSize(200, 30)
        self.amount_box.move(self.width()//2-self.amount_box.width()//2, 100)

    def _init_combo_box(self):
        self.sender_c_box = QtWidgets.QComboBox(self)
        self.sender_c_box.addItems(self._get_accs_name())
        self.sender_c_box.setFixedSize(140, 50)
        self.sender_c_box.move(self.amount_box.x()//2-self.sender_c_box.width()//2, self.amount_box.y()+self.amount_box.height()//2-self.sender_c_box.height()//2)
        self.sender_c_box.setStyleSheet("QComboBox { font-size: 15px; }")
        self.sender_c_box.currentTextChanged.connect(self._sender_changed)

        self.receiver_c_box = QtWidgets.QComboBox(self)
        self.receiver_c_box.addItems(self._get_accs_name())
        self.receiver_c_box.setFixedSize(140, 50)
        self.receiver_c_box.move(self.amount_box.x()+self.amount_box.width()+((self.width()-(self.amount_box.x()+self.amount_box.width()))//2)-self.receiver_c_box.width()//2, self.amount_box.y()+self.amount_box.height()//2-self.sender_c_box.height()//2)
        self.receiver_c_box.setStyleSheet("QComboBox { font-size: 15px; }")
        self.receiver_c_box.currentTextChanged.connect(self._receiver_changed)

    def _sender_changed(self):
        self.sender_bal.setText(f"Balance: {self._get_bal(self.sender_c_box.currentText())}")
        self.sender_bal.setStyleSheet("font-size: 15px;")
        self.sender_bal.adjustSize()
        self.sender_bal.move(self.sender_c_box.x()+self.sender_c_box.width()//2-self.sender_bal.width()//2, self.sender_c_box.y()+self.sender_c_box.height()+15)

    def _receiver_changed(self):
        self.receiver_bal.setText(f"Balance: {self._get_bal(self.receiver_c_box.currentText())}")
        self.receiver_bal.setStyleSheet("font-size: 15px;")
        self.receiver_bal.adjustSize()
        self.receiver_bal.move(self.receiver_c_box.x()+self.receiver_c_box.width()//2-self.receiver_bal.width()//2, self.receiver_c_box.y()+self.receiver_c_box.height()+15)

    def _get_bal(self, acc_name):
        with open("Data/Users/"+self.username+"/Accounts/"+acc_name+".json", "r") as r:
            return json.load(r)["Balance"]
        
    def _submit_pressed(self):
        sender_bal = float(self._get_bal(self.sender_c_box.currentText()))
        bal = self.amount_box.text()
        
        try:
            bal = int(bal)
            if sender_bal<bal:
                self._updt_error_label("Not enough money in " + self.sender_c_box.currentText())
            elif self.sender_c_box.currentText() == self.receiver_c_box.currentText():
                self._updt_error_label("Cant send money to the same account..")
            elif bal <= 0:
                self._updt_error_label("Transfert must be superior than 0")
            else:
                self._send_money(bal, self.sender_c_box.currentText(), self.receiver_c_box.currentText())
        except:
            self._updt_error_label("Invalid amount!")

    def _send_money(self, amount, sender, receiver):
        with open("Data/Users/"+self.username+"/Accounts/"+sender+".json", "r") as r:
            sender_data = json.load(r)

        with open("Data/Users/"+self.username+"/Accounts/"+receiver+".json", "r") as r:
            receiver_data = json.load(r)

        sender_data["Balance"] -= amount
        receiver_data["Balance"] += amount

        with open("Data/Users/"+self.username+"/Accounts/"+sender+".json", "w") as w:
            json.dump(sender_data, w)

        with open("Data/Users/"+self.username+"/Accounts/"+receiver+".json", "w") as w:
            json.dump(receiver_data, w)

        self._updt_error_label(f"{amount}€ sent from {sender} to {receiver}")
        self._receiver_changed()
        self._sender_changed()

    def _init_labels(self):
        sender = QtWidgets.QLabel(self)
        sender.setText("Sender")
        sender.setStyleSheet("font-size: 15px;")
        sender.adjustSize()
        sender.move(self.sender_c_box.x()+self.sender_c_box.width()//2-sender.width()//2, self.sender_c_box.y()-20)

        receiver = QtWidgets.QLabel(self)
        receiver.setText("Receiver")
        receiver.setStyleSheet("font-size: 15px;")
        receiver.adjustSize()
        receiver.move(self.receiver_c_box.x()+self.receiver_c_box.width()//2-receiver.width()//2, self.receiver_c_box.y()-20)

        self.sender_bal = QtWidgets.QLabel(self)
        self.sender_bal.setText(f"Balance: {self._get_bal(self.sender_c_box.currentText())}")
        self.sender_bal.setStyleSheet("font-size: 15px;")
        self.sender_bal.adjustSize()
        self.sender_bal.move(self.sender_c_box.x()+self.sender_c_box.width()//2-self.sender_bal.width()//2, self.sender_c_box.y()+self.sender_c_box.height()+15)

        self.receiver_bal = QtWidgets.QLabel(self)
        self.receiver_bal.setText(f"Balance: {self._get_bal(self.receiver_c_box.currentText())}")
        self.receiver_bal.setStyleSheet("font-size: 15px;")
        self.receiver_bal.adjustSize()
        self.receiver_bal.move(self.receiver_c_box.x()+self.receiver_c_box.width()//2-self.receiver_bal.width()//2, self.receiver_c_box.y()+self.receiver_c_box.height()+15)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.amount_box.x()+self.amount_box.width()//2-self.error_label.width()//2, self.amount_box.y()+self.amount_box.height()+15)

class AccountsCreation(QMainWindow):
    def __init__(self, username, whole_data):
        self.username = username
        self.whole_data = whole_data

        self.button_w, self.button_h = 130, 30
        self.boxes_w, self.boxes_h = 240, 30

        self.acc_data = self.get_acc_data()

        super().__init__()

        self.setFixedSize(350, 400)
        self.setWindowTitle(f"{self.username}'s Creation Page")
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_buttons()
        self._init_boxes()
        self._init_labels()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hide_error)
        self.timer.setSingleShot(True)
        self.time = 3.5

    def hide_error(self):
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, 200)

    def _updt_error_label(self, error):
        self.error_label.setText(error)
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, 200)
        self.timer.start(int(self.time*1000))

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def get_acc_data(self):
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "r") as r:
            return json.load(r)

    def _back_pressed(self):
        self.account = Accounts(self.username, self.get_acc_data(), self.whole_data)
        self.account.show()
        self.hide()

    def _init_labels(self):
        self.balance_label = QtWidgets.QLabel(self)
        self.balance_label.setText(f"Main Account Balance: "+str(self.acc_data.get("Balance")))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, 50)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("")
        self.error_label.adjustSize()
        self.error_label.move(self.width()//2-self.error_label.width()//2, 200)

    def _init_boxes(self):
        self.name_box = QtWidgets.QLineEdit(self)
        self.name_box.setPlaceholderText("Account Name")
        self.name_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.name_box.move(self.width()//2-self.name_box.width()//2, 100)

        self.amount_tr_box = QtWidgets.QLineEdit(self)
        self.amount_tr_box.setPlaceholderText("Transfert Amount")
        self.amount_tr_box.setFixedSize(self.boxes_w, self.boxes_h)
        self.amount_tr_box.move(self.width()//2-self.amount_tr_box.width()//2, 150)

    def _init_buttons(self):
        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setText("Create Account")
        self.submit_button.setFixedSize(self.button_w+40, self.button_h)
        self.submit_button.move(self.width()//2-self.submit_button.width()//2, self.height()-self.submit_button.height()-70)
        self.submit_button.pressed.connect(self._submit_pressed)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-self.back_button.height()-20)
        self.back_button.pressed.connect(self._back_pressed)

    def _get_acc_names(self):
        name = []
        for file in os.listdir("Data/Users/"+self.username+"/Accounts"):
            name.append(file.lower())
        return name

    def _submit_pressed(self):
        if self.name_box.text() == "":
            self._updt_error_label("Account name cant be empty!")
            return
        elif self.name_box.text().lower()+".json" in self._get_acc_names():
            self._updt_error_label(f"You already have an account named \"{self.name_box.text()}\"")
            return
        
        try:
            amount = int(self.amount_tr_box.text())
            if amount > self.get_acc_data().get("Balance"):
                self._updt_error_label("Amount superior than your balance..")
                return
            if amount < 0:
                self._updt_error_label("Amount cant be negative!")
                return
        except:
            self._updt_error_label("Invalid amount number!")
            return
        self.create_file(self.name_box.text(), amount)
        self._updt_bal()

    def _updt_bal(self):
        self.balance_label.setText(f"Main Account Balance: "+str(self.acc_data.get("Balance")))
        self.balance_label.adjustSize()
        self.balance_label.move(self.width()//2-self.balance_label.width()//2, 50)
        
    def create_file(self, name, bal):
        id = get_rnd_acc_number()
        with open("Data/Users/"+self.username+"/Accounts/"+name+".json", "w") as w:
           json.dump({"Name": name, "Account-Number": id, "Balance": float(bal)}, w)
        self.name_box.setText("")
        self.amount_tr_box.setText("")
        self._updt_error_label("Account succesfully created!")

        with open("Data/Users/"+self.username+"/Accounts/ids.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

        with open("Data/Users/"+self.username+"/Accounts/ids.csv", "w", newline='') as w:
           writer = csv.writer(w)
           for row in data:
               writer.writerow(row)
           writer.writerow([str(id), name])

        self._rmv_bal(bal)

    def _rmv_bal(self, amount):
        self.acc_data["Balance"] = self.acc_data["Balance"]-amount
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "w") as w:
           json.dump({"Name": "Main", "Account-Number": self.acc_data["Account-Number"], "Balance": self.acc_data["Balance"]}, w)

class AccountsLoan(QMainWindow):
    def __init__(self, username, whole_data):
        self.username = username
        self.whole_data = whole_data

        self.button_w, self.button_h = 130, 30

        super().__init__()

        self.setFixedSize(700, 400)
        self.setWindowTitle(f"{self.username}'s Loan page")
        self.setWindowIcon(QIcon('GUI/KnoxBank.jpeg'))
        self.center()

        self._init_buttons()

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft().x(), window_geometry.topLeft().y()-30)

    def get_acc_data(self):
        with open("Data/Users/"+self.username+"/Accounts/Main.json", "r") as r:
            return json.load(r)

    def _back_pressed(self):
        self.account = Accounts(self.username, self.get_acc_data(), self.whole_data)
        self.account.show()
        self.hide()

    def _init_buttons(self):
        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setFixedSize(self.button_w, self.button_h)
        self.back_button.move(self.width()//2-self.back_button.width()//2, self.height()-self.back_button.height()-20)
        self.back_button.pressed.connect(self._back_pressed)

def window():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('GUI/KnoxBank.ico'))
    window1 = MainWindow()
    window1.show()
    sys.exit(app.exec_())

window()