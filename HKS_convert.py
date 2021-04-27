import os
import glob
from decim import decim
from coef_to_EO_convert import coef
#from numba import njit
import time 
from dir_list import get_file_list
from convert_with_A1win import convert_fl
from decim_HKS import dcm_HKS

PATH_SRC='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/SRC' #Путь к исходникам
path_to_win_A1_exe='/home/gluk/bin/PROJECTS/RAW_TILT_CONVERTER/win2asc/win2asc' #Путь к win2asc
path_to_asc='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC' #Путь к директории обработки. Здесь в процессе обработки создаются
# и удаляются файлы
path_to_100hz_asc='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/100hz'#Cюда помещаются 100hz asc. 
path_to_1min_csv='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/min'
path_to_1hour_csv='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/hour'


filelist=get_file_list(PATH_SRC) # Получаем список всех файлов в директории SRC
convert_fl(path_to_win_A1_exe, filelist, path_to_asc,path_to_100hz_asc) #Конвертируем файлы с помощью win2asc. На вход путь к win2asc, список с путями файлов
#путь к директории ASC, где происходит обработка, путь к директории ASC/100hz куда складываем данные после конвертации с помощью win2asc

dcm_HKS(path_to_100hz_asc, path_to_1min_csv) #Открываем файлы и децимируем их




