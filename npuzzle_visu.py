from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QButtonGroup, QGroupBox, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPainter

class Visu_option(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = "SUPER N-puzzle solver options ROZY"
        self.left = 1200
        self.top = 300
        self.width = 200
        self.height = 480
        self.initUI()

    def paintEvent(self, e):
        rect1 = QPainter(self)
        rect1.drawRect(10, 230, 150, 100)
        rect2 = QPainter(self)
        rect2.drawRect(10, 110, 150, 80)
        
    def initBtn(self):
        self.group_h = QButtonGroup(self)
        self.group_c = QButtonGroup(self)

        self.btn_h_lc = QRadioButton("Linear Conflicts", self)
        self.btn_h_man = QRadioButton("Manhattan", self)
        self.btn_h_ham = QRadioButton("Hamming", self)
        self.btn_h_euc = QRadioButton("Euclidienne", self)

        self.btn_c_astar = QRadioButton("A*", self)
        self.btn_c_greedy = QRadioButton("Greedy searches", self)
        self.btn_c_uni = QRadioButton("Uniform cost", self)

        self.group_h.addButton(self.btn_h_lc)
        self.group_h.addButton(self.btn_h_man)
        self.group_h.addButton(self.btn_h_ham)
        self.group_h.addButton(self.btn_h_euc)

        self.group_c.addButton(self.btn_c_astar)
        self.group_c.addButton(self.btn_c_greedy)
        self.group_c.addButton(self.btn_c_uni)

        self.btn_h_lc.move(20, 240)
        self.btn_h_man.move(20, 260)
        self.btn_h_ham.move(20, 280)
        self.btn_h_euc.move(20, 300)
        
        self.btn_c_astar.move(20, 120)
        self.btn_c_greedy.move(20, 140)
        self.btn_c_uni.move(20, 160)

        self.btn_h_lc.setChecked(True)
        self.btn_c_astar.setChecked(True)

        self.btn_solve = QPushButton("Solve", self)
        self.btn_solve.move(20, 380)

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.initBtn()
        self.show()

class Visu_npuzzle(QWidget):

    def __init__(self, data, dim):
        super().__init__()
        self.data = data
        self.dim = dim
        self.title = "SUPER N-puzzle solver ROZY"
        self.left = 500
        self.top = 300
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.makeGrid()
        self.show()

    def makeGrid(self):
        data = self.data
        dim = self.dim
        self.grid_layout = QGridLayout()
        positions = [(i, j) for i in range(dim) for j in range(dim)]
        for pos, val in zip(positions, data):
            btn = QPushButton(str(val))
            self.grid_layout.addWidget(btn, *pos)
        self.setLayout(self.grid_layout)

    def updateGrid(self):
        for i in reversed(range(self.grid_layout.count())):
            widgetToRemove = self.grid_layout.itemAt(i).widget()
            widgetToRemove.setParent(None)
            widgetToRemove.deleteLater()
        try:
            index = 0
            for row in range(self.grid_layout.rowCount()):
                for column in range(self.grid_layout.columnCount()):
                    btn = QPushButton(str(self.data[index]))
                    self.grid_layout.addWidget(btn, row, column)
                    index += 1
        except IndexError:
            pass
