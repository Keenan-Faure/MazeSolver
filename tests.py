import unittest
from maze import Maze
from maze import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )
        self.assertEqual(
            m1.win,
            None
        )
    
    def test_maze_init(self):
        maze = Maze(5, 5, 1, 1, 50, 50, None)

        self.assertEqual(
            maze.x1,
            5
        )
        self.assertEqual(
            maze.y1,
            5
        )
        self.assertEqual(
            len(maze._cells),
            1
        )
        self.assertEqual(
            len(maze._cells[0]),
            1
        )
        self.assertEqual(
            maze.cell_size_x,
            50
        )
        self.assertEqual(
            maze.cell_size_y,
            50
        )
        self.assertEqual(
            maze.win,
            None
        )
    
    def test_break_down_wall(self):
        win = Window(300, 300)

        maze = Maze(5, 5, 3, 3, 10, 10, win)
        maze._break_entrance_and_exit()

        self.assertFalse(maze._cells[0][0].has_bottom_wall)
        self.assertFalse(maze._cells[0][0].has_top_wall)
        self.assertFalse(maze._cells[0][0].has_left_wall)
        self.assertFalse(maze._cells[0][0].has_right_wall)

        row_len = len(maze._cells) - 1
        col_len = len(maze._cells[0]) - 1

        self.assertFalse(maze._cells[row_len][col_len].has_bottom_wall)
        self.assertFalse(maze._cells[row_len][col_len].has_top_wall)
        self.assertFalse(maze._cells[row_len][col_len].has_left_wall)
        self.assertFalse(maze._cells[row_len][col_len].has_right_wall)

    def test_reset_cells(self):
        win = Window(300, 300)

        maze = Maze(5, 5, 3, 3, 50, 50, win)

        maze._break_walls_r(maze.num_rows, maze.num_cols)
        maze._reset_cells_visted()

        self.assertFalse(maze._cells[0][0].visited)
        self.assertFalse(maze._cells[1][1].visited)
        self.assertFalse(maze._cells[2][2].visited)

    
if __name__ == "__main__":
    unittest.main()