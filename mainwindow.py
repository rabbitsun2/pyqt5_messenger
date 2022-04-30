# Subject: PyQt5 버튼 예제
# Author: 정도윤(Doyun Jung)
# Created Date: 2022-04-07
# Description:

import queue
import sys
import threading
import pymysql
import senderdialog as SenderDialogFrm
import recvdialog as RecvDialogFrm
import sentnotedialog as SentnoteDialogFrm
import chatroomdialog as ChatroomDialogFrm
from dbms import dbms
from model import model
from service import service

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore

form_mainwindow = uic.loadUiType("mainWindow.ui")[0]

class MainWindow(QDialog, QWidget, form_mainwindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #self.initUI()

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn
        print(self.getConn().getConnection())

    def getMyMember(self):
        return self.member

    def setMyMember(self, member):
        self.member = member

    def initUI(self):

        self.btn_home.clicked.connect(self.action_clicked_btn_home_open)
        self.btn_user_sync.clicked.connect(self.action_clicked_btn_user_sync)
        self.btn_participate.clicked.connect(self.action_clicked_btn_participate)
        self.btn_user_realtime_sync.clicked.connect(self.action_clicked_btn_user_realtime_sync)
        self.btn_recv_view.clicked.connect(self.action_clicked_btn_recv_view)
        self.btn_send_view.clicked.connect(self.action_clicked_btn_send_view)
        self.btn_participate_chat.clicked.connect(self.action_clicked_btn_participate_chat)

        self.friendWidget.clicked.connect(self.action_clicked_friendWidget)

        # 상대 목록 초기화
        self.friend_list_init()

        # 실시간 동기화 버튼 토글
        self.toggle_realtime_sync = 0

        # 쪽지 존재여부
        self.statusMessage.setText("초기")
        self.statusMessage.setStyleSheet("QLineEdit"
                            "{"
                                "background : #ff8c00;"
                            "}")


    def action_clicked_btn_participate(self):
        lst_model_index = self.friendWidget.selectedIndexes()
        lst_item = self.friendWidget.selectedItems()

        select_row = -1
        select_item = ""

#        print("아이템1:")
#        print(lst_model_index)
#        print("/아이템2:")
#        print(lst_item)

        # row()값 찾기
        for modelRow in lst_model_index:
            select_row = modelRow.row()

        # item값 찾기
        for item in lst_item:
            select_item = item.text()

        if select_row == -1:
            QMessageBox.information(self, '알림', '대화 상대를 선택 후 사용하세요.')
        else:
            target_nickname = select_item[0:select_item.find("/")]
            target_email = select_item[select_item.find("/") + 1 : ]

            print(target_email)
            print("/")
            print(target_nickname)

            recvFriend = model.CakeonMember()
            recvFriend.setEmail(target_email)
            recvFriend.setNickname(target_nickname)

#            self.hide()
            senderFrm = SenderDialogFrm.SenderDialog()
            senderFrm.setConn(self.conn)
            senderFrm.setMyMember(self.getMyMember())
            senderFrm.setRecvMember(recvFriend)
            senderFrm.updateUI()
            senderFrm.exec_()


#            self.show()

    def action_clicked_friendWidget(self):
        lst_model_index = self.friendWidget.selectedIndexes()
        lst_item = self.friendWidget.selectedItems()

        my_member = self.getMyMember()
        select_row = -1
        select_item = ""

        # 선택된 열 정보
        for modelRow in lst_model_index:
            print(modelRow.row())
            select_row = modelRow.row()

        # 선택된 아이템 정보
        for item in lst_item:
            print(item.text())
            select_item = item.text()

        # 비교
        if select_row != -1 and select_item == my_member.getNickname():
            QMessageBox.information(self, '알림', '자기 자신은 채팅 상대가 될 수 없습니다.')


    def action_clicked_btn_home_open(self):
        self.close()    # 창 닫기

    # 동기화 클릭 동작
    def action_clicked_btn_user_sync(self):
        self.friendWidget.clear()
        self.friend_list_init()

    def action_clicked_btn_second(self):
        window = RecvDialogFrm.RecvDialog()
        window.setConn(self.getConn())
        window.setRecvMember(self.getMyMember())
        window.updateUI()
        window.show()
        window.exec_()


    def action_clicked_btn_user_realtime_sync(self):

        if self.toggle_realtime_sync == 0:
            self.btn_user_realtime_sync.setText("실시간 끄기")
            self.toggle_realtime_sync = 1
            self.startMessageTimer()
        else:
            self.btn_user_realtime_sync.setText("실시간 켜기")
            self.toggle_realtime_sync = 0
            self.timer.cancel()

    def action_clicked_btn_participate_chat(self):

        print("")
        chatRoomFrm = ChatroomDialogFrm.ChatRoomDialog()
        chatRoomFrm.setConn(self.getConn())
        chatRoomFrm.exec_()

    def startMessageTimer(self):

        if self.toggle_realtime_sync == 1:
            print("Timer")

            # 실행 영역
            # 메시지 모델
            messagebox = model.Message()

            # 서비스
            messengerService = service.MessengerService()
            messengerService.setConn(self.getConn())
            memberService = service.MemberService()
            memberService.setConn(self.getConn())

            # 받는 사람
            recvMember = self.getMyMember()
    #            print(recvMember.getEmail())
            recvMember = memberService.selectMember(recvMember)

            if recvMember is not None:
                messagebox.setRecv_id(recvMember[0])

    #       print(messagebox.getRecv_id())
            data = messengerService.selectRecvIdMessage(messagebox)

            # 보낸 쪽지함 - 동기화
            self.send_messagebox_sync()

            # 메시지가 존재할 때
            if data is not None:

    #                    print(messagebox.getId())
                self.statusMessage.setText("쪽지 있음")
                self.statusMessage.setStyleSheet("QLineEdit"
                                    "{"
                                        "background : #00FF00;"
                                    "}")

                # 쪽지 가져오기
                self.recv_message_list_init()

            else:
                self.statusMessage.setText("쪽지 없음")
                self.statusMessage.setStyleSheet("QLineEdit"
                                    "{"
                                        "background : lightblue;"
                                    "}")


            self.timer = threading.Timer(5, self.startMessageTimer)
            self.timer.start()

        else:
            print("")
            self.statusMessage.setStyleSheet("QLineEdit"
                                "{"
                                    "background : lightblue;"
                                "}")



    def send_messagebox_sync(self):
        print("")

        # 초기화
        self.sendMessageWidget.clear()

        self.conn = self.getConn()
        db = self.conn.getConnection()

        # 서비스
        memberService = service.MemberService()
        memberService.setConn(self.getConn())

        # 받는 사람
        recvMember = self.getMyMember()
#            print(recvMember.getEmail())
        recvMember = memberService.selectMember(recvMember)

        cursor = db.cursor()
        sql = """SELECT cakeon_messenger_sms.id, cakeon_member.email, cakeon_member.nickname,
        cakeon_member.regidate, cakeon_messenger_sms.sender_id, cakeon_messenger_sms.recv_id,
        cakeon_messenger_sms.message, cakeon_messenger_sms.first_read, cakeon_messenger_sms.regidate
        from cakeon_messenger_sms, cakeon_member WHERE sender_id = %s
        and cakeon_messenger_sms.sender_remove = %s
        and cakeon_member.id = cakeon_messenger_sms.sender_id order by cakeon_messenger_sms.id desc
              """

        cursor.execute(sql, (recvMember[0], 0))
        result = cursor.fetchall()

        # 결과값이 존재할 때
        if result is not None:

            # 분류
            for data in result:

                if data[7] == 0:
                    note_icon = QIcon('note_icon.jpg')
                    icon_item = QListWidgetItem(note_icon, '[{}]{}/{} - {}'.format(data[0], data[2], data[1], data[6]))
                    self.sendMessageWidget.addItem(icon_item)
                    regidate_icon = QIcon('regidate_icon.jpg')
                    icon_item = QListWidgetItem(regidate_icon, '{}'.format(data[8]))
                    self.sendMessageWidget.addItem(icon_item)

                elif data[7] == 1:
                    note_read_icon = QIcon('note_icon.jpg')
                    icon_item = QListWidgetItem(note_read_icon, '[{}]{}/{} - {}'.format(data[0], data[2], data[1], data[6]))
                    self.sendMessageWidget.addItem(icon_item)
                    regidate_icon = QIcon('regidate_icon.jpg')
                    icon_item = QListWidgetItem(regidate_icon, '{}'.format(data[8]))
                    self.sendMessageWidget.addItem(icon_item)

        db.commit()
        db.close()

    def action_clicked_btn_recv_view(self):

        lst_model_index = self.recvMessageWidget.selectedIndexes()
        lst_item = self.recvMessageWidget.selectedItems()

        select_row = -1
        select_item = ""

        data = None

        # row()값 찾기
        for modelRow in lst_model_index:
            select_row = modelRow.row()

        # item값 찾기
        for item in lst_item:
            select_item = item.text()

        if select_row == -1:
            QMessageBox.information(self, '알림', '대화 상대를 선택 후 사용하세요.')
        else:

            # 메시지 모델
            messagebox = model.Message()

            # 서비스
            messengerService = service.MessengerService()
            messengerService.setConn(self.getConn())
            memberService = service.MemberService()
            memberService.setConn(self.getConn())

            message_id = select_item[1:select_item.find("]")]

            # message_id 찾기
            if message_id.find(":") == -1:
                #print(message_id)
                messagebox.setId(message_id)
                data = messengerService.selectIdMessage(messagebox)
            else:
                message_id = -1



            # 메시지가 존재할 때
            if data is not None:

                # 새 메시지 생성
                messagebox = model.Message()

                messagebox.setId(data[0])
                messagebox.setSender_id(data[1])
                messagebox.setRecv_id(data[2])
                messagebox.setMessage(data[3])
                messagebox.setSender_remove(data[4])
                messagebox.setRecv_remove(data[5])
                messagebox.setFirst_read(data[6])
                messagebox.setRegidate(data[7])

                # 보낸 사람 생성
                tmp = memberService.selectIdMember(messagebox.getSender_id())
                senderMember = model.CakeonMember()
                senderMember.setId(tmp[0])
                senderMember.setEmail(tmp[1])
                senderMember.setPasswd(tmp[2])
                senderMember.setNickname(tmp[3])
                senderMember.setRegidate(tmp[4])

                # 받은 쪽지 - 폼 초기화
                recvFrm = RecvDialogFrm.RecvDialog()
                recvFrm.setConn(self.conn)
                recvFrm.setSenderMember(senderMember)
                recvFrm.setRecvMember(self.getMyMember())
                recvFrm.setMessageBox(messagebox)
                recvFrm.updateUI()

                recvFrm.exec_()

                # 읽음 - 표시하기
                messengerService.updateFirstRead(messagebox)

    def action_clicked_btn_send_view(self):

        print("")

        # 선택 항목
        lst_model_index = self.sendMessageWidget.selectedIndexes()
        lst_item = self.sendMessageWidget.selectedItems()

        select_row = -1
        select_item = ""

        data = None

        # row()값 찾기
        for modelRow in lst_model_index:
            select_row = modelRow.row()

        # item값 찾기
        for item in lst_item:
            select_item = item.text()

        if select_row == -1:
            QMessageBox.information(self, '알림', '대화 상대를 선택 후 사용하세요.')
        else:

            # 메시지 모델
            messagebox = model.Message()

            # 서비스
            messengerService = service.MessengerService()
            messengerService.setConn(self.getConn())
            memberService = service.MemberService()
            memberService.setConn(self.getConn())

            message_id = select_item[1:select_item.find("]")]

            # message_id 찾기
            if message_id.find(":") == -1:
                #print(message_id)
                messagebox.setId(message_id)
                data = messengerService.selectIdMessage(messagebox)
            else:
                message_id = -1



            # 메시지가 존재할 때
            if data is not None:

                # 새 메시지 생성
                messagebox = model.Message()

                messagebox.setId(data[0])
                messagebox.setSender_id(data[1])
                messagebox.setRecv_id(data[2])
                messagebox.setMessage(data[3])
                messagebox.setSender_remove(data[4])
                messagebox.setRecv_remove(data[5])
                messagebox.setFirst_read(data[6])
                messagebox.setRegidate(data[7])

                # 보낸 사람 생성
                tmp = memberService.selectIdMember(messagebox.getSender_id())
                senderMember = model.CakeonMember()
                senderMember.setId(tmp[0])
                senderMember.setEmail(tmp[1])
                senderMember.setPasswd(tmp[2])
                senderMember.setNickname(tmp[3])
                senderMember.setRegidate(tmp[4])

                # 받은 쪽지 - 폼 초기화
                sentnoteFrm = SentnoteDialogFrm.SentnoteDialog()
                sentnoteFrm.setConn(self.conn)
                sentnoteFrm.setSenderMember(senderMember)
                sentnoteFrm.setRecvMember(self.getMyMember())
                sentnoteFrm.setMessageBox(messagebox)
                sentnoteFrm.updateUI()

                sentnoteFrm.exec_()


    def friend_list_init(self):

        self.conn = self.getConn()
        db = self.conn.getConnection()

        cursor = db.cursor()
        sql = """SELECT cakeon_member.id, cakeon_member.email, cakeon_member.nickname, cakeon_member_messenger.`status`,
               cakeon_member_messenger.locked FROM cakeon_member, cakeon_member_messenger
               WHERE cakeon_member.id = cakeon_member_messenger.member_id order by cakeon_member.id
              """

        cursor.execute(sql)
        result = cursor.fetchall()

        # 결과값이 존재할 때
        if result is not None:

            # 분류
            for data in result:

                if data[3] == 0:
                    out_of_office_icon = QIcon('out_of_office.jpg')
                    icon_item = QListWidgetItem(out_of_office_icon, '{}/{}'.format(data[2], data[1]))
                    self.friendWidget.addItem(icon_item)
                elif data[3] == 1:
                    com_in_icon = QIcon('com_in.jpg')
                    icon_item = QListWidgetItem(com_in_icon, '{}/{}'.format(data[2], data[1]))
                    self.friendWidget.addItem(icon_item)


        db.commit()
        db.close()

    def recv_message_list_init(self):
        print("")

        self.recvMessageWidget.clear()

        self.conn = self.getConn()
        db = self.conn.getConnection()

        # 서비스
        memberService = service.MemberService()
        memberService.setConn(self.getConn())

        # 받는 사람
        recvMember = self.getMyMember()
#            print(recvMember.getEmail())
        recvMember = memberService.selectMember(recvMember)

        cursor = db.cursor()
        sql = """SELECT cakeon_messenger_sms.id, cakeon_member.email, cakeon_member.nickname,
            cakeon_member.regidate, cakeon_messenger_sms.sender_id, cakeon_messenger_sms.recv_id,
            cakeon_messenger_sms.message, cakeon_messenger_sms.first_read, cakeon_messenger_sms.regidate
            from cakeon_messenger_sms, cakeon_member WHERE recv_id = %s
            and cakeon_messenger_sms.recv_remove = %s
            and cakeon_member.id = cakeon_messenger_sms.sender_id order by cakeon_messenger_sms.id desc
              """

        cursor.execute(sql, (recvMember[0], 0))
        result = cursor.fetchall()

        # 결과값이 존재할 때
        if result is not None:

            # 분류
            for data in result:

                if data[7] == 0:
                    note_icon = QIcon('note_icon.jpg')
                    icon_item = QListWidgetItem(note_icon, '[{}]{}/{} - {}'.format(data[0], data[2], data[1], data[6]))
                    self.recvMessageWidget.addItem(icon_item)
                    regidate_icon = QIcon('regidate_icon.jpg')
                    icon_item = QListWidgetItem(regidate_icon, '{}'.format(data[8]))
                    self.recvMessageWidget.addItem(icon_item)

                elif data[7] == 1:
                    note_read_icon = QIcon('note_read_icon.jpg')
                    icon_item = QListWidgetItem(note_read_icon, '[{}]{}/{} - {}'.format(data[0], data[2], data[1], data[6]))
                    self.recvMessageWidget.addItem(icon_item)
                    regidate_icon = QIcon('regidate_icon.jpg')
                    icon_item = QListWidgetItem(regidate_icon, '{}'.format(data[8]))
                    self.recvMessageWidget.addItem(icon_item)

        db.commit()
        db.close()

def hello():
    print("반갑다.")
