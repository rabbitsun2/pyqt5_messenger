# Subject: PyQt5 버튼 예제
# Author: 정도윤(Doyun Jung)
# Created Date: 2022-04-07
# Description:

import sys
from dbms import dbms
from service import service
from model import model
import pymysql
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore

form_senderdialogwindow = uic.loadUiType("senderDialog.ui")[0]

class SenderDialog(QDialog, QWidget, form_senderdialogwindow):

    def __init__(self):
        super(SenderDialog, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn_home.clicked.connect(self.action_clicked_btn_home_open)
        self.btn_send.clicked.connect(self.action_clicked_btn_send)

    def updateUI(self):
        recvMember = self.getRecvMember()
        self.txt_Nickname.setText(recvMember.getNickname() + "/" + recvMember.getEmail())


    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn
        print(self.getConn().getConnection())

    def getMyMember(self):
        return self.member

    def setMyMember(self, member):
        self.member = member

    def getRecvMember(self):
        return self.recvMember

    def setRecvMember(self, member):
        self.recvMember = member

    def action_clicked_btn_home_open(self):
        self.close()    # 창 닫기

    def action_clicked_btn_send(self):

        # 상태
        status = 1

        # 메시지 내용
        usrMessage = self.txt_Message.toPlainText()

        # 현재 시간
        now = datetime.datetime.now()
        todaytime = now.strftime('%Y-%m-%d %H:%M:%S')

        # 현재 메시지 모델
        messagebox = model.Message()
        messagebox.setMessage(usrMessage)
        messagebox.setRegidate(todaytime)

        # 서비스
        messengerService = service.MessengerService()
        messengerService.setConn(self.getConn())
        memberService = service.MemberService()
        memberService.setConn(self.getConn())

        # 받는 사람
        recvMember = self.getRecvMember()
#        print(recvMember.getEmail())
        recvMember = memberService.selectMember(recvMember)

        # 받은 사람 값 반영
        if recvMember is not None:
            messagebox.setRecv_id(recvMember[0])
            status = status + 1

        # 보낸 사람
        sendMember = self.getMyMember()
        print(sendMember.getEmail())
        sendMember = memberService.selectMember(sendMember)

        # 보낸 사람 값 반영
        if sendMember is not None:
            messagebox.setSender_id(sendMember[0])
            status = status + 1

#        print(sendMember[0])

        # 메시지 등록 처리
        if status == 3:
            messengerService.insertMessage(messagebox)
            QMessageBox.information(self, '알림', '성공적으로 발송이 완료되었습니다')
            self.close()


def hello():
    print("반갑다.")
