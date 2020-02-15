from maze import Maze


def test_blocked_cell_percentage():
    blocked = 0
    maze_1 = Maze(51, 51)
    for r in maze_1.maze:
        for cell in r:
            if cell.blocked:
                blocked += 1
    assert 0.26 < (blocked / (51 * 51)) < 0.34
