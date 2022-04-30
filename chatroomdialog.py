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

form_chatroomdialogwindow = uic.loadUiType("chatroomDialog.ui")[0]

class ChatRoomDialog(QDialog, QWidget, form_chatroomdialogwindow):

    def __init__(self):
        super(ChatRoomDialog, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn_home.clicked.connect(self.action_clicked_btn_home_open)

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn
        print(self.getConn().getConnection())

    def getRecvMember(self):
        return self.recv_member

    def setRecvMember(self, member):
        self.recv_member = member

    def action_clicked_btn_home_open(self):
        self.close()    # 창 닫기


