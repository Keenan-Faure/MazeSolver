from tkinter import Tk, BOTH, Canvas
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter import Menu

import random
import time

#Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Line
class Line:
    def __init__(self, first_point: Point, second_point: Point):
        self.first_point  = first_point
        self.second_point = second_point

    def draw(self, Canvas: Canvas, fill_color: str):
        Canvas.create_line(
            # adding 2 because the width is initially 1
            # hence if the point is located < width length it 
            # will not show on Canvas
            (self.first_point.x + 3), (self.first_point.y + 3), 
            (self.second_point.x + 3), (self.second_point.y + 3), 
            fill=fill_color, width=1
        )
        Canvas.pack()

#Window
class Window(Tk):

    # private root Tk
    # private canvas Canvas
    # private running Boolean
    def __init__(self, width: int, height: int):
        super().__init__()

        self.__root = Tk()
        self.__root.config(width=width, height=height)
        self.__root.title("Maze Runner Solution")

        #Canvas
        self.__canvas = Canvas(self.__root,bg = "black",height=height, width=width)
        self.__canvas.pack()
        self.__running = False

        #connects your close method to the "delete window" action
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        #Optional menu
        # menu = Menu(self.__root)
        # self.__root.config(menu=menu)

        # file = Menu(menu)
        # file.add_command(label="Exit", command=self.close)

        # menu.add_cascade(label="File", menu=file)

        # edit = Menu(menu)
        # edit.add_command(label="Undo")

        # menu.add_cascade(label="Edit", menu=edit)
    
    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()
    
    def wait_for_close(self):
        self.__running = True

        #continuously updates the windows
        while(self.__running == True):
            self.redraw()
    
    def close(self):
        # answer = askokcancel(
        #     title='Confirmation',
        #     message='Close application?',
        #     icon=WARNING)

        # #closes the application if 'Yes'
        # if answer:
        #     showinfo(
        #         title='Termination Status',
        #         message='The app was closed successfully')
        self.__running = False
    
    def draw_line(self, Line: Line, fill_color):
        Line.draw(self.__canvas, fill_color)
    
    def get_canvas(self):
        return self.__canvas

#Cell
class Cell:
    def __init__(
            self, 
            has_left_wall, 
            has_right_wall, 
            has_top_wall, 
            has_bottom_wall, 
            _x1, 
            _x2, 
            _y1, 
            _y2, 
            _win: Window=None
        ):

        self.has_left_wall   = has_left_wall
        self.has_right_wall  = has_right_wall
        self.has_top_wall    = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1             = _x1
        self._x2             = _x2
        self._y1             = _y1
        self._y2             = _y2
        self._win            = _win
        self.visited         = False
    
    def draw_move(self, to_cell, undo=False):
        #gets mid points for two cells
        p1_mid_point = self.calc_midpoint()
        to_cell_mid_point = to_cell.calc_midpoint()

        #creates and draws the lines
        line = Line(p1_mid_point,to_cell_mid_point)
        if(undo == False):
            line.draw(self._win.get_canvas(), "red")
        else:
            line.draw(self._win.get_canvas(), "grey")

    def update_points(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def calc_midpoint(self):
        x_1 = (self._x1 + self._x2) / 2
        y_1 = (self._y1 + self._y2) / 2
        mid_point = Point(x_1, y_1)
        return mid_point
        
    def draw(self, x1, y1, x2, y2):
        self.update_points(x1, y1, x2, y2)
        if(self.has_left_wall):
            first_point = Point(x1, y2)
            second_point = Point(x1, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "red")
        else:
            first_point = Point(x1, y2)
            second_point = Point(x1, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "black")

        if(self.has_right_wall):
            first_point = Point(x2, y2)
            second_point = Point(x2, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "red")
        else:
            first_point = Point(x2, y2)
            second_point = Point(x2, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "black")

        if(self.has_top_wall):
            first_point = Point(x2, y1)
            second_point = Point(x1, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "red")
        else:
            first_point = Point(x2, y1)
            second_point = Point(x1, y1)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "black")
            
        if(self.has_bottom_wall):
            first_point = Point(x2, y2)
            second_point = Point(x1, y2)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "red")
        else:
            first_point = Point(x2, y2)
            second_point = Point(x1, y2)
            line = Line(first_point,second_point)
            line.draw(self._win.get_canvas(), "black")


class Maze:

    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win: Window=None,
            seed=None
        ):

        self.x1          = x1
        self.y1          = y1
        self.num_rows    = num_rows
        self.num_cols    = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win         = win
        self._cells      = []

        if(seed != None): seed = random.seed(seed)
        
        #calls function to create the maze
        self._create_cells()
    
    def _create_cells(self):
        cells = [[Cell(True, True, True, True, 0, 0, 0, 0, self.win) for x in range(self.num_rows)] for y in range(self.num_cols)]
        self._cells = cells

    def _draw_cell(self, i:int, j:int):
        x1_pos = ((i) * self.cell_size_x) + self.x1
        y1_pos = ((j) * self.cell_size_y) + self.y1
        x2_pos = ((i + 1) * self.cell_size_x) + self.x1
        y2_pos = ((j + 1) * self.cell_size_y) + self.y1
        self._cells[i][j].draw(x1_pos, y1_pos, x2_pos, y2_pos)
        self._animate()
    
    def _pos_to_pixel(self, i, j):
        if((i-self.x1) == 0):
            x_pos = 0
        else:
            x_pos = (i - self.x1) / (self.cell_size_x)

        if((j-self.y1) == 0):
            y_pos = 0
        else:
            y_pos = (j - self.y1) / (self.cell_size_y)
        return [int(x_pos), int(y_pos)]


    def _animate(self):
        self.win.redraw()
        time.sleep(0.2)

    def _break_entrance_and_exit(self):
        if(len(self._cells) > 0):
            row_len = len(self._cells) - 1
            col_len = len(self._cells[0]) - 1
            first_cell = self._cells[0][0]
            last_cell = self._cells[row_len][col_len]

            #left

            #breaks down walls then calls draw
            first_cell.has_left_wall = False
            first_cell.has_right_wall = False
            first_cell.has_top_wall = False
            first_cell.has_bottom_wall = False

            self._draw_cell(0,0)

            #left of first cell right wall must be removed
            first_cell = self._cells[1][0]
            first_cell.has_left_wall = False

            self._draw_cell(1,0)

            #bottom of first cell top wall must be removed
            first_cell = self._cells[0][1]
            first_cell.has_top_wall = False

            self._draw_cell(0,1)

            last_cell.has_left_wall = False
            last_cell.has_right_wall = False
            last_cell.has_top_wall = False
            last_cell.has_bottom_wall = False

            self._draw_cell(row_len,col_len)

            #top of last cells bottom must be removed
            last_cell = self._cells[row_len][col_len-1]
            last_cell.has_bottom_wall = False

            self._draw_cell(row_len,col_len-1)

            #right of last cells right must be removed
            last_cell = self._cells[row_len-1][col_len]
            last_cell.has_right_wall = False

            self._draw_cell(row_len-1,col_len)
    
    # returns the possible cells to visit
    # from the current cell
    # where x,y are the
    # adjacent cells positions (does checks) and
    # i,j are the iteration through the maze
    def get_possible_visit(self, i:int, j:int, x:int, y:int):
        possible_visit = []
        if(y-1 >= 0 and y-1 <= (j-1)): 
            if(self._cells[x][y-1].visited == False):
                cell_dict = {
                    "post": "top",
                    "cell": self._cells[x][y-1],
                    "x": x,
                    "y": y-1
                }
                possible_visit.append(cell_dict)

        if(x-1 >= 0 and x-1 <= (i-1)): 
            if(self._cells[x-1][y].visited == False):
                cell_dict = {
                    "post": "left",
                    "cell": self._cells[x-1][y],
                    "x": x-1,
                    "y": y
                }
                possible_visit.append(cell_dict)

        if(x+1 <= i-1 and x+1 >= 0): 
            if(self._cells[x+1][y].visited == False):
                cell_dict = {
                    "post": "right",
                    "cell": self._cells[x+1][y],
                    "x": x+1,
                    "y": y
                }
                possible_visit.append(cell_dict)

        if(y+1 <= j-1 and y+1 >= 0): 
            if(self._cells[x][y+1].visited == False):
                cell_dict = {
                    "post": "bottom",
                    "cell": self._cells[x][y+1],
                    "x": x,
                    "y": y+1
                }
                possible_visit.append(cell_dict)
        return possible_visit

    def _break_walls_r(self, i: int, j: int):
        self._cells[i-1][j-1].visited = True

        #adding reversed to start from the numbers entered
        possible_visit = []
        for x in reversed(range(i)):
            for y in reversed(range(j)):
                possible_visit = self.get_possible_visit(self.num_cols, self.num_rows, x, y)
                #no more places to go to
                if(len(possible_visit) == 0):
                    #draw current cell
                    self._cells[i-1][j-1].draw(
                        self._cells[i-1][j-1]._x1,
                        self._cells[i-1][j-1]._y1,
                        self._cells[i-1][j-1]._x2,
                        self._cells[i-1][j-1]._y2
                    )
                    return
                else:
                    #random direction
                    direction = int(random.randrange(len(possible_visit)))
                    self._break_down_walls_between(
                        self._cells[i-1][j-1],
                        possible_visit[direction]["cell"], 
                        possible_visit[direction]["post"]
                    )
                    self._break_walls_r(possible_visit[direction]["x"]+1,possible_visit[direction]["y"]+1)

    def _break_down_walls_between(self, this_cell: Cell, other_cell: Cell, direction: str):
        if(str(direction) == "top"):
            this_cell.has_top_wall = False
            x_y = self._pos_to_pixel(this_cell._x1, this_cell._y1)
            self._draw_cell(x_y[0], x_y[1])

            other_cell.has_bottom_wall = False
            x_y_2 = self._pos_to_pixel(other_cell._x1, other_cell._y1)
            self._draw_cell(x_y_2[0], x_y_2[1])

        elif(str(direction) == "left"):
            this_cell.has_left_wall = False
            x_y = self._pos_to_pixel(this_cell._x1, this_cell._y1)
            self._draw_cell(x_y[0], x_y[1])

            other_cell.has_right_wall = False
            x_y_2 = self._pos_to_pixel(other_cell._x1, other_cell._y1)
            self._draw_cell(x_y_2[0], x_y_2[1])

        elif(str(direction) == "right"):
            this_cell.has_right_wall = False
            x_y = self._pos_to_pixel(this_cell._x1, this_cell._y1)
            self._draw_cell(x_y[0], x_y[1])

            other_cell.has_left_wall = False
            x_y_2 = self._pos_to_pixel(other_cell._x1, other_cell._y1)
            self._draw_cell(x_y_2[0], x_y_2[1])

        elif(str(direction) == "bottom"):
            this_cell.has_bottom_wall = False
            x_y = self._pos_to_pixel(this_cell._x1, this_cell._y1)
            self._draw_cell(x_y[0], x_y[1])

            other_cell.has_top_wall = False
            x_y_2 = self._pos_to_pixel(other_cell._x1, other_cell._y1)
            self._draw_cell(x_y_2[0], x_y_2[1])
    
    def _reset_cells_visted(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    # determines if a wall exists between two cells
    # before moving
    # @return bool
    def _check_exist_wall(self, possible_cell: list, i: int, j:int):
        if(str(possible_cell["post"]) == "top"):
            if(self._cells[i][j].has_top_wall == False 
               and possible_cell["cell"].has_bottom_wall == False):
                return False

        elif(str(possible_cell["post"]) == "left"):
            if(self._cells[i][j].has_left_wall == False
               and possible_cell["cell"].has_right_wall == False):
                return False
                
        elif(str(possible_cell["post"]) == "right"):
            if(self._cells[i][j].has_right_wall == False
               and possible_cell["cell"].has_left_wall == False):
                return False

        elif(str(possible_cell["post"]) == "bottom"):
            if(self._cells[i][j].has_bottom_wall == False
               and possible_cell["cell"].has_top_wall == False):
                return False
        return True
                

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i: int, j: int):
        self._animate()
        self._cells[i][j].visited = True

        #for each direction available
        possible_visits = self.get_possible_visit(self.num_rows, self.num_cols, i, j)

        #End cell is the last cell at the bottom of the maze
        if(self._cells[i][j] == self._cells[self.num_rows-1][self.num_cols-1]):
            return True
        
        for index in range(len(possible_visits)):

            #check if there exists a wall between two cells

            #a wall exists, or it has been vistited already
            if(self._check_exist_wall(possible_visits[index], i, j)):
                self._cells[i][j].draw_move(possible_visits[index]["cell"], True)
                self._animate()

            #no wall, not visited and a cell exists in the direction
            else:

                #draw a move
                self._cells[i][j].draw_move(possible_visits[index]["cell"])
                #recursive call on first cell of possibilities
                if(self._solve_r(possible_visits[index]["x"], possible_visits[index]["y"])):
                    return True

        if(len(possible_visits) <= 0):
            return False

#Main function
def main():
    win = Window(500, 500)

    maze = Maze(5,5,7,7,50,50,win)

    for x in range(maze.num_rows):
            for y in range(maze.num_cols):
                maze._draw_cell(x, y)

    maze._break_entrance_and_exit()
    maze._break_walls_r(maze.num_rows, maze.num_cols)
    maze._reset_cells_visted()
    maze._animate()
    maze.solve()
    win.wait_for_close()

main()