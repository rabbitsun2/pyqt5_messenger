# This Python file uses the following encoding: utf-8


class CakeonMember:
    def __init__(self):
        pass

    def getId(self):
        return self.id

    def getEmail(self):
        return self.email

    def getPasswd(self):
        return self.passwd

    def getNickname(self):
        return self.nickname

    def getRegidate(self):
        return self.regidate

    def setId(self, id):
        self.id = id

    def setEmail(self, email):
        self.email = email

    def setPasswd(self, passwd):
        self.passwd = passwd

    def setNickname(self, nickname):
        self.nickname = nickname

    def setRegidate(self, regidate):
        self.regidate = regidate

class Message:
    def __init__(self):
        pass

    def getId(self):
        return self.id

    def getSender_id(self):
        return self.sender_id

    def getRecv_id(self):
        return self.recv_id

    def getMessage(self):
        return self.message

    def getSender_remove(self):
        return self.sender_remove

    def getRecv_remove(self):
        return self.recv_remove

    def getFirst_read(self):
        return self.firstread

    def getRegidate(self):
        return self.regidate

    def setId(self, id):
        self.id = id

    def setSender_id(self, id):
        self.sender_id = id

    def setRecv_id(self, id):
        self.recv_id = id

    def setMessage(self, message):
        self.message = message

    def setSender_remove(self, sender_remove):
        self.sender_remove = sender_remove

    def setRecv_remove(self, recv_remove):
        self.recv_remove = recv_remove

    def setFirst_read(self, firstread):
        self.firstread = firstread

    def setRegidate(self, regidate):
        self.regidate = regidate

class ChatRoom:
    def getId(self):
        return self.id

    def getMy_id(self):
        return self.my_id

    def getGuest_id(self):
        return self.guest_id

    def getChat_id(self):
        return self.chat_id

    def getMy_remove(self):
        return self.my_remove

    def getMessage(self):
        return self.message

    def getRegidate(self):
        return self.regidate

    def setId(self, id):
        self.id = id

    def setMy_id(self, my_id):
        self.my_id = my_id

    def setGuest_id(self, guest_id):
        self.guest_id = guest_id

    def setChat_id(self, chat_id):
        self.chat_id = chat_id

    def setMy_remove(self, my_remove):
        self.my_remove = my_remove

    def setMessage(self, message):
        self.message = message

    def setRegidate(self, regidate):
        self.regidate = regidate
