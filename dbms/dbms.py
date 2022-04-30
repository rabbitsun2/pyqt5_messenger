# This Python file uses the following encoding: utf-8

import pymysql

class Connection:
    def __init__(self):
        pass

    def setConnection(self, hostname, id, passwd, dbname, port, charset):
        self.hostname = hostname
        self.id = id
        self.passwd = passwd
        self.dbname = dbname
        self.port = port
        self.charset = charset

    def getHostname(self):
        return self.hostname

    def getId(self):
        return self.id

    def getPasswd(self):
        return self.passwd

    def getDbname(self):
        return self.dbname

    def getPort(self):
        return self.port

    def getCharset(self):
        return self.charset

    def setHostname(self, hostname):
        self.hostname = hostname

    def setId(self, id):
        self.id = id

    def setPasswd(self, passwd):
        self.passwd = passwd

    def setDbname(self, dbname):
        self.dbname = dbname

    def setPort(self, port):
        self.port = port

    def setCharset(self, charset):
        self.charset = charset

    def getConnection(self):
        db = pymysql.connect(host=self.getHostname(),
                               user=self.getId(),
                               password=self.getPasswd(),
                               db=self.getDbname(),
                               charset=self.getCharset(),
                               port=self.getPort())

        return db
