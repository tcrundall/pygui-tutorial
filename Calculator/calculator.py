import PySimpleGUI as sg

def button(label):
    return sg.Button(label, key='-%s-'%(label.upper()))

layout = [
    [sg.Text('', key='-DISPLAY-')],
    [sg.Button('Clear', key='-CLEAR-'), sg.Button('Equals', key='-EQUALS-')],
    [button(label) for label in '123+'],
    [button(label) for label in '456-'],
    [button(label) for label in '789*'],
    [button(label) for label in '0./'],
    # [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('+')],
    # [sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('-')],
    # [sg.Button('7'), sg.Button('8'), sg.Button('9'), sg.Button('*')],
    # [sg.Button('0'), sg.Button('.'), sg.Button('/')],
]

window = sg.Window('Calculator', layout)

num_events = {'-%s-'%d:str(d) for d in range(10)}

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event in num_events:
        display = window['-DISPLAY-'].get()
        window['-DISPLAY-'].update(display + num_events[event])

window.close()
