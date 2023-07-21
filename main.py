from sudoku_solver import solve
import PySimpleGUI as psg


class Window(psg.Window):
    def __init__(self):
        super().__init__(
            'SudokuSolver', [
                [[psg.Input(key=f'{ln}{n}', size=(2, 1), justification='center') for n in range(9)] for ln in range(9)],
                [psg.Button('Solve', size=13), psg.Button('Clear', expand_x=True)]
            ]
        )

    def update_all(self, lst=None):
        for ln in range(9):
            for n in range(9):
                if not lst:
                    self[f'{ln}{n}'].update('')
                else:
                    self[f'{ln}{n}'].update(lst[ln][n])


def main():
    psg.set_options(
        font='Calibri 18',
    )
    window = Window()
    while True:
        event, values = window.read()

        if event == psg.WINDOW_CLOSED:
            break

        if event == "Clear":
            window.update_all()
        elif event == "Solve":
            try:
                window.update_all(solve([[int(v) if (v := values[f'{ln}{n}']) else 0 for n in range(9)] for ln in range(9)]))
            except:
                psg.Popup('Error!')


if __name__ == '__main__':
    main()
