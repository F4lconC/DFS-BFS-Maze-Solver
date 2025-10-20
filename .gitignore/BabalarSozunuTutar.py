import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import styles
import DFSandBFS


# noinspection PyUnresolvedReferences
class MazeSolver(QWidget):

    def __init__(self):
        super().__init__()

        self.a = QVBoxLayout()

        self.squareButtons = {}
        self.buttons = {}
        self.widgets = {}
        self.change = ""

        self.placeOfA = -1
        self.placeOfB = -1

        self.start()

        self.show()

    def start(self, rows=7, columns=7):

        self.hide_everything()
        self.clear_widgets()

        self.a.addLayout(self.merge_all_layouts(rows, columns))

        self.setLayout(self.a)

    def merge_all_layouts(self, rows, colums):

        layout_of_square_buttons = self.create_maze(rows, colums)
        placing_buttons = self.create_right_side_buttons()
        lsb = self.create_left_side_buttons(rows)

        h_layout = QHBoxLayout()
        h_layout.addLayout(placing_buttons)
        h_layout.addStretch()
        h_layout.addLayout(layout_of_square_buttons)
        h_layout.addStretch()
        h_layout.addLayout(lsb)

        return h_layout

    def create_square_buttons(self, row: int, column: int, size: int) -> QVBoxLayout:

        vbox = QVBoxLayout()
        vbox.addStretch()
        counter = 0
        for i in range(row):

            hbox = QHBoxLayout()
            hbox.addStretch()
            hbox.setSpacing(0)

            for j in range(column):
                button = QPushButton()
                button.setFixedSize(size, size)
                button.setAccessibleName(str(i) + str(j))
                counter += 1

                button_stylesheet = """
                    background-color: gray;
                    color: white;
                    font: bold;
                    font-family: 'Times New Roman', Times, serif;
                    font-size: 32px;
                    border: 1px solid black;
                    padding: 0px;
                    margin: 0px 0px;
                """
                button.setStyleSheet(button_stylesheet)

                button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

                button.setDisabled(True)

                self.squareButtons[button.accessibleName()] = button
                self.squareButtons[button.accessibleName()].clicked.connect(
                    lambda checked, arg=self.squareButtons[button.accessibleName()]: self.change_square_button(arg))
                hbox.addWidget(self.squareButtons[button.accessibleName()])

            hbox.setSpacing(0)
            hbox.addStretch()
            vbox.addLayout(hbox)
            vbox.setSpacing(0)
        vbox.addStretch()
        return vbox

    def create_maze(self, row: int, column: int) -> QVBoxLayout:

        # Clear last Maze
        self.squareButtons.clear()

        MAX_WIDTH_AND_HEIGHT = 600
        width_and_height_of_squares = MAX_WIDTH_AND_HEIGHT // max(row, column)

        maze = self.create_square_buttons(row, column, width_and_height_of_squares)

        return maze

    def create_right_side_buttons(self):

        button_stylesheet = """
                background-color: {};
                color: white;
                font-size: 22px;
                border: 2px solid {};
                border-radius: 16px;
                padding: 6px 16px;
                margin: 5px 3px;
            """
        v_layout = QVBoxLayout()
        for color, text in [("green", "Place A"), ("orange", "Place B"), ("brown", "Place/Remove Walls")]:

            button = QPushButton(text)

            button.setFixedWidth(240)

            button.setStyleSheet(button_stylesheet.format(color, color))

            button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

            button.setAccessibleName(text)
            self.buttons[button.accessibleName()] = button

            v_layout.addWidget(self.buttons[button.accessibleName()])

        self.buttons["Place A"].clicked.connect(self.placeA)
        self.buttons["Place B"].clicked.connect(self.placeB)
        self.buttons["Place/Remove Walls"].clicked.connect(self.place_walls)

        return v_layout

    def create_left_side_buttons(self, size_of_maze):

        h_layout = QHBoxLayout()
        h_layout.addStretch()

        text = "Size: "
        label = QLabel(text)
        self.widgets[text] = label

        combo_box = QComboBox()

        for i in range(3, 10):
            combo_box.addItem(str(i))

        combo_box.setCurrentIndex(size_of_maze - 3)
        combo_box.setAccessibleName(text + "combo")

        combo_box.currentIndexChanged.connect(self.create_new_maze)

        self.widgets[text + "combo"] = combo_box

        h_layout.addWidget(label)
        h_layout.addWidget(self.widgets[text + "combo"])
        h_layout.addStretch()

        button_stylesheet = """
            background-color: green;
            color: white;
            font-size: 22px;
            border: 2px solid green;
            border-radius: 16px;
            padding: 6px 16px;
            margin: 5px 3px 50px 3px;
        """
        clear_maze_button = QPushButton("Clear Maze")
        clear_maze_button.setStyleSheet(button_stylesheet)

        clear_maze_button.clicked.connect(self.create_new_maze)

        clear_maze_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        clear_maze_button.setFixedWidth(240)

        clear_maze_button.setAccessibleName("Clear Maze")
        self.buttons[clear_maze_button.accessibleName()] = clear_maze_button

        maze_button_layout = QHBoxLayout()
        maze_button_layout.addStretch()
        maze_button_layout.addWidget(self.buttons[clear_maze_button.accessibleName()])
        maze_button_layout.addStretch()

        style = """
            background-color: {};
            color: white;
            font-size: 22px;
            border: 3px solid {};
            border-radius: 10px;
            padding: 4px 16px;
            margin: 5px;
        """

        dfs_bfs_layout = QHBoxLayout()
        dfs_bfs_layout.addStretch()

        for text, color in [("DFS", "green"), ("BFS", "gray")]:

            button = QPushButton(text)
            button.setStyleSheet(style.format(color, color))

            button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            button.clicked.connect(
                lambda checked, arg=text: self.dfs_and_bfs_button(arg))

            button.setAccessibleName(text)
            self.buttons[text] = button

            dfs_bfs_layout.addWidget(self.buttons[text])

        dfs_bfs_layout.addStretch()

        button_solve = QPushButton("Solve")
        button_solve.setStyleSheet("""
            background-color: purple;
            color: white;
            font-size: 24px;
            border: 2px solid purple;
            border-radius: 16px;
            padding: 6px 16px;
            margin: 5px 3px 50px 3px;
               """)

        button_solve.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        button_solve.clicked.connect(self.solve)
        self.buttons["solve"] = button_solve

        solve_layout = QHBoxLayout()
        solve_layout.addWidget(self.buttons["solve"])

        left_side_layout = QVBoxLayout()

        left_side_layout.addStretch()
        left_side_layout.addLayout(h_layout)
        left_side_layout.addLayout(maze_button_layout)
        left_side_layout.addLayout(dfs_bfs_layout)
        left_side_layout.addLayout(solve_layout)
        left_side_layout.addStretch()

        return left_side_layout

    def assign_command_to_squares(self):

        for i in range(len(self.squareButtons)):
            self.squareButtons[str(i)].clicked.connect(
                lambda: self.change_square_button(self.squareButtons[str(i)]))

    def enable_square_buttons(self):
        for i in self.squareButtons.keys():
            self.squareButtons[str(i)].setEnabled(True)

    def disable_square_buttons(self):
        for i in self.squareButtons.keys():
            self.squareButtons[i].setEnabled(False)

    def change_square_button(self, button: QPushButton):

        name = button.accessibleName()
        if self.change == "A":
            if self.placeOfA != -1:
                self.squareButtons[str(self.placeOfA)].setStyleSheet(styles.styleWall)
                self.squareButtons[str(self.placeOfA)].setText("")
            self.squareButtons[name].setText("A")
            self.squareButtons[name].setStyleSheet(styles.styleA)
            self.placeOfA = name
            self.disable_square_buttons()
        elif self.change == "B":
            if self.placeOfB != -1:
                self.squareButtons[str(self.placeOfB)].setStyleSheet(styles.styleWall)
                self.squareButtons[str(self.placeOfB)].setText("")
            self.squareButtons[name].setText("B")
            self.squareButtons[name].setStyleSheet(styles.styleB.format("orange"))
            self.placeOfB = name
            self.disable_square_buttons()
        elif self.change == "Wall":

            if (self.squareButtons[name].palette().window().color().name() == "#808080" or button.text() == 'A'
                    or button.text() == "B"):
                self.squareButtons[name].setStyleSheet(styles.styleEmpty)
            else:
                self.squareButtons[name].setStyleSheet(styles.styleWall)

    def placeA(self):
        self.change = "A"
        self.enable_square_buttons()

    def placeB(self):
        self.change = "B"
        self.enable_square_buttons()

    def place_walls(self):
        self.change = "Wall"
        self.enable_square_buttons()

    def create_new_maze(self):

        self.placeOfA = -1
        self.placeOfB = -1

        rows = int(self.widgets["Size: combo"].currentText())
        columns = int(self.widgets["Size: combo"].currentText())

        self.start(rows, columns)

    def dfs_and_bfs_button(self, name: str):

        if self.buttons[name].palette().window().color().name() == "#808080":
            self.buttons[name].setStyleSheet(styles.styleTrueDfs)
            name1 = 'B' if name[0] == 'D' else 'D'
            name1 += name[1:3]
            self.buttons[name1].setStyleSheet(styles.styleFalseDfs)

    def hide_everything(self):
        for i in self.squareButtons.keys():
            self.squareButtons[i].hide()

        for i in self.buttons.keys():
            self.buttons[i].hide()

        for i in self.widgets.keys():
            self.widgets[i].hide()

    def clear_widgets(self):

        self.squareButtons.clear()
        self.widgets.clear()
        self.buttons.clear()
        self.change = ""

    def solve(self):

        if self.placeOfA == -1 or self.placeOfB == -1:
            messageBox = QMessageBox()
            QMessageBox.about(messageBox, "Invalid Maze", "There are missing A or B")
            return

        class Node:

            def __init__(self, place, value=None):
                self.place = place
                self.value = value
                self.neighboors = []

        createdNodes = {}

        for i in self.squareButtons.keys():

            if self.squareButtons[i].palette().window().color().name() == "#808080":
                continue

            if i not in createdNodes.keys():
                node = Node((i[0], i[1]), self.squareButtons[i].text())
                createdNodes[i] = node
            else:
                node = createdNodes[i]

            for j in (-1, 1):

                x = int(i[0])
                y = int(i[1])
                try:
                    if self.squareButtons[str(x + j) + i[1]].palette().window().color().name() != "#808080":
                        if str(x + j) + i[1] not in createdNodes.keys():
                            newNode = Node((str(x + j), i[1]), self.squareButtons[str(x + j) + i[1]].text())
                            createdNodes[i].neighboors.append(newNode)
                            createdNodes[str(x + j) + i[1]] = newNode
                        else:
                            createdNodes[i].neighboors.append(createdNodes[str(x + j) + i[1]])

                except:
                    pass

                try:
                    a = 1313
                    if self.squareButtons[i[0] + str(y + j)].palette().window().color().name() != "#808080":
                        if i[0] + str(y + j) not in createdNodes.keys():
                            newNode = Node((i[0], str(y + j)), self.squareButtons[i[0] + str(y + j)].text())
                            createdNodes[i].neighboors.append(newNode)
                            createdNodes[i[0] + str(y + j)] = newNode
                        else:
                            createdNodes[i].neighboors.append(createdNodes[i[0] + str(y + j)])
                except:
                    pass

        if self.buttons["DFS"].palette().window().color().name() == "#808080":
            dfs = False
        else:
            dfs = True
        solver = DFSandBFS.MazeSolverr(createdNodes[self.placeOfA], dfs)
        solution = solver.solve()
        if solution == None:
            messageBox = QMessageBox()
            QMessageBox.about(messageBox, "No Solution", "There is no solution for this maze.")
            return
        self.showSolution(solution[1:])

    def sleep(self, time):

        loop = QEventLoop()
        QTimer.singleShot(time * 100, loop.quit)
        loop.exec_()

    def showSolution(self, solution: list):

        for i in solution:
            self.squareButtons[i[0] + i[1]].setStyleSheet(styles.styleYellow)
            self.sleep(5)

        self.squareButtons[self.placeOfB].setStyleSheet(styles.styleB.format("green"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MazeSolver()
    sys.exit(app.exec_())
