import PySimpleGUI as sg
import numpy as np

layout = [[sg.Text("hello", key="-HELLO-"), sg.Button("world", key="-WORLD-")]]
window = sg.Window("Hello", layout=layout)

capitalized = False
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-WORLD-":
        if capitalized:
            new_str = str(np.char.lower(window["-HELLO-"].get()))
            capitalized = False
        else:
            new_str = str(np.char.capitalize(window["-HELLO-"].get()))
            capitalized = True

        window["-HELLO-"].update(new_str)

window.close()
