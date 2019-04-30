from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QButtonGroup, QGroupBox, QGridLayout, QHBoxLayout, QLabel, QPlainTextEdit, QVBoxLayout
from PyQt5.QtGui import QPainter, QGuiApplication
import time

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
        self.width = 160
        self.height = 120
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
            btn.setSizePolicy(50, 50)
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
        self.width = 250
        self.height = 600
        self.dialog = Visu_npuzzle(data, dim)
        self.initUI()

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
        self.btn_solve.move(60, 370)
        self.btn_solve.clicked.connect(self.solve)
        
        self.btn_previous = QPushButton("Previous", self)
        self.btn_previous.move(5, 340)
        self.btn_previous.clicked.connect(self.previous)

        self.btn_next = QPushButton("next", self)
        self.btn_next.move(110, 340)
        self.btn_next.clicked.connect(self.next)

        self.label_h = QLabel("Heuristic choice :", self)
        self.label_h.move(10, 210)
        self.label_c = QLabel("Cost choice :", self)
        self.label_c.move(10, 90)

        self.result = QLabel("")
        self.current_move = QLabel("")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label_h)
        self.vbox.addWidget(self.btn_h_lc)
        self.vbox.addWidget(self.btn_h_man)
        self.vbox.addWidget(self.btn_h_ham)
        self.vbox.addWidget(self.btn_h_euc)

        self.vbox.addWidget(self.label_c)
        self.vbox.addWidget(self.btn_c_astar)
        self.vbox.addWidget(self.btn_c_uni)
        self.vbox.addWidget(self.btn_c_greedy)

        self.vbox.addWidget(self.btn_previous)
        self.vbox.addWidget(self.btn_next)
        self.vbox.addWidget(self.btn_solve)
        self.vbox.addWidget(self.result)
        self.vbox.addWidget(self.current_move)

#        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

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
                widgetToRemove = self.result
                widgetToRemove.setParent(None)
                widgetToRemove.deleteLater()
                self.result = QLabel("Error taquin unsolvable")
                self.vbox.addWidget(self.result)
                print("Error taquin unsolvable")
            elif e.__str__() == "ErrorHeuristic":
                print("Error heuristic don't exist")
            elif e.__str__() == "ErrorCost":
                print("Error cost don't exist")
            else:
                print(e)
            return

        start_time = time.time()
        self.res = a_star(graph)
        true_time = time.time() - start_time
        solutions = []
        res = self.res
        while res:
            solutions.insert(0, res)
            res = res.parent
        self.solutions = solutions
        self.solutions_visu = len(solutions) - 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()

        # display infos
        widgetToRemove = self.result
        widgetToRemove.setParent(None)
        widgetToRemove.deleteLater()
        text = "Nb moves : {}\n".format(self.res.g)
        text += "Time complexity : {}\n".format(graph.time_complexity)
        text += "Space complexity : {}\n".format(graph.size_complexity)
        text += "True time resolution : {:2f}\n".format(true_time)
        self.result = QLabel(text)
        self.vbox.addWidget(self.result)

        # display move in other window
        widgetToRemove = self.current_move
        widgetToRemove.setParent(None)
        widgetToRemove.deleteLater()
        self.current_move = QLabel("Current move : " + str(self.solutions_visu))
        self.vbox.addWidget(self.current_move)

        return

    def next(self):
        if not hasattr(self, 'solutions_visu'):
            return
        if self.solutions_visu + 1 > len(self.solutions) - 1:
            return
        self.solutions_visu += 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()

        widgetToRemove = self.current_move
        widgetToRemove.setParent(None)
        widgetToRemove.deleteLater()
        self.current_move = QLabel("Current move : " + str(self.solutions_visu))
        self.vbox.addWidget(self.current_move)

        return

    def previous(self):
        if not hasattr(self, 'solutions_visu'):
            return
        if self.solutions_visu - 1 < 0:
            return
        self.solutions_visu -= 1
        self.dialog.data = self.solutions[self.solutions_visu].puzzle
        self.dialog.updateGrid()

        widgetToRemove = self.current_move
        widgetToRemove.setParent(None)
        widgetToRemove.deleteLater()
        self.current_move = QLabel("Current move : " + str(self.solutions_visu))
        self.vbox.addWidget(self.current_move)
        return
