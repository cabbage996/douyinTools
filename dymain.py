import json
import sys

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from dyvideoUI import Ui_MainWindow
from getid import get_douyin_id

# PySide6-uic demo.ui -o ui_demo.py
# from ui_demo import Ui_Demo
#打包程序：pyinstaller -D dymain.py -w -i tiktok.ico -n 抖音UID一键查

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.handle_init()  #结果面板初始化
        
        self.band()
    
    def band(self):
      self.ui.pushButton.clicked.connect(self.handle_click)


    def handle_click(self):
      videoid=self.ui.lineEdit.text()
      if videoid=="":
        #空值处理
        self.handle_init()
        return     
      #新增多线程处理
      self.thread_getdata=GetDataHandleThread()
      self.thread_getdata.videoid=videoid
      self.thread_getdata.signal.connect(self.handle_result)
      self.thread_getdata.start()
      self.thread_getdata.exec() #防止连续点击按钮造成程序崩溃
      # author=get_douyin_id(videoid)
      
      
    

    #结果界面初始化函数
    def handle_init(self):
      self.ui.uid.setText('')
      self.ui.shortid.setText('')
      self.ui.nickname.setText('')

    #处理结果
    def handle_result(self,author):
      author=json.loads(author)
      if not author:
        self.handle_err()
        return
      self.handle_success(author=author)




    #结果界面报错函数
    def handle_err(self):
      self.ui.uid.setText('您输入的视频ID不存在!')
      self.ui.shortid.setText(" ")
      self.ui.nickname.setText(" ") 

    def handle_success(self,author):
      uid=author['uid']
      shortid=author['short_id']
      nickname=author['nickname']
      uniqueid=author['unique_id']
      #print(uniqueid)
      #更改样式
      self.ui.uid.setText('抖音ID:'+uid)
      #如果uniqueid存在，抖音号就是uniqueid,否则就是short_id
      if not uniqueid:
        self.ui.shortid.setText('抖音号:'+shortid)
      else:
        self.ui.shortid.setText('抖音号:'+uniqueid)
      self.ui.nickname.setText('抖音昵称:'+nickname)
      self.ui.uid.setTextInteractionFlags(Qt.TextSelectableByMouse)
      self.ui.shortid.setTextInteractionFlags(Qt.TextSelectableByMouse)
      self.ui.nickname.setTextInteractionFlags(Qt.TextSelectableByMouse)

 #使用多线程处理后台数据     
class GetDataHandleThread(QThread):
  #子线程发送信号
  signal=Signal(str)
  def __init__(self):
    super().__init__()
    self.videoid=''
  
  def run(self):
    #处理后台数据
    author=get_douyin_id(self.videoid)
    self.signal.emit(json.dumps(author))   #发送获取数据信号
    




if __name__ == '__main__':
    app = QApplication(sys.argv)  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    window.setWindowTitle('抖音uid查询工具v1.0')
    sys.exit(app.exec()) # 避免程序执行到这一行后直接退出
