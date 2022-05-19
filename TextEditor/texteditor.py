import PySimpleGUI as sg
from pathlib import Path

smileys = [
    'happy', [':)', 'xD', ':D', '<3'],
    'sad', [':(', 'T_T'],
    'other', [':3'],
]
smiley_events = [s for smile_set in smileys[1::2] for s in smile_set]

menu_layout = [
    ['File', ['Open', 'Save', '---', 'Exit']],
    ['Tools', ['Word Count']],
    ['Add', smileys],
]

sg.theme('GrayGrayGray')

layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('Untitled', key='-DOCNAME-')],
    [sg.Multiline(no_scrollbar=True, size=(40, 30), key='-TEXTBOX-')]
]

if __name__ == '__main__':
    window = sg.Window("TextEditor", layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Open':
            file_path = sg.popup_get_file('open', no_window=True)
            if file_path:
                file = Path(file_path)
                window['-DOCNAME-'].update(file.name)
                # print(file.read_text())
                window['-TEXTBOX-'].update(file.read_text())

        if event == 'Save':
            file_path = sg.popup_get_file(
                'Save as',
                no_window=True,
                save_as=True
            )
            if file_path.split('.')[-1] != 'txt':
                file_path += '.txt'

            file = Path(file_path)
            file.write_text(values['-TEXTBOX-'])
            window['-DOCNAME-'].update(file.name)

        if event == 'Word Count':
            full_text = values['-TEXTBOX-']
            clean_text = full_text.split()
            wordcount = len(clean_text)
            char_count = len(''.join(clean_text))
            sg.popup('words: %s\ncharacters: %s'%(wordcount, char_count))

        if event in smiley_events:
            # # Tutorial suggestion:
            # full_text = values['-TEXTBOX-']
            # full_text += event
            # window['-TEXTBOX-'].update(full_text)

            # Using "tkinter" method
            # https://github.com/PySimpleGUI/PySimpleGUI/issues/3644
            window['-TEXTBOX-'].Widget.insert("insert", event)

    window.close()
