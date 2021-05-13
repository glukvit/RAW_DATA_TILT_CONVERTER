import os
import pandas as pd
from dir_list import get_file_list

def dcm_HKS(path_to_100hz_asc, path_to_1min_csv, path_to_1hour_csv): # Получаем список файлов в директории 100hz
    
    filelist = get_file_list(path_to_100hz_asc) #Вызываем модуль и получаем полный список всех файлов.

    for every in filelist: #Открываем каждый часовой файл 
	    if os.path.getsize(every) != 0:
                print('Децимирую: ', every)
                fin_df = pd.DataFrame() #Сюда сложим все данные
                df=pd.read_csv(every, header=None, sep = ' ')
                df['DATE'] = df[1].str.cat(df[2], sep = ' ') #Соединяем два столбца со временем чтобы получить дату в нужном формате
                cols = [0, 'DATE',3] #Выбираем нужные столбцы и расставляем их в нужном порядке
                df = df[cols] #Переопределяем датафрейм 0-номер канала, 'DATE'-дата, 3-номер столбца с отчетами
                channels = df[0].unique() # Выбираем из столбца названия каналов
                print('Названия каналов в исходном файле')
                print('По причине отличия названий каналов на разных станцияхв программе использовать эти для данной станции')
                print(channels)
                df['DATE'] = pd.to_datetime(df['DATE']) #Переводим столбец DATE в тип datetime
                df1 = df.set_index([0, 'DATE']) # Устанавливаем мульти индекс

                for item in channels: #Перебираем каналы чтобы:
                     fin_df[item] = df1.loc[item][3] # С помощью индекса по колонке 0 сделать выборку по каналам получаем датафрейм с данными по каналам в столбцах
                
                fin_df.dropna(axis = 'columns', inplace = True) #Удаляет столбцы содержащие nan
                fin_df.reset_index(inplace = True) #Чтобы столбец DATA отображался в столбцах сбрасываем индекс
                fin_df.rename(columns={ 6: 'HAE',  7: 'HAN', 8: 'HK2'}, inplace = True) #Переименовываем столбцы
                
                #Пересохранение файла 100ГЦ в csv.gz

                base=os.path.basename(every) #Выбираем из полного пути имя
                base1=os.path.splitext(base)[0] #Удаляем из имени первое расширение
                base2=os.path.splitext(base1)[0] #Удаляем из имени второе расширение
                
                name_of_100hz_file = os.path.join(path_to_100hz_asc,base2) + '.csv' #Имя 100гц файла
                fin_df.to_csv(name_of_100hz_file, index = False, compression = "gzip") #Запись
                
                fin_df= fin_df.set_index(pd.to_datetime(fin_df['DATE'])).resample('1T').mean() #Делаем минутную выборку
                fin_df.reset_index(inplace = True) #Чтобы столбец DATA отображался в столбцах сбрасываем индекс
 
                name_of_minute_file = os.path.join(path_to_1min_csv,base2) + '_1min.csv'# Имя минутного файла
                fin_df.to_csv(name_of_minute_file, index = False, compression = "gzip")

                fin_df= fin_df.set_index(pd.to_datetime(fin_df['DATE'])).resample('1H').mean() #Делаем минутную выборку
                fin_df.reset_index(inplace = True) #Чтобы столбец DATA отображался в столбцах сбрасываем индекс
  
                name_of_hour_file = os.path.join(path_to_1hour_csv,base2) + '_1hour_.csv' #Имя часового файла
                fin_df.to_csv(name_of_hour_file, index = False, compression = "gzip")

                os.remove(every)

