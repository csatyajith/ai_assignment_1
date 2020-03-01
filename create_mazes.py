import pickle

from maze import Maze


def create_mazes():
    mazes = []
    for _ in range(50):
        mazes.append(Maze(101, 101))
    with open("mazes", "wb") as mazes_file:
        pickle.dump(mazes, mazes_file)


if __name__ == '__main__':
    create_mazes()
