from FrameView import FrameView
from FrameModel import *
import styles
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QApplication, QInputDialog
import sys


class FrameController:


    def __init__(self, view: FrameView, model: FrameModel):
        self.view = view
        self.model = model

        self.assign_command_to_squares()
        self.enable_square_buttons()
        self.setup_buttons()


    def reset(self, rows=7, columns=7):
        self.view.reset(rows, columns)
        self.model.reset(rows, columns)
        print(self.view.buttons)

        self.assign_command_to_squares()
        self.enable_square_buttons()
        self.setup_buttons()


    def assign_command_to_squares(self):
        for squareButton in self.view.squareButtons.values():
            key = squareButton.accessibleName()
            squareButton.clicked.connect(
                lambda: self.change_square_button(self.view.squareButtons[key]))

    def enable_square_buttons(self):
        for i in self.view.squareButtons.keys():
            self.view.squareButtons[i].setEnabled(True)

    def disable_square_buttons(self):
        for i in self.view.squareButtons.keys():
            self.view.squareButtons[i].setEnabled(False)

    def change_square_button(self, button: QPushButton):
        name = button.accessibleName()
        pos = name.split("-")
        pos = (int(pos[0]), int(pos[1]))
        if self.model.placingBlock == A:
            if self.model.placeOfA != (-1, -1): # if A is already placed
                self.view.squareButtons[self.model.get_str(self.model.placeOfA)].setStyleSheet(styles.styleWall)
                self.view.squareButtons[self.model.get_str(self.model.placeOfA)].setText("")
            self.view.squareButtons[name].setText("A")
            self.view.squareButtons[name].setStyleSheet(styles.styleA)
            self.model.place_A(pos[0], pos[1])
        elif self.model.placingBlock == B:
            if self.model.placeOfB != (-1, -1): # if B is already placed
                self.view.squareButtons[self.model.get_str(self.model.placeOfB)].setStyleSheet(styles.styleWall)
                self.view.squareButtons[self.model.get_str(self.model.placeOfB)].setText("")
            self.view.squareButtons[name].setText("B")
            self.view.squareButtons[name].setStyleSheet(styles.styleB.format("orange"))
            self.model.place_B(pos[0], pos[1])
        elif self.model.placingBlock == WALL:
            if (self.view.squareButtons[name].palette().window().color().name() == "#808080" or button.text() == 'A'
                    or button.text() == "B"):
                self.view.squareButtons[name].setStyleSheet(styles.styleEmpty)
                self.model.place_empty(pos[0], pos[1])
            else:
                self.view.squareButtons[name].setStyleSheet(styles.styleWall)
                self.model.place_wall(pos[0], pos[1])

    def setup_buttons(self):
        for button in self.view.squareButtons.values():
            button.clicked.connect(
                lambda checked, arg=button: self.change_square_button(arg))
        self.view.buttons["Place A"].clicked.connect(self.placeA)
        self.view.buttons["Place B"].clicked.connect(self.placeB)
        self.view.buttons["Place/Remove Walls"].clicked.connect(self.place_walls)
        for button in [self.view.buttons["DFS"], self.view.buttons["BFS"]]:
            button.clicked.connect(
                lambda checked, arg=button.text(): self.dfs_and_bfs_button(arg))
        self.view.combo_box.currentIndexChanged.connect(self.create_new_maze)
        self.view.buttons["Clear Maze"].clicked.connect(self.create_new_maze)
        self.view.buttons["solve"].clicked.connect(self.solve_maze)

        #set up predrawn mazes combo box 
        self.view.maze_combobox.addItem("Custom Maze")
        self.view.maze_combobox.model().item(0).setEnabled(False)
        names = self.get_predrawn_maze_names()
        for i in names:
            self.view.maze_combobox.addItem(i)
        if self.model.preDrawnedMaze:
            index = self.view.maze_combobox.findText(self.model.maze_name)
            if index != -1:
                self.view.maze_combobox.setCurrentIndex(index)

        self.view.maze_combobox.currentIndexChanged.connect(self.load_predrawn_maze)

    def get_predrawn_maze_names(self):
        return self.model.get_all_predrawn_maze_names()

    def placeA(self):
        self.model.placingBlock = A
        self.enable_square_buttons()

    def placeB(self):
        self.model.placingBlock = B
        self.enable_square_buttons()

    def place_walls(self):
        self.model.placingBlock = WALL
        self.enable_square_buttons()

    def create_new_maze(self):
        rows = int(self.view.widgets["Size: combo"].currentText())
        columns = int(self.view.widgets["Size: combo"].currentText())
        print(rows, columns)
        print(self.view.buttons)
        self.reset(rows, columns)

    def load_predrawn_maze(self):
        
        name = self.view.maze_combobox.currentText()
        rows= columns = self.model.get_row_from_name(name)
        self.reset(rows, columns)
        self.model.load_maze_from_file(name)
        maze = self.model.maze

        for i in range(self.model.rows):
            for j in range(self.model.columns):
                if maze[i][j] == WALL:
                    self.view.squareButtons[f"{i}-{j}"].setStyleSheet(styles.styleWall)
                    self.view.squareButtons[f"{i}-{j}"].setText("")
                elif maze[i][j] == EMPTY:
                    self.view.squareButtons[f"{i}-{j}"].setStyleSheet(styles.styleEmpty)
                    self.view.squareButtons[f"{i}-{j}"].setText("")
                elif maze[i][j] == A:
                    self.view.squareButtons[f"{i}-{j}"].setStyleSheet(styles.styleA)
                    self.view.squareButtons[f"{i}-{j}"].setText("A")
                elif maze[i][j] == B:
                    self.view.squareButtons[f"{i}-{j}"].setStyleSheet(styles.styleB.format("orange"))
                    self.view.squareButtons[f"{i}-{j}"].setText("B")



    def ask_maze_name(self):
        name, ok = QInputDialog.getText(self.view, "Save Maze", "Enter maze name:")
        if ok and name:
            return name
        return None

    def save_maze(self):
        name = self.ask_maze_name()
        
        if not name:
            return
        
        self.model.save_maze_to_file(name)

        
    def dfs_and_bfs_button(self, name: str):
        if self.view.buttons[name].palette().window().color().name() == "#808080":
            self.view.buttons[name].setStyleSheet(styles.styleTrueDfs)
            name1 = 'B' if name[0] == 'D' else 'D'
            name1 += name[1:3]
            self.view.buttons[name1].setStyleSheet(styles.styleFalseDfs)
            self.model.DFS = (name == 'DFS')

    def sleep(self, time):
        loop = QEventLoop()
        QTimer.singleShot(time * 100, loop.quit)
        loop.exec_()

    def showSolution(self, solution: list):
        for i in solution:
            self.view.squareButtons[str(i[0]) + "-" + str(i[1])].setStyleSheet(styles.styleYellow)
            self.sleep(5)
        self.view.squareButtons[str(self.model.placeOfB[0]) + "-" + str(self.model.placeOfB[1])].setStyleSheet(styles.styleB.format("green"))

    def solve_maze(self):
        solution = self.model.solve_maze()
        print(solution)
        if solution is None:
            self.view.show_message("No Solution", "There is no solution for this maze.")
        else:
            self.showSolution(solution)
        self.disable_square_buttons()
        self.view.buttons["solve"].setText("Save Maze")
        self.view.buttons["solve"].clicked.disconnect()
        self.view.buttons["solve"].clicked.connect(lambda: self.save_maze())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = FrameView()
    model = FrameModel()
    game = FrameController(view, model)
    sys.exit(app.exec_())



























