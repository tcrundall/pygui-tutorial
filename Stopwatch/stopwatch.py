"""
Stopwatch

Challenges
- get display to update every second, (built in "clock" concept?)
- change button layout (start vs stop/lap) based on state
- keep log of data, and convert into layout dynamically

Three states
Fresh:
just a start button

Running:
current duration
stop | lap
table of previous laps

Stopped:
paused time
reset
table of previous laps
"""
import PySimpleGUI as sg
from time import time


def create_window():
    sg.theme('black')
    BUTTON_COLOR = '#FF0000'
    PRESSED_COLOR = '#FFFFFF'

    layout = [
        [
            sg.Push(),
            sg.Image(
                'cross.png',
                key='-CLOSE-',
                pad=0,
                enable_events=True
            )
        ],
        [sg.VPush()],
        [sg.Text('', font='Young 50', key='-TIME-')],
        [
            sg.Button(
                'Start',
                button_color=(PRESSED_COLOR, BUTTON_COLOR),
                border_width=0,
                key='-STARTSTOP-',
            ),
            sg.Button(
                'Lap',
                button_color=(PRESSED_COLOR, BUTTON_COLOR),
                border_width=0,
                key='-LAP-',
                visible=False,
            ),
        ],
        [sg.Column([[]], key='-LAPCOL-')],
        [sg.VPush()],
    ]

    window = sg.Window(
        title='Stopwatch',
        layout=layout,
        size=(300, 300),
        no_titlebar=True,
        element_justification='center',
    )

    return window


if __name__ == '__main__':
    laps = [10, 20]
    
    window = create_window()

    running = False
    start_time = None
    laps = 1
    while True:
        event, values = window.read(timeout=10)

        if running:
            elapsed_time = round(time() - start_time, 1)
            window['-TIME-'].update(elapsed_time)

        if event in (sg.WIN_CLOSED, '-CLOSE-'):
            break

        if event == '-STARTSTOP-':
            if running:
                window['-STARTSTOP-'].update('Reset')
                window['-LAP-'].update(visible=False)
                running = False
            else:
                if start_time:
                    window.close()
                    window = create_window()
                    laps = 1
                    start_time = None

                else:
                    start_time = time()
                    window['-STARTSTOP-'].update('Stop')
                    window['-LAP-'].update(visible=True)
                    running = True

        if event == '-LAP-':
            window.extend_layout(
                window['-LAPCOL-'],
                [[
                    sg.Text(laps),
                    sg.VSeparator(),
                    sg.Text(elapsed_time),
                ]]
            )
            laps += 1

    window.close()
