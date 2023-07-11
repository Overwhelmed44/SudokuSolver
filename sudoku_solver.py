from copy import deepcopy


class NoSolutionException(Exception):
    ...


class MultipleSolutionsException(Exception):
    ...


class InvalidGridException(Exception):
    ...


class SudokuSolver:
    multiple_solutions = False

    def __init__(self, rows, cols=None, squares=None, changes=None):
        self.rows = rows
        self.cols = cols if cols else list(map(list, zip(*rows)))
        if squares:
            self.squares = squares
        else:
            self.squares = [[] for _ in range(9)]
            for it in range(9):
                r = rows[it]
                for n in range(3):
                    n3 = n * 3
                    self.squares[it // 3 * 3 + n].extend(r[n3:n3 + 3])
        self.r19 = set(range(1, 10))
        self.r09 = set(range(10))

        self.changes = changes if changes else []

    @staticmethod
    def get_square(y, x):
        return y // 3 * 3 + x // 3, y % 3 * 3 + x % 3

    def assert_(self):
        if len([arg for line in self.rows for arg in line]) != 81 or not all([
            all(map(lambda sq: not set(sq) - self.r09 and (
                all(map(lambda a: sq.count(a) == 1, [arg for arg in sq if arg]))
            ), arr)) for arr in (self.rows, self.cols, self.squares)
        ]) or (not SudokuSolver.multiple_solutions and len(
            [arg for line in self.rows for arg in line if arg]) < 17): raise InvalidGridException()

    def replace(self, y, x, val):
        self.rows[y][x] = val
        self.cols[x][y] = val
        cords = self.get_square(y, x)
        self.squares[cords[0]][cords[1]] = val

    def variations(self, y, x):
        return self.r19 - set(self.rows[y]) - set(self.cols[x]) - set(self.squares[self.get_square(y, x)[0]])

    def new(self, y, x, val):
        self.replace(y, x, val)
        temp = self.changes.copy()
        temp.append((y, x))
        return deepcopy(self.rows), deepcopy(self.cols), deepcopy(self.squares), temp

    def initial_loop(self):
        for l_ind, line in enumerate(self.rows):
            if all(line):
                continue
            for p_ind, pos in enumerate(line):
                if pos:
                    continue
                variations = self.variations(l_ind, p_ind)
                if not variations:
                    raise NoSolutionException
                if len(variations) == 1:
                    self.replace(l_ind, p_ind, *variations)
                    self.changes.append((l_ind, p_ind))

    def __call__(self):
        while self.changes:
            change = self.changes.pop(0)
            y, x = change

            for ind, arg in enumerate(self.rows[y]):
                if arg:
                    continue
                variations = self.variations(y, ind)
                if not variations:
                    return False
                if len(variations) == 1:
                    self.replace(y, ind, *variations)
                    self.changes.append((y, ind))

            for ind, arg in enumerate(self.cols[x]):
                if arg:
                    continue
                variations = self.variations(ind, x)
                if not variations:
                    return False
                if len(variations) == 1:
                    self.replace(ind, x, *variations)
                    self.changes.append((ind, x))

            square = self.get_square(y, x)[0]
            for ind, arg in enumerate(self.squares[square]):
                if arg:
                    continue
                y = square // 3 * 3 + ind // 3
                x = square % 3 * 3 + ind % 3
                variations = self.variations(y, x)
                if not variations:
                    return False
                if len(variations) == 1:
                    self.replace(y, x, *variations)
                    self.changes.append((y, x))

        if all(map(all, self.rows)):
            return self.rows

        blank = []
        for l_ind, line in enumerate(self.rows):
            if all(line):
                continue
            ind = line.index(0)
            blank.extend((l_ind, ind, self.variations(l_ind, ind)))
            break

        single = False
        for var in blank[2]:
            res = SudokuSolver(*self.new(blank[0], blank[1], var))()
            if res:
                if SudokuSolver.multiple_solutions:
                    return res
                if single:
                    raise MultipleSolutionsException()
                single = res
        return single


def solve(grid):
    SudokuSolver.multiple_solutions = True
    obj = SudokuSolver(grid)
    obj.assert_()
    obj.initial_loop()
    obj = obj()
    if not obj:
        raise NoSolutionException()
    return obj
