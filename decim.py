import pandas as pd
import os
from numba import njit

#@njit

def write_to_tmps(path_to_tmpfs,fin_df,date_fl):
	curph=os.getcwd()
	os.chdir(path_to_tmpfs)
	name_of_file=path_to_tmpfs+'/'+date_fl[0:10]+'.csv'
	short_name=date_fl[0:10]
	fin_df.to_csv(name_of_file, index=False)
	os.chdir(curph)
	return(name_of_file,short_name)



def decim(desteny_dir,path_to_tmpfs):
	curph=os.getcwd() 
	os.chdir(desteny_dir) #Переходим в суточную директорию с asc файлами
	list_fl=os.listdir(desteny_dir) #Получаем список файлов из суточной директории с asc
	list_fl.sort() #Сортируем
	list_of_paths=[] #Список для полных путей к часовым файлам

	for every in list_fl: #Получаем список полных путей к часовым файлам
		ph=os.path.abspath(every) 
		list_of_paths.append(ph)

#	fin_df=pd.DataFrame(columns=['DATE',0,1,2,3])#Объявили пустой датафрейм куда запишем окончательные данные. КОЛИЧЕСТВО СТОЛБЦОВ ЗАВИСИТ ОТ КОЛИЧЕСТВА КАНАЛОВ СТАНЦИИ!!!
	fin_df=pd.DataFrame(columns=['DATE',0,1,2])# КОГДА НЕТ ТРЕТЬЕГО КАНАЛА С МИКРОФОНОМ. Объявили пустой датафрейм куда запишем окончательные данные. КОЛИЧЕСТВО СТОЛБЦОВ ЗАВИСИТ ОТ КОЛИЧЕСТВА КАНАЛОВ СТАНЦИИ!!
	for every in list_of_paths: #Открываем каждый часовой файл в текущей суточной директории
		print(every)
		if os.path.getsize(every) != 0:
			df=pd.read_csv(every, header=None, sep=' ') 
			df['DATE']=df[1].str.cat(df[2], sep=' ') #Соединяем два столбца со временем чтобы получить дату в нужном формате
			cols = [0, 'DATE',3] #Выбираем нужные столбцы и расставляем их в нужном порядке
			df = df[cols] #Переопределяем датафрейм 0-номер канала, 'DATE'-дата, 3-номер столбца с отчетами
			date_fl=df.loc[0,'DATE'] # Дата начала отсчета в файле. Будет использоваться как время в строке децимированного файла
			df1=df.groupby(df[0])[cols].mean()#.reset_index() # Осредняем данные со 100Гц до одной минуты. Файл минутный.
			temp_df=df1.T	#Временный датафрейм приводим к удобному виду. Транспонируем, теперь номера каналов это столбцы, значения в строках
			temp_df=temp_df.drop(index=[0]).reset_index() #Удаляем первую строчку с мусором и сбрасываем индекс
			temp_df.loc[0,'DATE']=date_fl # Подставляем дату в столбец временного датафрейм

			cols_for_temp_df=['DATE',0,1,2,3] #Определяем порядок столбцов 
#			cols_for_temp_df=['DATE',0,1,2] #КОГДА НЕТ ТРЕТЬЕГО КАНАЛА С МИКРОФОНОМ

			temp_df=temp_df[cols_for_temp_df] #Переставляем столбцы местами

			fin_df=fin_df.append(temp_df[['DATE',0,1,2,3]])
#			fin_df=fin_df.append(temp_df[['DATE',0,1,2]]) #	КОГДА НЕТ ТРЕТЬЕГО КАНАЛА С МИКРОФОНОМ
	
	name_fl_in_tmpfs,name_of_file=write_to_tmps(path_to_tmpfs,fin_df,date_fl)#Пишем датафрей в файл в директорию ОЗУ. На вход путь_до_директории, датафрейм, дата_для_файла.
		
#	print(fin_df)
	
	os.chdir(curph)
	return(name_fl_in_tmpfs,name_of_file)		
