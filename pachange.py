import pa_lib
import os.path

startPA = 0.05
endPA = 0.15

# выбор файла
file_names = []
for file_name in [f for f in os.listdir('input\\') if f.endswith(".gcode")]:
    file_names.append(file_name)
for n, file in enumerate(file_names):
    print (str(n)+" - "+file.split('.ini')[0])

if(len(file_names)==0):
    print("Нет файлов для выбора")
    raise SystemExit
if(len(file_names)==1):
    file_input = 'input\\'+file_names[0]
    print("Найден один файл для обработки")
    print(file_input)
else:
    file_input =  file_names[int(input("Выберите файл для обработки: "))]

GcA = pa_lib.GCodeAnalyze()
Extruder = pa_lib.Extruder()

# анализ файла и выбор параметров

GcA.file_input = 'input\\'+file_input
GcA.analyzeFile()
GcA.checkConditions()
GcA.calcStep(startPA,endPA)
GcA.askParams()
GcC = pa_lib.GCodeChange()
GcC.Change(GcA,Extruder)
print(f"Файл обработан. Результирующий файл {GcC.output_filename}")
input("Нажмите Enter для завершения")
