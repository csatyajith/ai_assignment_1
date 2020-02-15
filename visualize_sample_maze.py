from maze import MazeVisualizer, Maze

if __name__ == '__main__':
    n_rows = 10  # 10 is better for visualization Change to 51 for project
    n_cols = 10
    maze_1 = Maze(n_rows, n_cols)

    # print on console
    for r in maze_1.maze:
        print([0 if cell.blocked else 1 for cell in r])

    # plot on matplotlib
    maze_vis = MazeVisualizer(maze_1)
    maze_vis.show_maze()
