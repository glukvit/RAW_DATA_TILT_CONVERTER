import os
import glob
from decim import decim
from coef_to_EO_convert import coef
#from numba import njit
import time 

#@njit

#start_time = time.time()

#PATH_SRC='/home/gluk/EO_CONVERT/SRC' #Здесь лежат исходники в формате /директория_суток(пример:130401)/директория_часовых_файлов(пр:13040100 и т.д)/минутные_файлы(пр:13040100.00 и т.д.)
PATH_SRC='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/SRC'
#path_to_win_A1_exe='/home/gluk/win2asc/win2asc' #Путь к win2asc
path_to_win_A1_exe='/home/gluk/bin/PROJECTS/RAW_TILT_CONVERTER/win2asc'
#path_to_asc='/home/gluk/EO_CONVERT/ASC' #Сюда запишем минутники после конвертации win2asc
path_to_asc='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC'
#path_to_asc_1min_day='/home/gluk/EO_CONVERT/ASC/1min' #Сюда запишем окончательные суточные файлы с дискретизацией 1 минута.
path_to_asc_1min_day='/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/1min'
path_to_tmpfs='/mnt/tmpfs' #Директория в оперативной памяти. Настраивается отдельно. Сюда складываем файлы после процедуры decim. Их будем записывать в окончательные файлы. Просто так удобней, не нужно заморачиваться с переменными.
#koeff=(0.0012324169, 0.001267882, 0.00032246) #Коэффициенты регистратора DATAMARK LS-7000 и наклономера AP-702 для станции KLYT
koeff=(0.34981, 0.3649, 0.09532) #Коэффиценты для HKS станции APHT 

def write_fl(df_for_user, path_to_asc_1min_day,name_fl):
#	print(df_for_user)
#	print(path_to_asc_1min_day)
	name_fl=name_fl.replace('-','')+'.txt'
	print(name_fl)
	if not os.path.exists(path_to_asc_1min_day): #Если директории нет то создаем ее
			os.mkdir(path_to_asc_1min_day)
	pull_path_for_write=path_to_asc_1min_day+'/'+name_fl
	#Так если нужно записать каждый файл отдельно.
	df_for_user.to_csv(pull_path_for_write, index=False)
	
	return()
	

def convert_fl(list_fl,level_up): #Конвертация файлов в asc. Получаем список файлов и название суточной директории.

		desteny_dir=path_to_asc+'/'+level_up #Создаем путь к директории для текущих суток куда будем складывать asc

		if not os.path.exists(desteny_dir): #Если директории нет то создаем ее
			os.mkdir(desteny_dir)

		curph=os.getcwd() #Текущая директория часовая директория что-то вроде моего/home/gluk/EO_CONVERT/SRC/130402/13040223

		for every in list_fl: #Конвертация сейсмического win-формата в asc
						
			full_parh_to_every_file = os.path.abspath(every) #полный путь к обрабатываемому файлу
			cd(desteny_dir) #Переходим в директорию куда складывем файлы
			command_for_link='ln -sf '+full_parh_to_every_file #Создаем линк на файл в конечную директорию файла который будем обрабатывать

			os.system(command_for_link) #Создаем линк. В директории типа моей /home/gluk/EO_CONVERT/ASC/директория_суток/ появятся линки на соответствующие файлы из SRC
			command_to_convert=path_to_win_A1_exe+' '+desteny_dir+'/'+every #Команда конвертации win2asc с путем к линку

			os.system(command_to_convert) #Конвертируем в asc
			rm_link='rm '+ every #Удаляем линк файла который только, что обработался
			os.system(rm_link) #Удаляем
			cd(curph) #Возрващаемся в директорию /home/gluk/EO_CONVERT/SRC/дир_сут/дир_час
		return(desteny_dir) #Возращаем путь к текущим asc
			
def cd(cur_path):
	os.chdir(cur_path)
	return()
	
def read_files(list_in_dir, level_up): #Процедура получения списка файлов. На вход список директорий и откуда взяты директории
	for every in list_in_dir: #Для каждой директории
		cd(every) #Переходим в текущую директорию списка
		list_fl=os.listdir() #Получаем список файлов
		list_fl.sort()
		dest_dir=convert_fl(list_fl,level_up) #Запускаем конвертацию в asc. Передаем список файлов и название суточной директории
		cd('..') #Перейти на уровень выше
	return(dest_dir)

cd(PATH_SRC)
lstdirs=os.listdir() #Список директорий в SRC
lstdirs=list(lstdirs) #Список в list
lstdirs.sort() #Сортируем
for every in lstdirs: #Переходим в каждую директорию по списку и получаем список вложенных директорий
	cd(every)
	list_in_dir=os.listdir() #Список вложенных директорий
	list_in_dir.sort() # Сортировка
	dest_dir=read_files(list_in_dir, every) #Процедура получения файлов во вложенных директориях, передаем список директорий и директорию откуда список.
	name_fl_in_tmpfs,name_fl=decim(dest_dir,path_to_tmpfs) #На вход путь к директории для текущих суток тут теперь лежат asc, путь в директорию в ОЗУ где будут лежать файлы после децимации.
	df_for_user=coef(name_fl_in_tmpfs, koeff)
	write_fl(df_for_user, path_to_asc_1min_day,name_fl)
#	print(df_for_user)
	cd('..')

#print("--- %s seconds ---" % (time.time() - start_time))
