from PyQt4 import QtCore, QtGui, QtWebKit

class Browser(QtGui.QMainWindow):
    
    def __init__(self):
        """
            Initialize the browser GUI and connect the events\
        """
        QtGui.QMainWindow.__init__(self)
        self.resize(800,600)
        self.centralwidget = QtGui.QWidget(self)
        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(1)
        
        self.frame = QtGui.QFrame(self.centralwidget)
        
        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.tb_url = QtGui.QLineEdit(self.frame)
        self.bt_back = QtGui.QPushButton(self.frame)
        self.bt_ahead = QtGui.QPushButton(self.frame)
        ##start\
        self.bt_train = QtGui.QPushButton("train",self.frame)
        self.bt_ignore = QtGui.QPushButton("ignore",self.frame)
        self.bt_black_out = QtGui.QPushButton(self.frame)
        ##end\
        self.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
        self.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))
        self.horizontalLayout.addWidget(self.bt_back)
        self.horizontalLayout.addWidget(self.bt_ahead)
        ##start\
        self.horizontalLayout.addWidget(self.bt_black_out)
        self.horizontalLayout.addWidget(self.bt_train)
        self.horizontalLayout.addWidget(self.bt_ignore)
        ##end\
        self.horizontalLayout.addWidget(self.tb_url)
        self.gridLayout.addLayout(self.horizontalLayout)
        
        self.html = QtWebKit.QWebView()
        self.gridLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)
        
        self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
        self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
        self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)
        ##\
        self.connect(self.bt_train, QtCore.SIGNAL("clicked()"), self.train_signal)
        self.connect(self.bt_ignore, QtCore.SIGNAL("clicked()"), self.ignore_signal)
        self.connect(self.bt_black_out,QtCore.SIGNAL("clicked()"),self.black_out)
        ##\
        self.default_url = "https://google.com/"
        self.tb_url.setText(self.default_url)
        self.browse()
    
    def train_signal(self):
        print("Train new face")
    def ignore_signal(self):
        print("Ignore new face")
    def black_out(self):
        
        self.html.load(QtCore.QUrl("http://www.freepngimg.com/download/blocked/6-2-blocked-png-clipart.png"))
        self.horizontalLayout.removeWidget(self.bt_ahead)
        self.horizontalLayout.removeWidget(self.bt_back)
        self.horizontalLayout.removeWidget(self.tb_url)
        self.horizontalLayout.removeWidget(self.bt_train)
        self.horizontalLayout.removeWidget(self.bt_ignore)
        self.html.show()
    
    def browse(self):
        """
            Make a web browse on a specific url and show the page on the\
            Webview widget.\
        """
        
        url = self.tb_url.text() if self.tb_url.text() else self.default_url
        self.html.load(QtCore.QUrl(url))
        self.html.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = Browser()
    main.show()
    app.exec_()
    app.exit()
