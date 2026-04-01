from typing import List


def hanoi_tower(n: int) -> None:
    """
    Solves the Tower of Hanoi puzzle for 'n' disks using nested functions.

    The function prints the state of all three towers at the 
    beginning and after each move.
    Disks are represented by integers (larger number = larger disk).
    Empty positions are shown as '_'.

    Hanoi Tower Solution for n = 3:
    0:321:___:___
    1:32_:1__:___
    2:3__:1__:2__
    3:3__:___:21_
    4:___:3__:21_
    5:1__:3__:2__
    6:1__:32_:___
    7:___:321:___
    """

    def print_tower(tower) -> None:
        """
        Prints one tower as a string of disk numbers, using '_' for empty level.
        """
        ...

    def print_towers() -> None:
        """
        Prints the step number and current state of all three towers.
        """
        ...

    def move(n, tower_from, tower_to, tower_aux):
        """
        Recursive function to move 'n' disks from tower_from to tower_to
        using tower_aux as auxiliary tower.
        """
        ...

    ...

# Alternatively:
class HanoiTower:
    """
    Object-oriented implementation of the Tower of Hanoi puzzle.
    """
    def __init__(self, n: int) -> None:
        """
        Initialize towers and start the solution.

        Tower A contains n disks (largest at bottom),
        towers B and C are empty.

        Initializes a step counter and prints the initial state.
        Then starts the recursive algorithm to solve the puzzle.
        """

        ...

    def _print_tower(self, tower: List[int]) -> None:
        """
        Prints one tower as a string of disk numbers, using '_' for empty level.
        """
        ...

    def print_towers(self) -> None:
        """
        Prints the step number and current state of all three towers.
        """
        ...

    def _move(self, n, tower_from, tower_to, tower_aux) -> None:
        """
        Recursive function to move 'n' disks from t_from to t_to
        using t_aux as auxiliary tower.
        """
        ...

if __name__ == "__main__":
    for n in range(1, 6):
        ...
        # HanoiTower(n)
        # hanoi_tower(n)

    print("test ok")