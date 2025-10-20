import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import styles



class FrameView(QWidget):


    def __init__(self, rows=7, columns=7):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.squareButtons = dict()
        self.buttons = dict()    
        self.widgets = dict()

        self.a = QVBoxLayout()
        self.a.addLayout(self.merge_all_layouts(rows, columns))

        self.setLayout(self.a)
        self.show()
        

    
    def reset(self, rows=7, columns=7):

        self.hide_everything()
        self.clear_widgets()
        self.squareButtons = {}
        self.buttons = {}
        self.widgets = {}
        self.a.addLayout(self.merge_all_layouts(rows, columns))


    def merge_all_layouts(self, rows, colums):

        self.hide_everything()
        self.clear_widgets()

        layout_of_square_buttons = self.create_maze(rows, colums)
        placing_buttons = self.create_right_side_buttons()
        lsb = self.create_left_side_buttons(rows)

        h_layout = QHBoxLayout()
        h_layout.addStretch(7)
        h_layout.addLayout(placing_buttons)
        h_layout.addStretch(2)
        h_layout.addLayout(layout_of_square_buttons)
        h_layout.addStretch(2)
        h_layout.addLayout(lsb)
        h_layout.addStretch(7)

        v_layout = QVBoxLayout()
        v_layout.addStretch(10)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(1)
        v_layout.addLayout(self.createBottomLayout())
        v_layout.addStretch(10)

        return v_layout

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
                button.setAccessibleName(str(i) + "-" + str(j))
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
        v_layout.addStretch(32)
        for color, text in [("green", "Place A"), ("orange", "Place B"), ("brown", "Place/Remove Walls")]:

            button = QPushButton(text)

            button.setFixedWidth(240)

            button.setStyleSheet(button_stylesheet.format(color, color))

            button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

            button.setAccessibleName(text)
            self.buttons[button.accessibleName()] = button

            v_layout.addWidget(self.buttons[button.accessibleName()])
            v_layout.addStretch(10)
        v_layout.addStretch(22)
        return v_layout

    def create_left_side_buttons(self, size_of_maze):

        h_layout = QHBoxLayout()
        h_layout.addStretch()

        text = "Size: "
        label = QLabel(text)
        self.widgets[text] = label

        self.combo_box = QComboBox()

        for i in range(3, 15):
            self.combo_box.addItem(str(i))

        self.combo_box.setCurrentIndex(size_of_maze - 3)
        self.combo_box.setAccessibleName(text + "combo")

        self.widgets[text + "combo"] = self.combo_box

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
    
    def createBottomLayout(self):

        h_layout = QHBoxLayout()
        h_layout.addStretch()

        text = "Predrawn Mazes: "
        label = QLabel(text)
        self.widgets["predrawnMazesLabel"] = label

        self.maze_combobox = QComboBox()

        self.widgets["predrawnMazesCombo"] = self.combo_box

        h_layout.addWidget(label)
        h_layout.addWidget(self.maze_combobox)
        h_layout.addStretch()
        return h_layout
        

    def hide_everything(self):
        for i in self.squareButtons.keys():
            self.squareButtons[i].hide()

        for i in self.buttons.keys():
            self.buttons[i].hide()

        for i in self.widgets.keys():
            self.widgets[i].hide()

    def clear_widgets(self):
        # Remove all widgets/layouts from main layout
        while self.a.count():
            item = self.a.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            layout = item.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
        self.squareButtons.clear()
        self.widgets.clear()
        self.buttons.clear()
        self.change = ""

