import PySimpleGUI as sg

layout = [[sg.Text("Hello", key="-HELLO-"), sg.Button("World", key="-WORLD-")]]
window = sg.Window("Hello", layout=layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-WORLD-":
        window["-HELLO-"].update("World!")

window.close()
