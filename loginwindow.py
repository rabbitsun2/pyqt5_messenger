# Subject: PyQt5 폼 to 폼 열기 예제
# Author: 정도윤(Doyun Jung)
# Created Date: 2022-04-07
# Description:

import os
import sys
import socket
import threading
from dbms import dbms
from model import model

import pymysql
import hashlib
import mainwindow as MainFrm
import memberjoin as MemberJoinFrm

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic

form_class = uic.loadUiType("loginWindow.ui")[0]

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        print("Hello")
        self.btn_login.clicked.connect(self.actionClickedLogin)
        self.btn_join.clicked.connect(self.actionClickedJoin)

        # 초기값
        self.txt_Email.setText("root@localhost")
        self.txt_Passwd.setText("1234")

        # DBMS 설정
        self.conn = dbms.Connection()
        self.conn.setConnection("10.210.150.5", "hr", "123456", "hr", 12100, 'utf8')
        #self.conn.setConnection("112.76.56.89", "hr", "123456", "hr", 12100, 'utf8')

        # 사용자 계정 정보
        self.member = model.CakeonMember()
        #print(self.member)

    def actionClickedLogin(self):

        check = 0
        #print("Hello2")

        email = self.txt_Email.text()
        passwd = self.txt_Passwd.text()
        passwd_enc = hashlib.sha256(passwd.encode())
        passwd_enc = passwd_enc.hexdigest()
        #print(email)
        print(passwd_enc)

        db = self.conn.getConnection()

#       print(self.conn.getHostname())

        cursor = db.cursor()
        sql = "select * from cakeon_member where email = %s"

        cursor.execute(sql, (email))
        result = cursor.fetchone()

        if result is not None:
            if email in result[1]:
                check = check + 1
            if passwd_enc in result[2]:
                check = check + 1
            if check == 2:
                self.member.setId(int(result[0]))
                self.member.setEmail(result[1])
                self.member.setPasswd(result[2])
                self.member.setNickname(result[3])
                self.member.setRegidate(result[4])

        db.commit()
        db.close()

        if check == 2:
            self.hide()
            self.createFrm = MainFrm.MainWindow()
            self.createFrm.setConn(self.conn)
            self.createFrm.setMyMember(self.member)
            self.createFrm.initUI()
            self.createFrm.exec_()
            self.show()
            #MainFrm.hello()

    def actionClickedJoin(self):
        print("참")
        self.hide()
        self.createFrm = MemberJoinFrm.MemberJoin()
        self.createFrm.setConn(self.conn)
        self.createFrm.initUI()
        self.createFrm.exec()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
