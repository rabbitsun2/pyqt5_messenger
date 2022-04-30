# This Python file uses the following encoding: utf-8

import pymysql

class MemberService:
    def __init__(self):
        pass

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn

    def selectMember(self, member):

        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_member where email = %s
                """

        cursor.execute(sql, (member.getEmail()))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
        if result is not None:
            #result = ""
            print(result[2])

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def selectIdMember(self, id):
        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_member where id = %s
                """

        cursor.execute(sql, (id))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
        if result is not None:
            #result = ""
            print(result[2])

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def insertMember(self, member):

        self.conn = self.getConn()

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 회원 등록
                sql = """INSERT INTO cakeon_member(email, passwd, nickname, regidate)
                    VALUES(%s, %s, %s, %s)
                """
                cursor.execute(sql, (member.getEmail(), member.getPasswd(), member.getNickname(), member.getRegidate()))

                # 2단계 - 회원 일련번호 가져오기
                sql = """SELECT * from cakeon_member
                        where email = %s
                        and passwd = %s
                        and nickname = %s
                        and regidate = %s
                """

                cursor.execute(sql, (member.getEmail(), member.getPasswd(), member.getNickname(), member.getRegidate()))

                # 데이터 Fetch
                result = cursor.fetchone()
                if result is not None:
                    #print(result)
                    member.setId(int(result[0]))

                # 3단계 - 메신저 값 추가하기
                sql = """INSERT INTO cakeon_member_messenger(member_id, status, locked)
                        VALUES(%s, %s, %s)
                        """
                cursor.execute(sql, (member.getId(), 0, 0))

            db.commit()

        finally:
            db.close()


class MessengerService:

    def __init__(self):
        pass

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn

    def insertMessage(self, messagebox):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """INSERT INTO cakeon_messenger_sms(sender_id, recv_id, message, sender_remove, recv_remove, first_read, regidate)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """

                print(sql)

                cursor.execute(sql, (messagebox.getSender_id(), messagebox.getRecv_id(),
                                messagebox.getMessage(), 0, 0, 0, messagebox.getRegidate()))


            db.commit()

        finally:
            db.close()

    def updateFirstRead(self, messagebox):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 업데이트
                sql = """UPDATE cakeon_messenger_sms set first_read = 1 where id = %s
                """

#                print("메시지 박스:")
#                print(messagebox.getId())

                cursor.execute(sql, (messagebox.getId()))

            db.commit()

        finally:
            db.close()


    def updateSenderRemoveMessage(self, messagebox):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """UPDATE cakeon_messenger_sms set sender_remove = %s WHERE id = %s
                """

                # print(sql)

                cursor.execute(sql, (1, messagebox.getId()))


            db.commit()

        finally:
            db.close()

    def updateRecvRemoveMessage(self, messagebox):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """UPDATE cakeon_messenger_sms set recv_remove = %s WHERE id = %s
                """

                # print(sql)

                cursor.execute(sql, (1, messagebox.getId()))

            db.commit()

        finally:
            db.close()

    def updateSendRemoveMessage(self, messagebox):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """UPDATE cakeon_messenger_sms set sender_remove = %s WHERE id = %s
                """

                # print(sql)

                cursor.execute(sql, (1, messagebox.getId()))

            db.commit()

        finally:
            db.close()

    def selectRecvIdMessage(self, messagebox):
        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_sms
                 where recv_id = %s and recv_remove = %s order by id
            """

        cursor.execute(sql, (messagebox.getRecv_id(), 0))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def selectIdMessage(self, messagebox):
        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_sms
                 where id = %s
            """

        cursor.execute(sql, (messagebox.getId()))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

class ChatService:

    def __init__(self):
        pass

    def getConn(self):
        return self.conn

    def setConn(self, conn):
        self.conn = conn

    def selectGetRoom(self, chatroom):

        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_chatroom
                 where my_id = %s and
                 guest_id = %s and
                 chat_id = %s and
                 my_remove = %s and
                 message = %s and
                 regidate = %s
            """

        cursor.execute(sql, (chatroom.getMy_id(), chatroom.getGuest_id(),
                            chatroom.getChat_id(), chatroom.getMy_remove(),
                            chatroom.getMessage(), chatroom.getRegidate()))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def selectIdRoom(self, chatroom):

        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_chatroom
                 where my_id = %s
            """

        cursor.execute(sql, (chatroom.getId()))

        # 데이터 Fetch
        result = cursor.fetchone()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def selectMyIdRoom(self, chatroom):

        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_chatroom
                 where my_id = %s and
                 my_remove = %s
            """

        cursor.execute(sql, (chatroom.getMy_id(), 0))

        # 데이터 Fetch
        result = cursor.fetchall()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def selectGuestIdRoom(self, chatroom):

        result = None

        # DB 연결
        db = self.getConn().getConnection()
        cursor = db.cursor()

        sql = """select * from cakeon_messenger_chatroom
                 where guest_id = %s and
                 my_remove = %s
            """

        cursor.execute(sql, (chatroom.getGuest_id(), 0))

        # 데이터 Fetch
        result = cursor.fetchall()

        # 데이터 가져오기
#        if result is not None:
#            result = ""
#            print(result[2])
#            for data in result:
#                print("참")
#                print(data)
#            print("Hello")

        db.commit()
        db.close()

        #print("야:{}".format(result[2]))

        return result

    def insertChatroom(self, chatroom):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """INSERT INTO cakeon_messenger_chatroom(my_id, guest_id, chat_id, my_remove, message, regidate)
                    VALUES(%s, %s, %s, %s, %s, %s)
                """

                print(sql)

                cursor.execute(sql, (chatroom.getMy_id(), chatroom.getGuest_id(),
                                chatroom.getChat_id(), chatroom.getMy_remove(),
                                chatroom.getMessage(), chatroom.getRegidate()))


            db.commit()

        finally:
            db.close()

    def updateRemoveChatroom(self, chatroom):

        # DB 연결
        db = self.conn.getConnection()

        try:
            with db.cursor() as cursor:

                # 1단계 - 메시지 등록
                sql = """UPDATE cakeon_messenger_chatroom set my_remove = %s WHERE id = %s
                """

                # print(sql)

                cursor.execute(sql, (1, chatroom.getId()))

            db.commit()

        finally:
            db.close()
