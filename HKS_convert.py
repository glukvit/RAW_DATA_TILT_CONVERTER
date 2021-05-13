import os
import shutil
import glob
from decim import decim
import time 
from dir_list import get_file_list #Модуль для получения списка файлов в директории
from convert_with_A1win import convert_fl #Непосредственно модуль конвертации запускает Сишный скрипт конвертации
from decim_HKS import dcm_HKS #Модуль децимации файлов созданных win2asc создает три вида файлов 100гц, 1мин и часовой дискретизацией
from coef_to_HKS import coeff #Модуль добавления аппаратурных коэффициентов к данным. Обрабатывает все три вида файлов
###СКРИПТ КОНВЕРТИРУЕТ ДАННЫЕ ИЗ win ФОРМАТА В csv. Применяется для наклономеров с регистраторами HKS
###!!!!! КОЭФФИЦИЕНТЫ СТАНЦИЙ ПРОПИСЫВАЮТСЯ В МОДУЛЕ coef_to_HKS  !!!!!###

PATH_SRC = '/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/SRC' #Путь к исходникам
path_to_win_A1_exe ='/home/gluk/bin/PROJECTS/RAW_TILT_CONVERTER/win2asc/win2asc' #Путь к win2asc
path_to_asc ='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC' #Путь к директории обработки. Здесь в процессе обработки создаются
# и удаляются файлы
path_to_100hz_asc = path_to_asc + '/100hz'#Cюда помещаются 100hz csv.gz. 
path_to_1min_csv = path_to_asc + '/min' #Cюда перемещаются 1min csv
path_to_1hour_csv = path_to_asc + '/hour' #Cюда перемещаются 1hour csv

# Создаем структуру директорий:

if not os.path.exists(PATH_SRC): #Проверяем наличие директории /SRC
    print('Нет директории с исходными данными')
    os._exit #Выходим из программы

if not os.path.exists(path_to_win_A1_exe): #Проверяем наличие модуля с win2asc
    print('Нет директории c пакетом win2asc')
    os._exit #Выходим из программы

if  os.path.exists(path_to_asc): #Если есть директория то:
        shutil.rmtree(path_to_asc) # Сначала удаляем ее вместе со всем содержимым
        os.mkdir(path_to_asc) #И заново ее создаем
        os.mkdir(path_to_100hz_asc) #Создаем поддерикторию /ASC/100hz
        os.mkdir(path_to_1min_csv) #Создаем поддерикторию /ASC/min
        os.mkdir(path_to_1hour_csv) #Создаем поддерикторию /ASC/hour
else: #Если директории нет то:
        os.mkdir(path_to_asc) #просто ее создаем
        os.mkdir(path_to_100hz_asc) #Создаем поддерикторию /ASC/100hz
        os.mkdir(path_to_1min_csv) #Создаем поддерикторию /ASC/min 
        os.mkdir(path_to_1hour_csv) #Создаем поддерикторию /ASC/hour

filelist=get_file_list(PATH_SRC) # Получаем список всех файлов в директории SRC
convert_fl(path_to_win_A1_exe, filelist, path_to_asc,path_to_100hz_asc) #Конвертируем файлы с помощью win2asc. На вход путь к win2asc, список с путями файлов
#путь к директории ASC, где происходит обработка, путь к директории ASC/100hz куда складываем данные после конвертации с помощью win2asc
dcm_HKS(path_to_100hz_asc, path_to_1min_csv,path_to_1hour_csv) #Открываем файлы и децимируем их
coeff(path_to_100hz_asc, path_to_1min_csv,path_to_1hour_csv) #Прикручиваем аппаратурные коэффициенты

