import asyncio
import sys
import websockets
import base64
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton, QSplitter,
    QTextEdit,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from asyncqt import QEventLoop, asyncSlot
from websockets.exceptions import ConnectionClosed

from QKVLineEdit import KVList
from QTextButtonList import ButtonListView

class MainWindow(QMainWindow):


    _SESSION_TIMEOUT = 1.
    """float: Session timeout."""


    def __init__(self):
        super().__init__()

        self.initContent() 
        self.initToolbar()

        self.setGeometry(400, 400, 450, 250)
        self.setWindowTitle('Websocket Test Client')
        self.show()

    def initContent(self):
        self.postman = Postman()
        self.postman.signal.signal.connect(self.pushToHistory)
        
        self.listyList = ButtonListView(self.postman.setValues)
        self.splitter = QSplitter()
        self.splitter.addWidget(self.listyList)
        self.splitter.addWidget(self.postman)
        self.splitter.setStretchFactor(0,1)
        self.splitter.setStretchFactor(1,2)
        self.setCentralWidget(self.splitter)


    def initToolbar(self):
        self.toolbar = QToolBar("Main toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(QAction("&New", self))
        self.toolbar.setMouseTracking(True)

        button_action = QAction("Your Button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(lambda x: print("toolbar button clicked"))

        saveButton=QToolButton(self)
        saveButton.setPopupMode(QToolButton.InstantPopup)
        saveButton.setText("save")
    
        menu = QMenu(saveButton)
        menu.addAction(QAction("save all", self))
        menu.addAction(QAction("save as", self))
        saveButton.setMenu(menu)

        self.toolbar.addWidget(saveButton)
        self.toolbar.addAction(button_action)

    
    @pyqtSlot(str, dict, str)
    def pushToHistory(self, url, params, body):
        b = self.listyList.wlist.itemWidget(self.listyList.wlist.item(0))
        
        if b.url != url or b.body != body or b.params != params: 
            self.listyList.pushToHistory(url, body, params)
        

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def contextMenuEvent(self, event):
        print("context menu")
        super(MainWindow, self).contextMenuEvent(event)

class PostmanSignal(QObject):
    def __init__(self) -> None:
        super(PostmanSignal, self).__init__()

    signal = pyqtSignal(str, dict, str) 
    

class Postman(QWidget ):

    def __init__(self):
        super().__init__()
        
        self.initTopBar()
        
        self.pairList = KVList() 
        self.vbox.addWidget(self.pairList)
        #self.addPairButton = QPushButton("Add Pair", self)
        #self.addPairButton.clicked.connect(self.pairList.addKVPair)

        #self.removePairButton = QPushButton("Remove Pair", self)
        #self.removePairButton.clicked.connect(self.pairList.removeKVPair)

        #buttons = QHBoxLayout()
        #buttons.addWidget(self.addPairButton)
        #buttons.addWidget(self.removePairButton)
        #buttonsWidget = QWidget()
        #buttonsWidget.setLayout(buttons)
        #self.vbox.addWidget(buttonsWidget)        
       
        self.body = QTextEdit()
        self.vbox.addWidget(self.body)

        self.editResponse = QTextEdit()
        self.vbox.addWidget(self.editResponse)

        self.setLayout(self.vbox)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 

    def initTopBar(self):
        self.vbox = QVBoxLayout()
        self.signal = PostmanSignal()    
        self.urlBar = QLineEdit()
        self.topBar = QWidget()
        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.addWidget(self.urlBar)
        
        self.connectButton = QPushButton("Connect", self)
        self.connectButton.clicked.connect(self.sendConnectRequest)
        self.topBarLayout.addWidget(self.connectButton) 
        self.disconnectButton = QPushButton("Disconnect", self)
        self.disconnectButton.clicked.connect(self.disconnect)
        self.topBarLayout.addWidget(self.disconnectButton)
        
        self.sendButton = QPushButton("Send Text")
        self.sendButton.clicked.connect(self.sendMessage)
        self.topBarLayout.addWidget(self.sendButton)
        
        self.topBar.setLayout(self.topBarLayout)
        
        self.vbox.addWidget(self.topBar)
        
    def setValues(self, url, params=None, body=None):
        self.urlBar.setText(url)
        self.pairList.setPairs(params if params else {})
        self.body.setText(body if body else '')
    
    @asyncSlot()
    async def disconnect(self) -> None:
        await self.ws.close()
    
    @asyncSlot()
    async def sendConnectRequest(self):
        self.signal.signal.emit(
                self.urlBar.text(), 
                self.pairList.getPairs(),
                ''
        )
        try:
            username = self.pairList.pairs[0].getKey()
            password = self.pairList.pairs[0].getValue()
            auth_header = 'Basic ' + base64.b64encode(bytes(username + ':' + password, 'utf-8')).decode('utf-8')

            self.ws = await websockets.connect(self.urlBar.text(),
                    extra_headers={'Authorization': auth_header})
        except Exception as exc:
            print(exc)
            self.body.setText(str(exc))
            return
        else:
            print("Connected")
        try:
            async for recieved in self.ws: 
                if isinstance(recieved, bytes):
                    recieved = recieved.decode('utf-8')

                self.body.setText(recieved)
        except ConnectionClosed as c:
            print("Connection Closed: code {} \n {}".format(c.code, c.reason))

    @asyncSlot()
    async def sendMessage(self):
        await self.ws.send(self.editResponse.toPlainText())


app = QApplication(sys.argv)
loop = QEventLoop(app)

# this allows me to use async/await with pyqt.
# Apparently it's not super performant, but I don't really need it to be.
asyncio.set_event_loop(loop)

window = MainWindow()
window.show()
# Start the event loop.
with loop:
    sys.exit(loop.run_forever())

