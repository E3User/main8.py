import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from itertools import zip_longest
import xlsxwriter
from numpy.polynomial import Polynomial
# чтение данных из файла excel
df = pd.read_excel('approx.xlsx', sheet_name='Лист9')

# создание массива точек для построения графика
ud_linspace = np.linspace(0, 11,1000)
ud_linspace1 = np.linspace(0.6, 11,1000)

# интерполяция данных для каждой скорости и создание массивов для построения графика
stress_1_interp = np.interp(ud_linspace, df['ud_1.2mm/min'], df['stress_1.2mm/min'])
stress_2_interp = np.interp(ud_linspace, df['ud_2.2mm/min'], df['stress_2.2mm/min'])
stress_3_interp = np.interp(ud_linspace, df['ud_3.2mm/min'], df['stress_3.2mm/min'])

stress_4_interp = np.interp(ud_linspace, df['ud_4.10mm/min'], df['stress_4.10mm/min'])
stress_5_interp = np.interp(ud_linspace, df['ud_5.10mm/min'], df['stress_5.10mm/min'])
stress_6_interp = np.interp(ud_linspace, df['ud_6.10mm/min'], df['stress_6.10mm/min'])

stress_7_interp = np.interp(ud_linspace, df['ud_7.50mm/min'], df['stress_7.50mm/min'])
stress_8_interp = np.interp(ud_linspace, df['ud_8.50mm/min'], df['stress_8.50mm/min'])
stress_9_interp = np.interp(ud_linspace, df['ud_9.50mm/min'], df['stress_9.50mm/min'])

stress_10_interp = np.interp(ud_linspace, df['ud_10.650mm/min'], df['stress_10.650mm/min'])
stress_11_interp = np.interp(ud_linspace, df['ud_11.650mm/min'], df['stress_11.650mm/min'])
stress_12_interp = np.interp(ud_linspace, df['ud_12.650mm/min'], df['stress_12.650mm/min'])

stress_13_interp = np.interp(ud_linspace, df['ud_13.1000mm/min'], df['stress_13.1000mm/min'])
stress_14_interp = np.interp(ud_linspace1, df['ud_14.1000mm/min'], df['stress_14.1000mm/min'])
stress_15_interp = np.interp(ud_linspace1, df['ud_15.1000mm/min'], df['stress_15.1000mm/min'])

# расчет среднего значения нагрузки для каждой скорости
stress_mid = (stress_1_interp + stress_2_interp + stress_3_interp) / 3
stress_mid2 = (stress_4_interp + stress_5_interp + stress_6_interp) / 3
stress_mid3 = (stress_7_interp + stress_8_interp + stress_9_interp) / 3
stress_mid4 = (stress_10_interp + stress_11_interp + stress_12_interp) / 3
stress_mid5 = (stress_13_interp + stress_14_interp + stress_15_interp) / 3
# сохранение точек графика "Среднее" в файл excel
df_save = pd.DataFrame({
    'Stress_1.2mm/min': stress_mid,
    'UD_1.2mm/min': ud_linspace,
    'Stress_10mm/min': stress_mid2,
    'UD_10mm/min': ud_linspace,
    'Stress_50mm/min': stress_mid3,
    'UD_50mm/min': ud_linspace,
    'Stress_650mm/min': stress_mid4,
    'UD_650mm/min': ud_linspace,
    'Stress_1000mm/min': stress_mid5,
    'UD_1000mm/min': ud_linspace,
})

# сохранение данных в файл excel
writer = pd.ExcelWriter('average_all.xlsx', engine='xlsxwriter')
df_save.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()

r=3.5e-3#Радиус цилиндрической части образца
rh= 3.1e-3 #Радиус шейки
Lobr= 58.48# Длина рабочей части образца
nolx=0# начальная точка х для постоения графика
noly=0# начальная точка у для постоения графика
V10 = 10 #Скорость нагружения мм/мин
V50 = 50 #Скорость нагружения мм/мин
V650 = 650 #Скорость нагружения мм/мин
V1000 = 1000 #Скорость нагружения мм/мин

# Считываем данные из файла Excel
df = pd.read_excel('average_all.xlsx', sheet_name='Sheet1')
# определяем индекс строки, где происходит переход от линейного участка к пластическому
"""" 
______________________________________________________________________________________________________________________
Модуль поиска опорных точек по машинной диаграмме
______________________________________________________________________________________________________________________
"""
"""
__________
rate 2мм/мин
__________
"""
#определим максимальное удлинение
Lmax=df['UD_1.2mm/min'].max()
# поиск максимального значения нагрузки
max_voltage = df['Stress_1.2mm/min'].max()
# поиск соответствующего ему значения перемещения
displacement = df.loc[df['Stress_1.2mm/min'] == max_voltage, 'UD_1.2mm/min'].values[0]

#определим деформацию соотвествующую пределу текучести
L02=Lmax*0.02
#Преобразуем значения по осям
Lgrx=df['UD_1.2mm/min']+L02
Pgry=df['UD_1.2mm/min']*21900
# Поиск точки пересечения прямой и интерполированной диаграммы
line1 = LineString(list(zip(ud_linspace, stress_mid)))
line2 = LineString(list(zip(Lgrx[Pgry<max_voltage], Pgry[Pgry<max_voltage])))
intersection = line1.intersection(line2)
if intersection.geom_type == 'Point':
    x, y = intersection.xy
else:
    print("Графики не пересекаются")
#Присвоим пределу текучести имя yield_stress(величина в Н)
yield_stress = y[0]
#Присвоим относительному удлиннению имя displacement_value(величина в мм)
displacement_value = x[0]

# Определим величину перемещения соотвествующее пределу прочности
max_displacement = df['UD_1.2mm/min'].iloc[-1]
# поиск соответствующего ему значению нагрузки
voltag = df.loc[df['UD_1.2mm/min'] == max_displacement, 'Stress_1.2mm/min'].values[0]
"""
__________
rate 10мм/мин
__________
"""
#определим максимальное удлинение
Lmax10=df['UD_10mm/min'].max()
# поиск максимального значения нагрузки
max_voltage10 = df['Stress_10mm/min'].max()
# поиск соответствующего ему значения перемещения
displacement10 = df.loc[df['Stress_10mm/min'] == max_voltage10, 'UD_10mm/min'].values[0]

#определим деформацию соотвествующую пределу текучести
L0210=Lmax10*0.02
#Преобразуем значения по осям
Lgrx10=df['UD_10mm/min']+L0210
Pgry10=df['UD_10mm/min']*21900
# Поиск точки пересечения прямой и интерполированной диаграммы
line110 = LineString(list(zip(ud_linspace, stress_mid2)))
line210 = LineString(list(zip(Lgrx[Pgry10<max_voltage10], Pgry10[Pgry10<max_voltage10])))
intersection_point10 = line110.intersection(line210)
x10 = intersection_point10.x
y10 = intersection_point10.y
#Присвоим пределу текучести имя yield_stress(величина в Н)
yield_stress10 = y10
#Присвоим относительному удлиннению имя displacement_value(величина в мм)
displacement_value10 = x10

# Определим величину перемещения соотвествующее пределу прочности
max_displacement10 = df['UD_10mm/min'].iloc[-90]
# поиск соответствующего ему значению нагрузки
voltag10 = df.loc[df['UD_10mm/min'] == max_displacement10, 'Stress_10mm/min'].values[0]
"""
__________
rate 50мм/мин
__________
"""
#определим максимальное удлинение
Lmax50=df['UD_50mm/min'].max()
# поиск максимального значения нагрузки
max_voltage50 = df['Stress_50mm/min'].max()
# поиск соответствующего ему значения перемещения
displacement50 = df.loc[df['Stress_50mm/min'] == max_voltage50, 'UD_50mm/min'].values[0]

#определим деформацию соотвествующую пределу текучести
L0250=Lmax50*0.02
#Преобразуем значения по осям
Lgrx50=df['UD_50mm/min']+L0250
Pgry50=df['UD_50mm/min']*22000
# Поиск точки пересечения прямой и интерполированной диаграммы
line150 = LineString(list(zip(ud_linspace, stress_mid3)))
line250 = LineString(list(zip(Lgrx[Pgry50<max_voltage50], Pgry50[Pgry50<max_voltage50])))
intersection_point50 = line150.intersection(line250)
x50 = intersection_point50.x
y50 = intersection_point50.y
#Присвоим пределу текучести имя yield_stress(величина в Н)
yield_stress50 = y50
#Присвоим относительному удлиннению имя displacement_value(величина в мм)
displacement_value50 = x50

# Определим величину перемещения соотвествующее пределу прочности
max_displacement50 = df['UD_50mm/min'].iloc[-137]
# поиск соответствующего ему значению нагрузки
voltag50 = df.loc[df['UD_50mm/min'] == max_displacement50, 'Stress_50mm/min'].values[0]
"""
__________
rate 650мм/мин
__________
"""
#определим максимальное удлинение
Lmax650=df['UD_650mm/min'].max()
# поиск максимального значения нагрузки
max_voltage650 = df['Stress_650mm/min'].max()
# поиск соответствующего ему значения перемещения
displacement650 = df.loc[df['Stress_650mm/min'] == max_voltage650, 'UD_650mm/min'].values[0]

#определим деформацию соотвествующую пределу текучести
L02650=Lmax650*0.02
#Преобразуем значения по осям
Lgrx650=df['UD_650mm/min']+L02650
Pgry650=df['UD_650mm/min']*21900
# Поиск точки пересечения прямой и интерполированной диаграммы
line1650 = LineString(list(zip(ud_linspace, stress_mid4)))
line2650 = LineString(list(zip(Lgrx[Pgry650<max_voltage650], Pgry650[Pgry650<max_voltage650])))
intersection_point650 = line1650.intersection(line2650)
x650 = intersection_point650.x
y650 = intersection_point650.y
#Присвоим пределу текучести имя yield_stress(величина в Н)
yield_stress650 = y650
#Присвоим относительному удлиннению имя displacement_value(величина в мм)
displacement_value650 = x650

# Определим величину перемещения соотвествующее пределу прочности
max_displacement650 = df['UD_650mm/min'].iloc[-176]
# поиск соответствующего ему значению нагрузки
voltag650 = df.loc[df['UD_650mm/min'] == max_displacement650, 'Stress_650mm/min'].values[0]
"""
__________
rate 1000мм/мин
__________
"""
#определим максимальное удлинение
Lmax1000=df['UD_1000mm/min'].max()
# поиск максимального значения нагрузки
max_voltage1000 = df['Stress_1000mm/min'].max()
# поиск соответствующего ему значения перемещения
displacement1000 = df.loc[df['Stress_1000mm/min'] == max_voltage1000, 'UD_1000mm/min'].values[0]

#определим деформацию соотвествующую пределу текучести
L021000=Lmax1000*0.02
#Преобразуем значения по осям
Lgrx1000=df['UD_1000mm/min']+L021000
Pgry1000=df['UD_1000mm/min']*19500
# Поиск точки пересечения прямой и интерполированной диаграммы
line11000 = LineString(list(zip(ud_linspace, stress_mid5)))
line21000 = LineString(list(zip(Lgrx[Pgry1000<max_voltage1000], Pgry1000[Pgry1000<max_voltage1000])))
intersection_point1000 = line11000.intersection(line21000)
x1000 = intersection_point1000.x
y1000 = intersection_point1000.y
#Присвоим пределу текучести имя yield_stress(величина в Н)
yield_stress1000 = y1000
#Присвоим относительному удлиннению имя displacement_value(величина в мм)
displacement_value1000 = x1000

# Определим величину перемещения соотвествующее пределу прочности
max_displacement1000 = df['UD_1000mm/min'].iloc[-235]
# поиск соответствующего ему значению нагрузки
voltag1000 = df.loc[df['UD_1000mm/min'] == max_displacement1000, 'Stress_1000mm/min'].values[0]
"""
_________________________________________________________________________________________________________________
В  модуле производится перевод машинной диаграммы зависимости нагрузки от перемещения к истинной напряжения 
от деформации и построением графика .
_________________________________________________________________________________________________________________
"""
"""
__________
rate 2мм/мин
__________
"""
#Определение истинного значения деформации и напряжения для предела текучести.
displacement1 = math.log((Lobr+displacement_value)/Lobr)
yield_stress1 = yield_stress/((3.14*r**2)*10e5)

# выделение точек лежащих в заданном промежутке
selected_points = df[(df['Stress_1.2mm/min'] > yield_stress) & (df['Stress_1.2mm/min'] < max_voltage)]

# выделение точек лежащих в заданном промежутке
selected_points = df[(df['UD_1.2mm/min'] > displacement_value) & (df['UD_1.2mm/min'] < displacement)]

# вычисление деформации для каждой точки в списке selected_points
displacement_list = [(math.log((Lobr+displacement_all)/Lobr)) for displacement_all in selected_points['UD_1.2mm/min']]
# вычисление деформации для каждой точки в списке selected_points
pressure_array = np.array([voltage / (((1-(0.3*disp-0.5*displacement1))**2)*((3.14*r**2)*10e5)) for voltage, disp in zip_longest(selected_points['Stress_1.2mm/min'], displacement_list)])

# Определение истинных напряжений и деформации для временного сопротивления
displacement2 = math.log((Lobr+displacement)/Lobr)
max_voltage1 = max_voltage/(((1-(0.3*displacement2-0.5*displacement1))**2)*((3.14*r**2)*10e5))

# Определение истинных напряжений и деформации для точки разрушения
displacement3 = math.log((Lobr+max_displacement)/Lobr)
voltage3 = voltag/(((1-(0.4*displacement3-0.3*displacement1))**2)*((3.14*r**2)*10e5))

# Объединение обработанных точек в единый список
istinnie_deformacii = []
istinnie_deformacii.append(round(nolx,2))
istinnie_deformacii.append(round(displacement1,2))
istinnie_deformacii.extend(np.round(displacement_list, 2))
istinnie_deformacii.append(round(displacement2,2))
istinnie_deformacii.append(round(displacement3,2))

istinnie_napryzhenia = []
istinnie_napryzhenia.append(round(noly,2))
istinnie_napryzhenia.append(round(yield_stress1,0))
istinnie_napryzhenia.extend(np.round(pressure_array, 1))
istinnie_napryzhenia.append(round(max_voltage1,1))
istinnie_napryzhenia.append(round(voltage3,1))

istinnie_deformacii = np.asarray(istinnie_deformacii)
istinnie_napryzhenia = np.asarray(istinnie_napryzhenia)
stress_poly = Polynomial.fit(istinnie_deformacii, istinnie_napryzhenia, 8) # Создание полинома восьмой стерени
istinnie_napryzhenia = stress_poly(istinnie_deformacii) # Вычисления истинных напряжений из полинома

#Прологорифмируем списки displacement_list и pressure_array
displacemenp_approx=displacement_list
pressure_approx = pressure_array
Lg_displacement_list = list(map(math.log, displacemenp_approx[-10:]))
Lg_pressure_array = list(map(math.log, pressure_approx[-10:]-yield_stress1))

if len(Lg_displacement_list) > len(Lg_pressure_array):
    Lg_displacement_list = Lg_displacement_list[:len(Lg_pressure_array)]
else:
    Lg_pressure_array = Lg_pressure_array[:len(Lg_displacement_list)]

z = np.polyfit(Lg_displacement_list, Lg_pressure_array, 1)
# Аппроксимация данных полиномом первой степени
z = np.polyfit(Lg_displacement_list, Lg_pressure_array, 1)
p = np.poly1d(z)
# Аппроксимация данных прямой линией методом наименьших квадратов
coefficients = np.polyfit(Lg_displacement_list, Lg_pressure_array, 1)
# Определение тангенса угла наклона прямой линии
slope = coefficients[0]
slope1 = coefficients[1]
"""
__________
rate 10мм/мин
__________
"""
#Определение истинного значения деформации и напряжения для предела текучести.
displacement110 = math.log((Lobr+displacement_value10)/Lobr)
yield_stress110 = yield_stress10/((3.14*r**2)*10e5)

# выделение точек лежащих в заданном промежутке
selected_points10 = df[(df['Stress_10mm/min'] > yield_stress10) & (df['Stress_10mm/min'] < max_voltage10)]

# выделение точек лежащих в заданном промежутке
selected_points10 = df[(df['UD_10mm/min'] > displacement_value10) & (df['UD_10mm/min'] < displacement10)]

# вычисление деформации для каждой точки в списке selected_points
displacement_list10 = [(math.log((Lobr+displacement_all10)/Lobr)) for displacement_all10 in selected_points10['UD_10mm/min']]
# вычисление деформации для каждой точки в списке selected_points
pressure_array10 = np.array([voltage10 / (((1-(disp10-displacement110))**2)*((3.14*r**2)*10e5)) for voltage10, disp10 in zip_longest(selected_points10['Stress_10mm/min'], displacement_list10)])

# Определение истинных напряжений и деформации для временного сопротивления
displacement210 = math.log((Lobr+displacement10)/Lobr)
max_voltage110 = max_voltage10/(((1-(displacement210-displacement110))**2)*((3.14*r**2)*10e5))

# Определение истинных напряжений и деформации для точки разрушения
displacement310 = math.log((Lobr+max_displacement10)/Lobr)
voltage310 = voltag10/(((1-(displacement310-displacement110))**2)*((3.14*r**2)*10e5))

# Объединение обработанных точек в единый список
istinnie_deformacii10 = []
istinnie_deformacii10.append(round(nolx,2))
istinnie_deformacii10.append(round(displacement110,2))
istinnie_deformacii10.extend(np.round(displacement_list10, 2))
istinnie_deformacii10.append(round(displacement210,2))
istinnie_deformacii10.append(round(displacement310,2))

istinnie_napryzhenia10 = []
istinnie_napryzhenia10.append(round(noly,2))
istinnie_napryzhenia10.append(round(yield_stress110,0))
istinnie_napryzhenia10.extend(np.round(pressure_array10, 1))
istinnie_napryzhenia10.append(round(max_voltage110,1))
istinnie_napryzhenia10.append(round(voltage310,1))

istinnie_deformacii10 = np.asarray(istinnie_deformacii10)
istinnie_napryzhenia10 = np.asarray(istinnie_napryzhenia10)
stress_poly = Polynomial.fit(istinnie_deformacii10, istinnie_napryzhenia10, 8) # Создание полинома восьмой стерени
istinnie_napryzhenia10 = stress_poly(istinnie_deformacii10) # Вычисления истинных напряжений из полинома

#Расчет параметра С
#Перевод  скорости нагружения к скорости деформации
Strain_rate10 = (V10/60)/Lobr
dis10 = (istinnie_napryzhenia10/(yield_stress110+((np.exp(slope1))*istinnie_napryzhenia10**Strain_rate10)))
lndisp10 = [math.log(Strain_rate10) for i in range(len(dis10))]
print(V10)
print(Strain_rate10)
print(lndisp10)

"""
__________
rate 50мм/мин
__________
"""
#Определение истинного значения деформации и напряжения для предела текучести.
displacement150 = math.log((Lobr+displacement_value50)/Lobr)
yield_stress150 = yield_stress50/((3.14*r**2)*10e5)

# выделение точек лежащих в заданном промежутке
selected_points50 = df[(df['Stress_50mm/min'] > yield_stress50) & (df['Stress_50mm/min'] < max_voltage50)]

# выделение точек лежащих в заданном промежутке
selected_points50 = df[(df['UD_50mm/min'] > displacement_value50) & (df['UD_50mm/min'] < displacement50)]

# вычисление деформации для каждой точки в списке selected_points
displacement_list50 = [(math.log((Lobr+displacement_all50)/Lobr)) for displacement_all50 in selected_points50['UD_50mm/min']]
# вычисление деформации для каждой точки в списке selected_points
pressure_array50 = np.array([voltage50 / (((1-(0.3*disp-0.5*displacement150))**2)*((3.14*r**2)*10e5)) for voltage50, disp in zip_longest(selected_points50['Stress_50mm/min'], displacement_list50)])

# Определение истинных напряжений и деформации для временного сопротивления
displacement250 = math.log((Lobr+displacement50)/Lobr)
max_voltage150 = max_voltage50/(((1-(0.3*displacement250-0.5*displacement150))**2)*((3.14*r**2)*10e5))

# Определение истинных напряжений и деформации для точки разрушения
displacement350 = math.log((Lobr+max_displacement50)/Lobr)
voltage350 = voltag50/(((1-(displacement350-displacement150))**2)*((3.14*r**2)*10e5))

# Объединение обработанных точек в единый список
istinnie_deformacii50 = []
istinnie_deformacii50.append(round(nolx,2))
istinnie_deformacii50.append(round(displacement150,2))
istinnie_deformacii50.extend(np.round(displacement_list50, 2))
istinnie_deformacii50.append(round(displacement250,2))
istinnie_deformacii50.append(round(displacement350,2))

istinnie_napryzhenia50 = []
istinnie_napryzhenia50.append(round(noly,2))
istinnie_napryzhenia50.append(round(yield_stress150,0))
istinnie_napryzhenia50.extend(np.round(pressure_array50, 1))
istinnie_napryzhenia50.append(round(max_voltage150,1))
istinnie_napryzhenia50.append(round(voltage350,1))

istinnie_deformacii50 = np.asarray(istinnie_deformacii50)
istinnie_napryzhenia50 = np.asarray(istinnie_napryzhenia50)
stress_poly = Polynomial.fit(istinnie_deformacii50, istinnie_napryzhenia50, 8) # Создание полинома восьмой стерени
istinnie_napryzhenia50 = stress_poly(istinnie_deformacii50) # Вычисления истинных напряжений из полинома

Strain_rate50 = (V50/60)/Lobr
dis50 = (istinnie_napryzhenia50/(yield_stress150+((np.exp(slope1))*istinnie_napryzhenia50**Strain_rate50)))
lndisp50 = [math.log(Strain_rate50) for i in range(len(dis50))]
print(V50)
print(Strain_rate50)
print(lndisp50)
"""
__________
rate 650мм/мин
__________
"""
#Определение истинного значения деформации и напряжения для предела текучести.
displacement1650 = math.log((Lobr+displacement_value650)/Lobr)
yield_stress1650 = yield_stress650/((3.14*r**2)*10e5)

# выделение точек лежащих в заданном промежутке
selected_points650 = df[(df['Stress_650mm/min'] > yield_stress650) & (df['Stress_650mm/min'] < max_voltage650)]

# выделение точек лежащих в заданном промежутке
selected_points650 = df[(df['UD_650mm/min'] > displacement_value650) & (df['UD_650mm/min'] < displacement650)]

# вычисление деформации для каждой точки в списке selected_points
displacement_list650 = [(math.log((Lobr+displacement_all650)/Lobr)) for displacement_all650 in selected_points650['UD_650mm/min']]
# вычисление деформации для каждой точки в списке selected_points
pressure_array650 = np.array([voltage650 / (((1-(0.3*disp650-0.5*displacement1650))**2)*((3.14*r**2)*10e5)) for voltage650, disp650 in zip_longest(selected_points650['Stress_650mm/min'], displacement_list650)])

# Определение истинных напряжений и деформации для временного сопротивления
displacement2650 = math.log((Lobr+displacement650)/Lobr)
max_voltage1650 = max_voltage650/(((1-(0.3*displacement2650-0.5*displacement1650))**2)*((3.14*r**2)*10e5))

# Определение истинных напряжений и деформации для точки разрушения
displacement3650 = math.log((Lobr+max_displacement650)/Lobr)
voltage3650 = voltag650/(((1-(displacement3650-displacement1650))**2)*((3.14*r**2)*10e5))

# Объединение обработанных точек в единый список
istinnie_deformacii650 = []
istinnie_deformacii650.append(round(nolx,2))
istinnie_deformacii650.append(round(displacement1650,2))
istinnie_deformacii650.extend(np.round(displacement_list650, 2))
istinnie_deformacii650.append(round(displacement2650,2))
istinnie_deformacii650.append(round(displacement3650,2))

istinnie_napryzhenia650 = []
istinnie_napryzhenia650.append(round(noly,2))
istinnie_napryzhenia650.append(round(yield_stress1650,0))
istinnie_napryzhenia650.extend(np.round(pressure_array650, 1))
istinnie_napryzhenia650.append(round(max_voltage1650,1))
istinnie_napryzhenia650.append(round(voltage3650,1))

istinnie_deformacii650 = np.asarray(istinnie_deformacii650)
istinnie_napryzhenia650 = np.asarray(istinnie_napryzhenia650)
stress_poly = Polynomial.fit(istinnie_deformacii650, istinnie_napryzhenia650, 8) # Создание полинома восьмой стерени
istinnie_napryzhenia650 = stress_poly(istinnie_deformacii650) # Вычисления истинных напряжений из полинома

Strain_rate650 = (V650/60)/Lobr
dis650 = (istinnie_napryzhenia650/(yield_stress1650+((np.exp(slope1))*istinnie_napryzhenia650**Strain_rate650)))
lndisp650 = [math.log(Strain_rate650) for i in range(len(dis650))]
print(V650)
print(Strain_rate650)
print(lndisp650)
print(slope1)
"""
__________
rate 1000мм/мин
__________
"""
#Определение истинного значения деформации и напряжения для предела текучести.
displacement11000 = math.log((Lobr+displacement_value1000)/Lobr)
yield_stress11000 = yield_stress1000/((3.14*r**2)*10e5)

# выделение точек лежащих в заданном промежутке
selected_points1000 = df[(df['Stress_1000mm/min'] > yield_stress1000) & (df['Stress_1000mm/min'] < max_voltage1000)]

# выделение точек лежащих в заданном промежутке
selected_points1000 = df[(df['UD_1000mm/min'] > displacement_value1000) & (df['UD_1000mm/min'] < displacement1000)]

# вычисление деформации для каждой точки в списке selected_points
displacement_list1000 = [(math.log((Lobr+displacement_all1000)/Lobr)) for displacement_all1000 in selected_points1000['UD_1000mm/min']]
# вычисление деформации для каждой точки в списке selected_points
pressure_array1000 = np.array([voltage1000 / (((1-(0.3*disp-0.5*displacement11000))**2)*((3.14*r**2)*10e5)) for voltage1000, disp in zip_longest(selected_points1000['Stress_1000mm/min'], displacement_list1000)])

# Определение истинных напряжений и деформации для временного сопротивления
displacement21000 = math.log((Lobr+displacement1000)/Lobr)
max_voltage11000 = max_voltage1000/(((1-(0.3*displacement21000-0.5*displacement11000))**2)*((3.14*r**2)*10e5))

# Определение истинных напряжений и деформации для точки разрушения
displacement31000 = math.log((Lobr+max_displacement1000)/Lobr)
voltage31000 = voltag1000/(((1-(0.5*displacement31000-0.3*displacement11000))**2)*((3.14*r**2)*10e5))

# Объединение обработанных точек в единый список
istinnie_deformacii1000 = []
istinnie_deformacii1000.append(round(nolx,2))
istinnie_deformacii1000.append(round(displacement11000,2))
istinnie_deformacii1000.extend(np.round(displacement_list1000, 2))
istinnie_deformacii1000.append(round(displacement21000,2))
istinnie_deformacii1000.append(round(displacement31000,2))

istinnie_napryzhenia1000 = []
istinnie_napryzhenia1000.append(round(noly,2))
istinnie_napryzhenia1000.append(round(yield_stress11000,0))
istinnie_napryzhenia1000.extend(np.round(pressure_array1000, 1))
istinnie_napryzhenia1000.append(round(max_voltage11000,1))
istinnie_napryzhenia1000.append(round(voltage31000,1))

istinnie_deformacii1000 = np.asarray(istinnie_deformacii1000)
istinnie_napryzhenia1000 = np.asarray(istinnie_napryzhenia1000)
stress_poly = Polynomial.fit(istinnie_deformacii1000, istinnie_napryzhenia1000, 8) # Создание полинома восьмой стерени
istinnie_napryzhenia1000 = stress_poly(istinnie_deformacii1000) # Вычисления истинных напряжений из полинома

Strain_rate1000 = (V1000/60)/Lobr
dis1000 = (istinnie_napryzhenia1000/(yield_stress11000+((np.exp(slope1))*istinnie_napryzhenia1000**Strain_rate1000)))
lndisp1000 = [math.log(Strain_rate1000) for i in range(len(dis1000))]
print(V1000)
print(dis1000)
print(lndisp1000)
print(slope1)
"""
_______________________________________________________________________________________________________________________
Модуль расчета параметров Джонсона Кука
_______________________________________________________________________________________________________________________
"""


"""
______________________________________________________________________________________________________________________
Блок вывода данных
______________________________________________________________________________________________________________________
"""
"""
__________
rate 2мм/мин
__________
"""
print("______strain rate 2 мм/мин______")
#Предел текучести
print('\u03C30.2 = ', round(yield_stress1,0),'МПа')
print('\u03B50.2 = ',round(displacement1,2))
#Временное сопротивление
print(f"\u03C3в = {round(max_voltage1,1)}",'МПа')
print(f"\u03B5в = {round(displacement2,2)}")
#точка разрыва
print('\u03C3п = ', round(voltage3,0),'МПа')
print('\u03B5п = ',round(displacement3,2))
#print('Напряжения на пластическом участке МПа:', np.round(pressure_array, 1))
#print('Деформации на пластическом участке:', np.round(displacement_list, 2))
# вывод коэффициентов
print(f"B= {math.exp(slope1)}")
print(f"n {slope}")
"""
__________
rate 10мм/мин
__________
"""
print("______strain rate 10 мм/мин______")
#Предел текучести
print('\u03C30.2 = ', round(yield_stress110,0),'МПа')
print('\u03B50.2 = ',round(displacement110,2))
#Временное сопротивление
print(f"\u03C3в = {round(max_voltage110,1)}",'МПа')
print(f"\u03B5в = {round(displacement210,2)}")
#точка разрыва
print('\u03C3п = ', round(voltage310,0),'МПа')
print('\u03B5п = ',round(displacement310,2))
"""
__________
rate 50мм/мин
__________
"""
print("______strain rate 50 мм/мин______")
#Предел текучести
print('\u03C30.2 = ', round(yield_stress150,0),'МПа')
print('\u03B50.2 = ',round(displacement150,2))
#Временное сопротивление
print(f"\u03C3в = {round(max_voltage150,1)}",'МПа')
print(f"\u03B5в = {round(displacement250,2)}")
#точка разрыва
print('\u03C3п = ', round(voltage350,0),'МПа')
print('\u03B5п = ',round(displacement350,2))
"""
__________
rate 650мм/мин
__________
"""
print("______strain rate 650 мм/мин______")
#Предел текучести
print('\u03C30.2 = ', round(yield_stress1650,0),'МПа')
print('\u03B50.2 = ',round(displacement1650,2))
#Временное сопротивление
print(f"\u03C3в = {round(max_voltage1650,1)}",'МПа')
print(f"\u03B5в = {round(displacement2650,2)}")
#точка разрыва
print('\u03C3п = ', round(voltage3650,0),'МПа')
print('\u03B5п = ',round(displacement3650,2))
"""
__________
rate 1000мм/мин
__________
"""
print("______strain rate 1000 мм/мин______")
#Предел текучести
print('\u03C30.2 = ', round(yield_stress11000,0),'МПа')
print('\u03B50.2 = ',round(displacement11000,2))
#Временное сопротивление
print(f"\u03C3в = {round(max_voltage11000,1)}",'МПа')
print(f"\u03B5в = {round(displacement21000,2)}")
#точка разрыва
print('\u03C3п = ', round(voltage31000,0),'МПа')
print('\u03B5п = ',round(displacement31000,2))
"""
_______________________________________________________________________________________________________________________
Блок построения графиков
_______________________________________________________________________________________________________________________
"""
fig, ((ax1, ax2)) = plt.subplots(1, 2,figsize = (15,5),sharex=True)
fig, (ax4) = plt.subplots(1, 1,figsize = (7,5),sharex=True)
fig, ((ax5, ax6)) = plt.subplots(1,2,figsize = (15,5),sharex=True)
fig, ((ax8, ax9)) = plt.subplots(1,2,figsize = (15,5),sharex=True)
fig, ((ax11, ax12)) = plt.subplots(1,2,figsize = (15,5),sharex=True)
fig, ((ax14, ax15)) = plt.subplots(1,2,figsize = (15,5),sharex=True)
fig, ((ax3, ax7, ax10, ax13, ax16)) = plt.subplots(1, 5,figsize = (80,5),sharex=True)
"""
__________
rate 2 мм/мин
__________
"""
ax1.plot(ud_linspace, stress_1_interp, label='Образец 1')
ax1.plot(ud_linspace, stress_2_interp, label='Образец 2')
ax1.plot(ud_linspace, stress_3_interp, label='Образец 3')
ax1.plot(ud_linspace, stress_mid, label='Среднее',linestyle='--')
ax1.legend()
ax1.set_xlabel('\u0394l,мм')
ax1.set_ylabel('Р ,Н')
ax1.set_title('Результаты эксперимента.Strain rate= 2мм/мин')

ax2.plot(ud_linspace, stress_mid, label='Среднее')
ax2.plot(Lgrx[Pgry<max_voltage],Pgry[Pgry<max_voltage], label='0.2%')
if intersection.geom_type == 'Point':
    ax2.plot(x[0], y[0], 'ro', label='\u03C302')
if intersection.geom_type == 'Point':
    ax2.plot(displacement, max_voltage, 'r^', label='\u03C3в')
if intersection.geom_type == 'Point':
    ax2.plot(max_displacement, voltag, 'rD', label='\u03C3р')
ax2.legend()
ax2.set_xlabel('\u0394l,мм')
ax2.set_ylabel('Р ,Н')
ax2.set_title('Результаты поиска расчетных точек')

ax3.plot(istinnie_deformacii, istinnie_napryzhenia) # добавлена закрывающая скобка
ax3.legend()
ax3.set_xlabel('\u03B5')
ax3.set_ylabel('\u03C3,МПа')
ax3.set_title('Strain rate 2 мм/мин')

ax4.plot(Lg_displacement_list, Lg_pressure_array, label='\u03C302-\u03C3в')
ax4.plot(Lg_displacement_list, p(Lg_displacement_list), 'r-', label='Аппроксимация')
ax4.set_title('Результат аппроксимации плиномом 1-ой степени')
ax4.legend()
ax4.set_xlabel('\u03B5')
ax4.set_ylabel('\u03C3, МПа')
"""
__________
rate 10 мм/мин
__________
"""
ax5.plot(ud_linspace, stress_4_interp, label='Образец 4')
ax5.plot(ud_linspace, stress_5_interp, label='Образец 5')
ax5.plot(ud_linspace, stress_6_interp, label='Образец 6')
ax5.plot(ud_linspace, stress_mid2, label='Среднее',linestyle='--')
ax5.legend()
ax5.set_xlabel('\u0394l,мм')
ax5.set_ylabel('Р ,Н')
ax5.set_title('Результаты эксперимента.Strain rate= 10 мм/мин')

ax6.plot(ud_linspace, stress_mid2, label='Среднее')
ax6.plot(Lgrx[Pgry10<max_voltage10],Pgry[Pgry10<max_voltage10], label='0.2%')
if intersection.geom_type == 'Point':
    ax6.plot(x10, y10, 'ro', label='\u03C302')
if intersection.geom_type == 'Point':
    ax6.plot(displacement10, max_voltage10, 'r^', label='\u03C3в')
if intersection.geom_type == 'Point':
    ax6.plot(max_displacement10, voltag10, 'rD', label='\u03C3р')
ax6.legend()
ax6.set_xlabel('\u0394l,мм')
ax6.set_ylabel('Р ,Н')
ax6.set_title('Результаты поиска расчетных точек')

ax7.plot(istinnie_deformacii10, istinnie_napryzhenia10) # добавлена закрывающая скобка
ax7.legend()
ax7.set_xlabel('\u03B5')
ax7.set_ylabel('\u03C3,МПа')
ax7.set_title('Strain rate 10 мм/мин')
"""
__________
rate 50 мм/мин
__________
"""
ax8.plot(ud_linspace, stress_7_interp, label='Образец 7')
ax8.plot(ud_linspace, stress_8_interp, label='Образец 8')
ax8.plot(ud_linspace, stress_9_interp, label='Образец 9')
ax8.plot(ud_linspace, stress_mid3, label='Среднее',linestyle='--')
ax8.legend()
ax8.set_xlabel('\u0394l,мм')
ax8.set_ylabel('Р ,Н')
ax8.set_title('Результаты эксперимента.Strain rate= 50 мм/мин')

ax9.plot(ud_linspace, stress_mid3, label='Среднее')
ax9.plot(Lgrx[Pgry50<max_voltage50],Pgry[Pgry50<max_voltage50], label='0.2%')
if intersection.geom_type == 'Point':
    ax9.plot(x50, y50, 'ro', label='\u03C302')
if intersection.geom_type == 'Point':
    ax9.plot(displacement50, max_voltage50, 'r^', label='\u03C3в')
if intersection.geom_type == 'Point':
    ax9.plot(max_displacement50, voltag50, 'rD', label='\u03C3р')
ax9.legend()
ax9.set_xlabel('\u0394l,мм')
ax9.set_ylabel('Р ,Н')
ax9.set_title('Результаты поиска расчетных точек')

ax10.plot(istinnie_deformacii50, istinnie_napryzhenia50) # добавлена закрывающая скобка
ax10.legend()
ax10.set_xlabel('\u03B5')
ax10.set_ylabel('\u03C3,МПа')
ax10.set_title('Strain rate 50 мм/мин')
"""
__________
rate 650 мм/мин
__________
"""
ax11.plot(ud_linspace, stress_10_interp, label='Образец 10')
ax11.plot(ud_linspace, stress_11_interp, label='Образец 11')
ax11.plot(ud_linspace, stress_12_interp, label='Образец 12')
ax11.plot(ud_linspace, stress_mid4, label='Среднее',linestyle='--')
ax11.legend()
ax11.set_xlabel('\u0394l,мм')
ax11.set_ylabel('Р ,Н')
ax11.set_title('Результаты эксперимента.Strain rate= 650 мм/мин')

ax12.plot(ud_linspace, stress_mid4, label='Среднее')
ax12.plot(Lgrx[Pgry650<max_voltage650],Pgry[Pgry650<max_voltage650], label='0.2%')
if intersection.geom_type == 'Point':
    ax12.plot(x650, y650, 'ro', label='\u03C302')
if intersection.geom_type == 'Point':
    ax12.plot(displacement650, max_voltage650, 'r^', label='\u03C3в')
if intersection.geom_type == 'Point':
    ax12.plot(max_displacement650, voltag650, 'rD', label='\u03C3р')
ax12.legend()
ax12.set_xlabel('\u0394l,мм')
ax12.set_ylabel('Р ,Н')
ax12.set_title('Результаты поиска расчетных точек')

ax13.plot(istinnie_deformacii650, istinnie_napryzhenia650) # добавлена закрывающая скобка
ax13.legend()
ax13.set_xlabel('\u03B5')
ax13.set_ylabel('\u03C3,МПа')
ax13.set_title('Strain rate 650 мм/мин')
"""
__________
rate 1000 мм/мин
__________
"""
ax14.plot(ud_linspace, stress_13_interp, label='Образец 13')
ax14.plot(ud_linspace1, stress_14_interp, label='Образец 14')
ax14.plot(ud_linspace1, stress_15_interp, label='Образец 15')
ax14.plot(ud_linspace, stress_mid5, label='Среднее',linestyle='--')
ax14.legend()
ax14.set_xlabel('\u0394l,мм')
ax14.set_ylabel('Р ,Н')
ax14.set_title('Результаты эксперимента.Strain rate= 1000 мм/мин')

ax15.plot(ud_linspace, stress_mid5, label='Среднее')
ax15.plot(Lgrx[Pgry1000<max_voltage1000],Pgry[Pgry1000<max_voltage1000], label='0.2%')
if intersection.geom_type == 'Point':
    ax15.plot(x1000, y1000, 'ro', label='\u03C302')
if intersection.geom_type == 'Point':
    ax15.plot(displacement1000, max_voltage1000, 'r^', label='\u03C3в')
if intersection.geom_type == 'Point':
    ax15.plot(max_displacement1000, voltag1000, 'rD', label='\u03C3р')
ax15.legend()
ax15.set_xlabel('\u0394l,мм')
ax15.set_ylabel('Р ,Н')
ax15.set_title('Результаты поиска расчетных точек')

ax16.plot(istinnie_deformacii1000, istinnie_napryzhenia1000) # добавлена закрывающая скобка
ax16.legend()
ax16.set_xlabel('\u03B5')
ax16.set_ylabel('\u03C3,МПа')
ax16.set_title('Strain rate 1000 мм/мин')

plt.show()



"""
_______________________________________________________________________________________________________________________
Модуль производит сохранение осредненных точек в файл эксель
_______________________________________________________________________________________________________________________
"""
# сохранение точек графика "Среднее" в файл excel
df_save = pd.DataFrame({
    'Stress_1.2mm/min': istinnie_napryzhenia10,
    'UD_1.2mm/min': istinnie_deformacii10
})

# сохранение данных в файл excel
writer = pd.ExcelWriter('average1.xlsx', engine='xlsxwriter')
df_save.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()