from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class CustomButton(QtWidgets.QPushButton):
    
    def __init__(self, url, params, body, callback, parent=None):
        super(CustomButton, self).__init__(parent)
        dim = QtGui.QFontMetrics(QtGui.QFont("Decorative", 10))

        self.url = url
        self. params = params
        self.body = body
        self.setMinimumSize(dim.width(self.url), dim.height()*2)
        self.resize(dim.width(self.url), dim.height()*2)
        self.clicked.connect(lambda: callback(self.url, self.params, self.body))
    
    def paintEvent (self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setFont(QtGui.QFont('Decorative', 10))
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, self.url)
        paint.end()



class Query():

    def __init__(self, url=None, params=None, method=None):
        self.url = url or ""
        self.params = params or {"a":"1", "b":"2"}
        self.method = method or  "POST"

class ButtonListView(QtWidgets.QWidget):
    
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.createLayout()

    def pushToHistory(self, url, body, params):
        QLWI = QListWidgetItem()
        new_button = CustomButton(url, params, body, self.callback)
        QLWI.setSizeHint(self.buttonSize)
        self.wlist.insertItem(0, QLWI)
        self.wlist.setItemWidget(QLWI, new_button)
        
    def createLayout(self):
        
        self.wlist = QtWidgets.QListWidget()
        self.wlist.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustToContents) 
        
        item1 = QtWidgets.QListWidgetItem(self.wlist)
        item_widget = CustomButton("http://www.url.com", {"A":"b"}, '', self.callback)
         
        item1.setSizeHint(item_widget.size())
        self.wlist.setSpacing(0)
        size = item_widget.size()
        size.setWidth(size.width() + 5)
        self.buttonSize = size
        self.wlist.setMinimumSize(size)
        self.wlist.addItem(item1)
        self.wlist.setItemWidget(item1, item_widget)
        
        listLayout = QtWidgets.QVBoxLayout()
        listLayout.addWidget(self.wlist)
        
        self.setLayout(listLayout)

