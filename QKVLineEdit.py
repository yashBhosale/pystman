from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QScrollArea, QVBoxLayout

class KVLineEdit(QWidget):
    
    def __init__(self):
        super().__init__()
        print("KVLineEdit created")
        hbox = QHBoxLayout()
        self.key = QLineEdit()
        self.value = QLineEdit()
        hbox.addWidget(self.key)
        hbox.addWidget(self.value)
        hbox.setContentsMargins(0,0,0,0)
        hbox.setSpacing(0)
        self.setLayout(hbox)
    
    def getKey(self) -> str:
        return self.key.text()
    def getValue(self) -> str:
        return self.value.text()

class KVList(QWidget):

    def __init__(self):
        super().__init__()
        self.pairs = []
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.addKVPair()
        
    def addKVPair(self):
        newPair = KVLineEdit()
        self.pairs.append(newPair)
        self.vbox.addWidget(newPair)

    def removeKVPair(self):
        if self.pairs:
            toRemove = self.pairs.pop()
            self.vbox.removeWidget(toRemove)

    def getPairs(self):
        retPairs = {}
        
        for pair in self.pairs:
            retPairs[pair.getKey()] = pair.getValue()
        
        return retPairs

    def setPairs(self, pairsToSet):
        if not pairsToSet:
            for i in range(len(self.pairs)):
                self.removeKVPair()

        diff = len(pairsToSet) - len(self.pairs)
        
        if diff < 0:
            for _ in range(diff):
                self.addKVPair()
        elif diff > 0:
            for _ in range(0, diff, -1):
                self.removeKVPair()

        for i, key in enumerate(pairsToSet):
            self.pairs[i].key.setText(key)
            self.pairs[i].value.setText(pairsToSet[key])



