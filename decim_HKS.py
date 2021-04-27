import os
import pandas as pd
import shutil

def dcm_HKS(path_to_100hz_asc, path_to_1min_csv): # Получаем список файлов в директории 100hz
    filelist = [] #Сюда поместим список файлов
    for root, dirs, files in os.walk(path_to_100hz_asc): #Перебираем директорию 
        for file in files: #append the file name to the list 
                filelist.append(os.path.join(root,file)) #Создаем список с полными путями ко все файлам
    filelist =sorted(filelist) #Сортируем лист
 
    fin_df = pd.DataFrame(columns=['0'])
    for every in filelist: #Открываем каждый часовой файл в текущей суточной директории
#	    print(every)
	    if os.path.getsize(every) != 0:
                df=pd.read_csv(every, header=None, sep=' ')
                df['DATE']=df[1].str.cat(df[2], sep=' ') #Соединяем два столбца со временем чтобы получить дату в нужном формате
                cols = [0, 'DATE',3] #Выбираем нужные столбцы и расставляем их в нужном порядке
                df = df[cols] #Переопределяем датафрейм 0-номер канала, 'DATE'-дата, 3-номер столбца с отчетами
                channels=df[0].unique() # Выбираем из столбца названия каналов
                df['DATE'] = pd.to_datetime(df['DATE']) #Переводим столбец DATE в тип datetime
                df1 = df.set_index([0, 'DATE']) # Устанавливаем мульти индекс

                for item in channels: #Перебираем каналы чтобы:
                     fin_df[item] = df1.loc[item][3] # С помощью индекса по колонке 0 сделать выборку по каналам получаем датафрейм с данными по каналам в столбцах
                
                fin_df.drop('0', axis = 1, inplace = True) #Удаляем мусор
                fin_df.reset_index(inplace = True) #Чтобы столбец DATA отображался в столбцах сбрасываем индекс
                fin_df.rename(columns={ 6: 'HAE',  7: 'HAN', 8: 'HK2'}, inplace = True) #Переименовываем столбцы
                print(fin_df)
                ###!!!! Здесь сделать пересохранение файла 100ГЦ

                fin_df= fin_df.set_index(pd.to_datetime(fin_df['DATE'])).resample('1T').mean() #Делаем минутную выборку
         #       fin_df.rename(columns={ 6: 'HAE',  7: 'HAN', 8: 'HK2'}, inplace = True) #Переименовываем столбцы
                fin_df.reset_index(inplace = True) #Чтобы столбец DATA отображался в столбцах сбрасываем индекс

                #print(fin_df)
                base=os.path.basename(every) #Выбираем из полного пути имя
                base1=os.path.splitext(base)[0] #Удаляем из имени первое расширение
                base2=os.path.splitext(base1)[0] #Удаляем из имени второе расширение

                if os.path.exists(path_to_1min_csv): #Проверяем наличие директории /ASC/min
                    shutil.rmtree(path_to_1min_csv) # Если есть удаляем
                    os.mkdir(path_to_1min_csv) #И заново создаем
                else: #Если директории /ASC/min нет то:
                    os.mkdir(path_to_1min_csv) #Создаем директорию

                name_of_minute_file = os.path.join(path_to_1min_csv,base2) + '.csv'
                #print(name_of_minute_file)
                fin_df.to_csv(name_of_minute_file, index=False, compression = "gzip") #