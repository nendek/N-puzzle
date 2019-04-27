from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QButtonGroup, QGroupBox, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter

from npuzzle_algo import a_star
from npuzzle_graph import NpuzzleGraph

class Visu_npuzzle(QWidget):

    def __init__(self, data, dim):
        super().__init__()
        self.data_init = data
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

class Visu_option(QWidget):
    
    def __init__(self, data, dim):
        super().__init__()
        self.title = "SUPER N-puzzle solver options ROZY"
        self.left = 1200
        self.top = 300
        self.width = 200
        self.height = 480
        self.dialog = Visu_npuzzle(data, dim)
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
        self.btn_solve.clicked.connect(self.solve)
        
        self.btn_previous = QPushButton("Previous", self)
        self.btn_previous.move(100, 340)
        self.btn_previous.clicked.connect(self.previous)

        self.btn_next = QPushButton("next", self)
        self.btn_next.move(20, 340)
        self.btn_next.clicked.connect(self.next)

        self.label_h = QLabel("Heuristic choices")

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.initBtn()
        self.dialog.show()

    def solve(self):
        if self.btn_h_lc.isChecked():
            heuristic = "linear_conflicts"
        elif self.btn_h_man.isChecked():
            heuristic = "manhattan"
        elif self.btn_h_ham.isChecked():
            heuristic = "hamming"
        elif self.btn_h_euc.isChecked():
            heuristic = "euclidienne"
        else:
            heuristic = "linear_conflicts"

        if self.btn_c_astar.isChecked():
            cost = "a_star"
        elif self.btn_c_uni.isChecked():
            cost = "uniform_cost"
        elif self.btn_c_greedy.isChecked():
            cost = "greedy_searches"

        try:
            graph = NpuzzleGraph(self.dialog.dim, self.dialog.data_init, cost, heuristic)
        except Exception as e:
            if e.__str__() == "unsolvable":
                print("Error taquin unsolvable")
            elif e.__str__() == "ErrorHeuristic":
                print("Error heuristic don't exist")
            elif e.__str__() == "ErrorCost":
                print("Error cost don't exist")
            else:
                print(e)
            return

        self.res = a_star(graph)
        solutions = []
        res = self.res
        while res:
            solutions.insert(0, res)
            res = res.parent
        self.solutions = solutions
        self.solutions_visu = len(solutions) - 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()
        return

    def next(self):
        if not hasattr(self, 'solutions_visu'):
            return
        if self.solutions_visu + 1 > len(self.solutions) - 1:
            return
        self.solutions_visu += 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()

        return

    def previous(self):
        if not hasattr(self, 'solutions_visu'):
            return
        if self.solutions_visu - 1 < 0:
            return
        self.solutions_visu -= 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()
        return
