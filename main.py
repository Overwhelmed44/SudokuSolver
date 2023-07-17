from sudoku_solver import solve
import PySimpleGUI as psg


class Window:
    def __init__(self):
        self.window = psg.Window(
            'SudokuSolver', [
                [[psg.Input(key=f'{ln}{n}', size=(2, 1), justification='center') for n in range(9)] for ln in range(9)],
                [psg.Button('Solve', size=13), psg.Button('Clear', expand_x=True)]
            ]
        )

    def update(self, lst=None):
        for ln in range(9):
            for n in range(9):
                if not lst:
                    self.window[f'{ln}{n}'].update('')
                else:
                    self.window[f'{ln}{n}'].update(lst[ln][n])


def main():
    psg.set_options(
        font='Calibri 18',
    )
    window = Window()
    while True:
        event, values = window.window.read()

        if event == psg.WINDOW_CLOSED:
            break

        if event == "Clear":
            window.update()
        elif event == "Solve":
            try:
                window.update(solve([[int(v) if (v := values[f'{ln}{n}']) else 0 for n in range(9)] for ln in range(9)]))
            except:
                psg.Popup('Error!')


if __name__ == '__main__':
    main()
