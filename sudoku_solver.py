from copy import deepcopy
from threading import Thread


class Field:
    def __init__(self, field):
        self.rows = field
        self.exs_c: tuple[set] = tuple({num for num in col if num != 0} for col in list(map(list, zip(*self.rows))))
        self.nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        self.squares = []
        for it in range(9):
            if not it % 3:
                self.squares.extend(([], [], []))
            r = self.rows[it]
            calc = (it//3+1)*3
            self.squares[calc - 3].extend(r[:3])
            self.squares[calc - 2].extend(r[3:6])
            self.squares[calc - 1].extend(r[6:])

    def srt(self):
        assert all([
            all(
                map(
                    lambda sq: not set(sq) - set(range(10)) and
                    all(map(lambda a: sq.count(a) == 1, [arg for arg in sq if arg])),
                    arr
                )
            )
            for arr in (self.rows, zip(*self.rows), self.squares)
        ])

    @staticmethod
    def get_square(y, x):
        return y // 3 * 3 + x // 3

    def replace(self, y, x, new):
        self.rows[y][x] = new
        self.exs_c[x].add(new)
        self.squares[self.get_square(y, x)].append(new)

    def nr(self, ln, p, v):
        self.rows[ln][p] = v
        return deepcopy(self.rows)

    def __call__(self):
        ch_ = True
        while ch_:
            ch_ = False
            psb = []
            for l_ind, line in enumerate(self.rows):
                if all(line):
                    continue
                for p_ind, pos in enumerate(line):
                    if not pos:
                        variations = tuple(self.nums - set(line) - self.exs_c[p_ind] - set(
                            self.squares[self.get_square(l_ind, p_ind)]
                        ))
                        if not variations:
                            return False
                        if len(variations) == 1:
                            self.replace(l_ind, p_ind, variations[0])
                            ch_ = True
                        elif not psb:
                            psb.extend((l_ind, p_ind, variations))
        if not psb:
            return self.rows
        for copy_ in psb[2]:
            result_ = Field(self.nr(psb[0], psb[1], copy_))()
            if result_:
                return result_
        return False


def sudoku_solver(field):
    assert len([arg for line in field for arg in line]) == 81

    f = Field(tuple(field))
    Thread(target=f.srt).run()
    f = f()
    assert f

    return f
