import json


WALL = 1
EMPTY = 0
A = 2
B = 3


class FrameModel:



    def __init__(self, rows=7, columns=7):
        self.rows = rows
        self.columns = columns
        self.maze: list[list] = list(list())
        self.DFS = True  # default
        self.placeOfA = (-1, -1)
        self.placeOfB = (-1, -1)
        self.generate_maze()
        self.placingBlock = WALL
        self.preDrawnedMaze = False
        self.maze_name = ""
        print("here")

    def reset(self, rows=7, columns=7):
        self.rows = rows
        self.columns = columns
        self.maze.clear()
        self.generate_maze()
        self.placeOfA = (-1, -1)
        self.placeOfB = (-1, -1)
        self.placingBlock = WALL

    def generate_maze(self):
        self.maze = [[WALL for _ in range(self.columns)] for _ in range(self.rows)]
    
    def place_A(self, x: int, y: int):
        self.maze[x][y] = A
        self.placeOfA = (x, y)
    
    def place_B(self, x: int, y: int):
        self.maze[x][y] = B
        self.placeOfB = (x, y)
    
    def place_wall(self, x, y):
        self.maze[x][y] = WALL

    def place_empty(self, x, y):
        self.maze[x][y] = EMPTY

    def get_number(self, place:tuple) -> str:
        x,y = place
        return x * self.rows + y

    def get_str(self, place:tuple) -> str:
        x,y = place
        return f"{x}-{y}"

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.columns and self.maze[nx][ny] != WALL:
                neighbors.append((nx, ny))
        return neighbors
    
    def solve_maze(self):
        print(self.maze)
        
        if self.placeOfA == (-1, -1) or self.placeOfB == (-1, -1):
            return -1  # A or B not placed
        
        visited = list()
        nodeList = [(self.placeOfA[0], self.placeOfA[1])]
        x, y = self.placeOfA[0], self.placeOfA[1]

        while True:
            print(nodeList)    
            if not nodeList or self.maze[x][y] == B:
                break

            if self.DFS:
                x, y = nodeList.pop()
            else:
                x, y = nodeList.pop(0)

            if (x, y) in visited:
                continue
            visited.append((x, y))

            for i, j in self.get_neighbors(x, y):
                    nodeList.append((i, j))
        visited.append(self.placeOfB)
        return visited[1:]  # exclude starting point
    
    def get_all_maze_info(self) -> list[list]:

        with open("preDrawnMazes.json", "r") as f:
            data = json.load(f)
            return data["mazes"]

    def save_maze_to_file(self, name):
        mazes = self.get_all_maze_info()
        maze =  {
            "name": name,
            "width": self.columns,
            "height": self.rows,
            "grid": self.maze,
            "start": {
                "x": self.placeOfA[0],
                "y": self.placeOfA[1]
            },
            "end": {
                "x": self.placeOfB[0],
                "y": self.placeOfB[1]
            }
        }
        mazes.append(maze)
        with open("preDrawnMazes.json", "w") as f:
            json.dump({"mazes": mazes}, f)

    def load_maze_from_file(self, name):
        mazes = self.get_all_maze_info()
        for maze in mazes:
            if maze["name"] == name:
                self.rows = maze["height"]
                self.columns = maze["width"]
                self.maze = maze["grid"]
                self.placeOfA = (maze["start"]["x"], maze["start"]["y"])
                self.placeOfB = (maze["end"]["x"], maze["end"]["y"])
                self.preDrawnedMaze = True
                self.maze_name = name
                print("loaded", self.preDrawnedMaze, self.maze_name)
                return
    
    def get_all_predrawn_maze_names(self) -> list[str]:
        mazes = self.get_all_maze_info()
        names = []
        for maze in mazes:
            names.append(maze["name"])
        return names

    def get_row_from_name(self, name: str) -> int:
        mazes = self.get_all_maze_info()
        for maze in mazes:
            if maze["name"] == name:
                return maze["height"]
        return -1