import PySimpleGUI as sg
import astropy.units as u
from astropy.units import imperial


def convert(value_in, conversion):
    if not value_in.isnumeric():
        return "Input is not numeric"

    unit1, unit2 = conversion.split(' to ')

    quant_in = float(value_in)*u.Unit(unit1)
    try:
        quant_out = quant_in.to(unit2)
    except u.UnitConversionError:
        return "Invalid conversion"

    return '%15s is %15s'%(quant_in, quant_out)


if __name__ == '__main__':
    imperial.enable()       # Needed for `mile` and `lb`

    conversions = [
        'cm to km',
        'km to mile',
        'kg to lb',
        'second to minute',
        'cm to minute'
    ]
    spin = sg.Spin([k for k in conversions], key='-SPIN-')
    layout = [
        [sg.Input(key="-INPUT-"), spin, sg.Button("Convert", key="-CONVERT-")],
        [sg.Text("", key="-TEXT-")],
    ]

    window = sg.Window(title="Converter", layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-CONVERT-":
            window["-TEXT-"].update(
                convert(values["-INPUT-"], values["-SPIN-"])
                )

    window.close()
