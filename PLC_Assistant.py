# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QLineEdit,QGridLayout,QComboBox,QHBoxLayout,QTextBrowser
from PyQt5.QtGui import QIcon
import sys
import snap7
from snap7.util import *
from snap7.snap7types import *
import re_rc





global IP ,JJ,CC
IP='192.168.0.1'
JJ =0
CC =1

areas = {
  'I': 0x81,  #input 输入区
  'Q': 0x82,  #output 输出区
  'M': 0x83,  #bit memory 中间存储区（M区）
  'DB': 0x84,  #DB区
  'CT': 0x1C,  #counters
  'TM': 0x1D,  #Timers
}




class PLC(snap7.client.Client):
    def __init__(self):
        super(PLC,self).__init__()
    def tongxin(self,IP,JJ,CC):
        try:
            self.connect(IP,rack=JJ,slot=CC)  # 建立连接（相关信息去TIA看，IP，机架和插槽）
            if (self.get_connected() == True):
                print('通信成功')
                info='正常'
        except :
            print('通信失败' )
            info = '通信断开'

        return (info)




class PLC_Assiastant(QWidget):
    def __init__(self):
        super(PLC_Assiastant, self).__init__()
        #实例化一个PLC类
        self.myplc=PLC()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('西门子PLC助手')
        self.setWindowIcon(QIcon(':/1/aigei_com.png'))


        #self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        a=500*self.height/1920
        b=350*self.height/1080
        self.resize(a, b)
        self.setFixedSize(2*a, b)
        # self.setMinimumSize=(500, 350)
        # self.setMaximumSize(500, 350)
        #左侧PLC通信部份布局

        self.Label_1 = QLabel()
        self.Label_2 = QLabel()
        self.Label_3 = QLabel()
        self.Label_PIC = QLabel()

        self.Button_1 = QPushButton()
        self.Button_2 = QPushButton()

        self.Text1 = QLineEdit()
        self.Text2 = QLineEdit()
        self.Text3 = QLineEdit()

        self.Label_1.setText('PLC地址：')
        self.Label_2.setText('机架号：')
        self.Label_3.setText('插槽号：')
        self.Label_PIC.setStyleSheet('image:url(:/1/wechat.png)')

        self.Text1.setText('192.168.0.1')
        self.Text2.setText('0')
        self.Text3.setText('0')
        self.Button_1.setText('连接PLC')
        self.Button_2.setText('断开PLC')

        self.VBOX1 = QGridLayout()
        #VBOX1.setContentsMargins(0,30,150,150)
        self.VBOX1.addWidget(self.Label_1,1,1,1,1)
        self.VBOX1.addWidget(self.Text1,1,2,1,7)
        self.VBOX1.addWidget(self.Label_2,2,1,1,1)
        self.VBOX1.addWidget(self.Text2, 2, 2, 1, 2)
        self.VBOX1.addWidget(self.Label_3,3,1,1,1)
        self.VBOX1.addWidget(self.Text3, 3, 2, 1, 2)
        self.VBOX1.addWidget(self.Button_1,4,1,1,3)
        self.VBOX1.addWidget(self.Button_2,5,1,1,3)
        self.VBOX1.addWidget(self.Label_PIC,6,1,1,7)



        # 右侧数据读写布局

        self.Label_4 = QLabel()
        self.Label_5 = QLabel()

        self.Text4 = QLineEdit()
        self.Text4.setDisabled(True)
        self.Text5 = QLineEdit()
        self.Text6 = QLineEdit()
        self.Text7 = QLineEdit()


        self.Button_3 = QPushButton()
        self.Button_4 = QPushButton()

        self.Comb_1 = QComboBox()
        information = ["Bit", "Int", "Real",'Word',"DWord"]
        self.Comb_1.addItems(information)
        self.Comb_2 =QComboBox()
        information = ["I", "Q", "M","DB"]
        self.Comb_2.addItems(information)
        #self.Comb_3 = QComboBox(self.P2)
        #information = ["DEC", "HEX",'BIN']
        #self.Comb_3.addItems(information)

        self.boxmsg = QTextBrowser()

        self.Label_4.setText('寄存器地址：')
        self.Label_5.setText('待写入值：')
        self.Button_3.setText('读值')
        self.Button_4.setText('写值')
        self.Text4.setText('0')
        self.Text5.setText('0')
        self.Text7.setText('0')
        self.Text6.setText('0')
        self.boxmsg.setText(
                            '1.软件基于S7通信协议，需要将snap7.dll复制到C:\Windows\System32\n'
                            '\n'
                             '2.PLC侧无需编程，允许远程PUT/GET访问\n'
                            '\n'
                            '3.I区写操作无效，DB块建议不勾选优化块访问\n'
                            '\n'
                             '4.16进制输入格式：如16#00FF 数据类型选择Word，待写入00FF\n'
                            '\n'
                            '5.版权所有者：porridge，欢迎学习交流(个人微信见左图)\n'
                            '\n'
                            '\n'                            
                            '\n'
                            '\n'
                            '---------------------------------------------------------------\n'
                            '                     本软件仅供学习交流   \n'
                            '            如作他用所承受的法律责任一概与作者无关\n'
                            '                (下载使用即代表你同意上述观点）\n'
                            '---------------------------------------------------------------')


        self.VBOX2 = QGridLayout()
        #VBOX2.setContentsMargins(200,30,30,0)
        self.VBOX2.addWidget(self.Label_4,1,1,1,1)
        self.VBOX2.addWidget(self.Comb_1,1,2,1,1)
        self.VBOX2.addWidget(self.Comb_2,1,3,1,1)
        self.VBOX2.addWidget(self.Text4,1,4,1,1)
        self.VBOX2.addWidget(self.Text5,1,5,1,1)
        self.VBOX2.addWidget(self.Text7,1,6,1,1)
        self.VBOX2.addWidget(self.Button_3,1,7,1,1)

        self.VBOX2.addWidget(self.Label_5,2,1,1,1)
        #self.VBOX2.addWidget(self.Comb_3,2,2,1,1)
        self.VBOX2.addWidget(self.Text6,2,2,1,5)
        self.VBOX2.addWidget(self.Button_4,2,7,1,1)
        self.VBOX2.addWidget(self.boxmsg, 3, 1, 1, 7)

        #
        All = QWidget(self)
        All.resize(1200*self.height/1920, 350*self.height/1080)
        self.VBOX3 = QHBoxLayout(self)

        self.VBOX3.addLayout(self.VBOX1)
        self.VBOX3.addLayout(self.VBOX2)

        self.setLayout(self.VBOX3)


        #self.setStyleSheet("#MAIN{border-image:url(:/1/捕获.JPG)}")
        All.setStyleSheet("background-image:url(:/1/捕获.JPG)")









        #plc连接/断开按钮事件
        self.Button_1.clicked.connect(self.clear)
        self.Button_1.clicked.connect(self.connectPLC)
        self.Button_2.clicked.connect(self.disconnectPLC)
        self.Button_3.clicked.connect(self.readPLC)
        self.Button_4.clicked.connect(self.writePLC)

        self.Comb_1.currentTextChanged.connect(self.changeText)
        self.Comb_2.currentTextChanged.connect(self.changeText)




    #槽函数：连接PLC
    def connectPLC(self):
        IP=self.Text1.text()
        JJ=eval(self.Text2.text())
        CC=eval(self.Text3.text())
        print(IP,JJ,CC)
        if (self.myplc.get_connected() == False):
            self.myplc.tongxin(IP,JJ,CC)
        if (self.myplc.get_connected() == True):

            self.boxmsg.append("<font color=green> -------------------------通信成功！-------------------------</font>")

            #self.boxmsg.setStyleSheet('QTextBrowser{font-family:"宋体";font-size:14px;color:rgb(0,200,100);}')

        else:
            self.boxmsg.append("<font color=red> -------------------------通信失败！-------------------------</font>")
    #清除注意提示
    def clear(self):
        self.boxmsg.clear()
    #槽函数：断开PLC连接
    def disconnectPLC(self):
       if (self.myplc.get_connected() == True):
        try:
            self.myplc.disconnect()
            print('断开成功')
            self.boxmsg.append("<font color=blue>------------------------ 断开成功！-------------------------</font>")
        except:
            pass

    def changeText(self):
        self.Datatype = self.Comb_1.currentText()
        self.DB_ON = self.Comb_2.currentText()
        #print( self.Datatype)


        if self.DB_ON != 'DB':
            self.Text4.setDisabled(True)
            self.Text4.setText('0')
            if self.Datatype != 'Bit':
                self.Text7.setDisabled(True)
            else:
                self.Text7.setDisabled(False)
        else:
            self.Text7.setDisabled(False)
            self.Text4.setDisabled(False)

    def get_rightdatatype(self,source,datatype,NO,start,end):
        if datatype == 'Bit':
            source=get_bool(source,0,end)
            source =str(source)
        if datatype == 'Int':
            source = get_int(source, 0)
            source = str(source)
        if datatype == 'Real':
            source = get_real(source, 0)
            source = round(source,3)
            source = str(source)
        if datatype == 'Word':
            source=source.hex() #python3 后可直接用hex（）读bytearry十六进制
            source = '0X '+str(source[0])+str(source[1])+' '+str(source[2])+str(source[3])
        if datatype == 'DWord':
            source = source.hex()
            source = '0X '+str(source[0])+str(source[1])+' '+str(source[2])+str(source[3])+' '+str(source[4])+str(source[5])+' '+str(source[6])+str(source[7])
        return source

    def WriteDate(self,area,NO,start,end,datatype,value):
        if datatype == 'Bit':
            Datatype = 1
            result = self.myplc.read_area(area,NO, start, Datatype)
            if value == '0'or value == 'False':
                value = False
            else:
                value = True
            set_bool(result, NO, end, value)
        if datatype == 'Int':
            Datatype = 2
            result = self.myplc.read_area(area, NO, start, Datatype)
            value = int(value)
            set_int(result, NO, value)
        if datatype == 'Real':
            Datatype = 4
            result = self.myplc.read_area(area,NO, start, Datatype)
            value = eval(value)
            set_real(result, NO, value)
        if datatype == 'Word':
            Datatype = 2
            result = self.myplc.read_area(area, NO, start, Datatype)
            int_DATA=self.str_into_int(value,4)
            set_int(result, NO, int_DATA)
        if datatype == 'DWord':
            Datatype = 4
            result = self.myplc.read_area(area, NO, start, Datatype)
            int_DATA=self.str_into_int(value,8)
            set_dword(result, NO, int_DATA)
        self.myplc.write_area(area, NO, start, result)

    def str_into_int(self,DATA,m):
        #从文本框获取hex表示的字符串数据，转int
        T = DATA
        C = 0
        j = m
        for i in T:
            if i == 'A'or i =='a':
                k = 10
            elif i == 'B'or i =='b':
                k = 11
            elif i == 'C'or i == 'c':
                k = 12
            elif i == 'D'or i == 'd':
                k = 13
            elif i == 'E'or i =='e':
                k = 14
            elif i == 'F'or i =='f':
                k = 15

            else:

                k = int(i)
            j = j - 1
            # C+=int(i)
            C += k * 16 ** j
        print(int(C))
        int_data = int(C)


        return int_data


 # 槽函数：读数据
    def readPLC(self,sign):
        if (self.myplc.get_connected() == True):
            #首先获取读取的数据类型
            datatype = self.Comb_1.currentText()
            Datatype = 1
            if datatype == 'Bit':
                Datatype = 1
            if datatype == 'Int':
                Datatype = 2
            if datatype == 'Real':
                Datatype = 4
            if datatype == 'Word':
                Datatype = 2
            if datatype == 'DWord':
                Datatype = 4
            try:
                #再获取读的区域
                area = areas[self.Comb_2.currentText()]
                # S数据起始与长度
                if area == 0x84:
                    NO= int(self.Text4.text())
                    start = int(self.Text5.text())
                    end = int(self.Text7.text())
                else:
                    NO = 0
                    start = int(self.Text5.text())
                    end = int(self.Text7.text())

                print(area,0, start, Datatype)
                result = self.myplc.read_area(area,NO,start,Datatype)
                print(result)

                result=self.get_rightdatatype(result,datatype,NO,start,end)

                if sign ==0:
                    print (result)
                    self.boxmsg.append("读取结果：%s"%str(result))
                else:
                    self.boxmsg.append("<font color=blue> Data Back:%s </font>" % str(result))

            except:
                self.boxmsg.append("<font color=red>读取失败！</font>")
                pass
        else:
            self.boxmsg.append("<font color=red>通信未连接！</font>")

 # 槽函数：写数据
    def writePLC(self):
        if (self.myplc.get_connected() == True):
            #首先获取读取的数据类型
            datatype = self.Comb_1.currentText()


            try:
                #再获取读的区域
                area = areas[self.Comb_2.currentText()]
                # S数据起始与长度
                if area == 0x84:
                    NO= int(self.Text4.text())
                    start = int(self.Text5.text())
                    end = int(self.Text7.text())
                else:
                    NO = 0
                    start = int(self.Text5.text())
                    end = int(self.Text7.text())

                value =self.Text6.text()

                self.WriteDate(area,NO,start,end,datatype,value)

                self.readPLC(1)





            except:
                self.boxmsg.append("<font color=red>写入失败！</font>")
                pass
        else:
            self.boxmsg.append("<font color=red>通信未连接！</font>")
            pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PLC_Assiastant()
    main.show()
    sys.exit(app.exec_())