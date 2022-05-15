import PySimpleGUI as sg

B_SIZE = (4, 2)
# WIDE_BUTTON_SIZE = (10, 3)


def button(label, size=None, expand_x=False):
    key = '-%s-'%(label.upper())
    if size:
        return sg.Button(label, key=key, size=size)
    else:
        return sg.Button(label, key=key, expand_x=expand_x)


def create_window(theme):
    sg.theme(theme)
    sg.set_options(font='Franklin 14', button_element_size=B_SIZE)
    layout = [
        [sg.Text(
            '',
            key='-DISPLAY-',
            font='Franklin 26',
            expand_x=True,
            justification='right',
            right_click_menu=theme_menu)],
        [
            button('Clear', size=None, expand_x=True),
            button('Equals', size=None, expand_x=True)],
        [button(label, size=B_SIZE) for label in '789+'],
        [button(label, size=B_SIZE) for label in '456-'],
        [button(label, size=B_SIZE) for label in '123*'],
        (
            [button('0', expand_x=True)]
            + [button(label, size=B_SIZE) for label in './']
        ),
    ]

    return sg.Window('Calculator', layout, finalize=True)


num_events = {'-%s-'%d: str(d) for d in range(10)}
num_events['-.-'] = '.'

oper_events = {'-%s-'%s: s for s in '+-*/'}

theme_menu = ['menu', ['dark', 'LightGrey1', 'DarkGrey8', 'random']]

window = create_window(theme='dark')
# theme_changed = False
current_num = []
full_operation = []
display = ''
while True:
    event, values = window.read()
    # if theme_changed:
    #     window['-DISPLAY-'].update(display)
    #     theme_changed = False

    if event == sg.WIN_CLOSED:
        break

    if event in num_events:
        current_num.append(num_events[event])
        window['-DISPLAY-'].update(''.join(current_num))

    if event in oper_events:
        full_operation.append(''.join(current_num))
        full_operation.append(oper_events[event])
        current_num = []

    if event == '-EQUALS-':
        if not full_operation:
            continue

        full_operation.append(''.join(current_num))
        result = eval(''.join(full_operation))
        window['-DISPLAY-'].update(str(result))
        current_num = []
        full_operation = []

    if event == '-CLEAR-':
        current_num = []
        full_operation = []
        window['-DISPLAY-'].update('')

    if event in theme_menu[1]:
        display = window['-DISPLAY-'].get()
        window.close()
        window = create_window(theme=event)
        current_num = []
        full_operation = []

window.close()
