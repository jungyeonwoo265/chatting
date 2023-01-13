import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p


form_class = uic.loadUiType("chatting.ui")[0]
name = "노도현"
to = "정연우"


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='chatting', charset='utf8')
        self.c = self.conn.cursor()
        self.conn.close()

        self.message()

        self.lineEdit.returnPressed.connect(self.input)

    # 채팅 입력
    def input(self):
        text = self.lineEdit.text()
        if text:
            self.open_db()
            self.c.execute(f'insert into message values(curdate(), "{name}", "{to}", curtime(), "{text}","n")')
            self.conn.commit()
            self.conn.close()
        self.lineEdit.clear()
        self.message()

    # 채팅 내용
    def message(self):
        self.listWidget.clear()
        self.open_db()
        self.c.execute(f'select 보냄,시간,내용 from message')
        message = self.c.fetchall()
        for i in message:
            self.listWidget.addItem(f'{i[0]} / {i[1]} / {i[2]}')
        self.conn.close()

    # DB 연결
    def open_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='chatting', charset='utf8')
        self.c = self.conn.cursor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
