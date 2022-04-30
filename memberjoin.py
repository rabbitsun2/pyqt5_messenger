# Subject: PyQt5 버튼 예제
# Author: 정도윤(Doyun Jung)
# Created Date: 2022-04-07
# Description:

import re
import sys
from dbms import dbms
from model import model
from service import service
import pymysql
import datetime
import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore

form_memberjoin = uic.loadUiType("memberJoin.ui")[0]

class MemberJoin(QDialog, QWidget, form_memberjoin):

    def __init__(self):
        super(MemberJoin, self).__init__()
        self.setupUi(self)
        self.initUI()

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn
        print(self.getConn().getConnection())

    def initUI(self):
        self.btn_home.clicked.connect(self.action_clicked_btn_home_open)
        self.btn_Submit.clicked.connect(self.action_clicked_btn_submit)
        self.btn_emailDuplicateChk.clicked.connect(self.action_clicked_btn_email_DuplicateChk)

        # 초기 임시값
        self.txt_Email.setText("asdf@asdf.com")
        self.txt_Passwd1.setText("1234")
        self.txt_Passwd2.setText("1234")
        self.txt_usrName.setText("홍길동")
        self.txt_Nickname.setText("닉네임")

        # 버그 개선
        self.cnt = 0

    def action_clicked_btn_home_open(self):
        self.close()    # 창 닫기

    def action_clicked_btn_email_DuplicateChk(self):

        # 상태
        status = 1

        memberService = service.MemberService()
        memberService.setConn(self.getConn())

        email = self.txt_Email.text()

        self.member = model.CakeonMember()
        self.member.setEmail(email)

        # 이메일 정규식 검사
        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if status == 1 and p.match(email) != None:
            status = 1
        else:
            status = 2

        # 이메일 중복 여부
        if status == 1 and memberService.selectMember(self.member) == None:
            status = 1
        elif status == 1 and memberService.selectMember(self.member) != None:
            status = 3

        print("헬로1: {}".format( status))

        if self.cnt == 0:

            # 알림 메시지
            if status == 1:
                QMessageBox.information(self, '알림', '사용 가능합니다.')
            elif status == 2:
                QMessageBox.information(self, '알림', '이메일 형식이 일치하지 않습니다.')
            elif status == 3:
                QMessageBox.information(self, '알림', '이메일이 중복되었습니다.')

        # 버그 개선
        self.bug_fixed()


    def action_clicked_btn_submit(self):

        if self.cnt == 0:

            # 상태
            status = 1

            memberService = service.MemberService()
            memberService.setConn(self.getConn())

            email = self.txt_Email.text()
            passwd1 = self.txt_Passwd1.text()
            passwd2 = self.txt_Passwd2.text()
            usrname = self.txt_usrName.text()
            birthdate = self.date_Birthdate.text()
            nickname = self.txt_Nickname.text()


            # 현재 시간
            now = datetime.datetime.now()
            todaytime = now.strftime('%Y-%m-%d %H:%M:%S')

            self.member = model.CakeonMember()
            self.member.setEmail(email)
            self.member.setPasswd(passwd1)
            self.member.setNickname(nickname)
            self.member.setRegidate(todaytime)

            # 이메일 정규식 검사
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if status == 1 and p.match(email) != None:
                status = 1
            else:
                status = 2

    #        print("헬로1: {}".format( status))

            # 이메일 중복 여부
            if status == 1 and memberService.selectMember(self.member) == None:
                status = 1
            elif status == 1 and memberService.selectMember(self.member) != None:
                status = 3

    #        print("헬로2: {} {}".format(email, status))

            # 비밀번호가 같은지 판단
            if status == 1 and passwd1 != passwd2:
                status = 4
            elif status == 1 and passwd1 == passwd2:
                status = 1

    #        print("헬로3: {}".format( status))

            # 비밀번호 길이 판단
            if status == 1 and len(passwd1) >= 4:
                passwd_enc = hashlib.sha256(passwd1.encode())
                passwd_enc = passwd_enc.hexdigest()
                self.member.setPasswd(passwd_enc)

                status = 1

            elif status == 1 and len(passwd1) < 4:
                status = 5


    #        print("헬로4: {}".format( status))

            # 이름 작성 여부
            if status == 1 and len(usrname) >= 3:
                status = 1
            elif status == 1 and len(usrname) < 3:
                status = 6

            print("헬로5: {}".format( status ))

            # 닉네임 작성 여부
            if status == 1 and len(nickname) >= 3:
                status = 1
            elif status == 1 and len(nickname) < 3:
                status = 7

            print("헬로6: {}".format( status ))

            if status == 1:
                memberService.insertMember(self.member)
                QMessageBox.information(self, '알림', '회원가입이 완료되었습니다.')

        # 버그 개선
        self.bug_fixed()


    def bug_fixed(self):
        self.cnt = self.cnt + 1

        if self.cnt == 2:
            self.cnt = 0


def hello():
    print("반갑다.")
