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
import senderdialog as SenderDialogFrm

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore

form_recvdialogwindow = uic.loadUiType("recvDialog.ui")[0]

class RecvDialog(QDialog, QWidget, form_recvdialogwindow):

    def __init__(self):
        super(RecvDialog, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn_home.clicked.connect(self.action_clicked_btn_home_open)
        self.btn_replyMessage.clicked.connect(self.action_clicked_btn_replyMessage)
        self.btn_remove.clicked.connect(self.action_clicked_btn_remove)

    def updateUI(self):
        sender = self.getSenderMember()
        messagebox = self.getMessageBox()
        self.txt_Nickname.setText(sender.getNickname() + "/" + sender.getEmail())
        self.txt_Message.clear()
        self.txt_Message.setPlainText(messagebox.getMessage())
        self.txt_Createdate.setReadOnly(1)
        result_datetime = messagebox.getRegidate().strftime("%Y-%m-%d %H:%M:%S")
#        print(messagebox.getRegidate())

        self.txt_Createdate.setText(result_datetime)

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn
        print(self.getConn().getConnection())

    def getRecvMember(self):
        return self.recv_member

    def setRecvMember(self, member):
        self.recv_member = member

    def getSenderMember(self):
        return self.sender_member

    def setSenderMember(self, member):
        self.sender_member = member

    def getMessageBox(self):
        return self.messagebox

    def setMessageBox(self, messagebox):
        self.messagebox = messagebox

    def action_clicked_btn_home_open(self):
        self.close()    # 창 닫기

    def action_clicked_btn_replyMessage(self):

        select_item = self.txt_Nickname.text()

        target_nickname = select_item[0:select_item.find("/")]
        target_email = select_item[select_item.find("/") + 1:]

        print(target_email)
        print("/")
        print(target_nickname)

        sendFriend = model.CakeonMember()
        sendFriend.setEmail(target_email)
        sendFriend.setNickname(target_nickname)

        self.senderFrm = SenderDialogFrm.SenderDialog()
        self.senderFrm.setConn(self.conn)
        self.senderFrm.setMyMember(self.getRecvMember())
        self.senderFrm.setRecvMember(sendFriend)
        self.senderFrm.updateUI()
        self.senderFrm.exec_()
        print("참")

    def action_clicked_btn_remove(self):

        messagebox = self.getMessageBox()
#        print(messagebox.getId())

        reply = QMessageBox.question(self, '알림', '받은 편지함에서 쪽지를 삭제하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 메시지 모델
            messagebox = self.getMessageBox()

            # 서비스
            messengerService = service.MessengerService()
            messengerService.setConn(self.getConn())
            memberService = service.MemberService()
            memberService.setConn(self.getConn())

#            print(messagebox.getId())

            # 메시지 박스 삭제처리
            messengerService.updateRecvRemoveMessage(messagebox)

            # 완료 메시지
            QMessageBox.information(self, '알림', '쪽지가 삭제되었습니다.')
            self.close()

        else:
            #event.ignore()
            print("참")


