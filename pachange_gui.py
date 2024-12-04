import PySimpleGUI as sg
import numpy as np
import pa_lib

def make_window():
    NAME_SIZE = 23-7


    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

    layout_r=[]
    layout_l=[
    ]

    sg.theme('Reddit')
    
    # Note - LOCAL Menu element is used (see about for how that's defined)
    layout = [
                [sg.T('PA Test postscript', font='_ 14', justification='c', expand_x=True)],
                [sg.Text('Файл gcode')],
                [sg.Input(enable_events = True, k = 'fileselected'), sg.FileBrowse(file_types=(('GCode Files', '*.gcode'),('ALL Files', '*.* *'),),k="fileselected",enable_events = True)],
                [sg.Text(k="instances")],
                [sg.Text(k='problems')],
                [name('Начальный ПА'),sg.Input('0.05', size=(10,1), key='-START_PA-', enable_events=True)],
                [name('Конечный ПА'),sg.Input('0.15', size=(10,1), key='-END_PA-', enable_events=True)],
                [name('Шаг изменений'),sg.T(k="steptext")],
                [name('Фактические ПА'),sg.Listbox([],k="steps", size=(15,5))],
                [sg.Text(k='output')],
                [sg.Button('Обработать', k="generateButton", disabled = True, enable_events=True)]
                ]
    
    window = sg.Window('PA Test postscript', layout, finalize=True)


    return window

window = make_window()
GcA = pa_lib.GCodeAnalyze()
Extruder = pa_lib.Extruder()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in ('-START_PA-','-END_PA-') and values[event]:
        try:
            in_as_float = float(values[event])
        except:
            if len(values[event]) == 1 and values[event][0] == '-':
                continue
            window[event].update(values[event][:-1])
        GcA.calcStep(values['-START_PA-'],values['-END_PA-'])
        window['steptext'].update(GcA.stepPA)
        window['steps'].update(GcA.steps)
    if event == "fileselected":
        GcA.file_input = values[event]
        GcA.analyzeFile()
        window['instances'].update(f"Количество тестовых блоков {GcA.instances}")
        GcA.calcStep(values['-START_PA-'],values['-END_PA-'])
        window['steptext'].update(GcA.stepPA)
        window['steps'].update(GcA.steps)
        window['problems'].update("")
        problems = GcA.checkConditions(True)
        window['problems'].update(problems)
        window['generateButton'].update(disabled = len(problems)>0)
    if event=='generateButton':
        GcC = pa_lib.GCodeChange()
        GcC.Change(GcA,Extruder)
        window['output'].update(GcC.output_filename)
        pass
window.close()