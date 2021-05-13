import pandas as pd
from dir_list import get_file_list
coef = (0.0034981, 0.003649, 0.00009532) # APHT коэффициенты

def coeff(*args): # На вход пути к трем поддиректориям /ASC/100hz, /ASC/min, /ASC/hour
    for every in args: #Последовательно перебираем каждую поддиректорию 
        filelist = get_file_list(every) #Получаем список файлов обрабатываемой поддиректории
  #      print(filelist)
        for item in filelist: #Перебираем список файлов в обрабатываемой поддиректории
            print('Добавляю аппаратурные коэффициенты к ', item)
            df=pd.read_csv(item, compression='gzip') #Читаем каждый файл
 
            df['HAE_raw'] = df['HAE']
            df['HAN_raw'] = df['HAN']
            df['HK2_raw'] = df['HK2']   
            
            df['HAE'] = df['HAE'] * coef[0]
            df['HAN'] = df['HAN'] * coef[1]
            df['HK2'] = df['HK2'] * coef[2]

            df['HAE'] = df['HAE'].round(3)
            df['HAN'] = df['HAN'].round(3)
            df['HK2'] = df['HK2'].round(3)

            df.to_csv(item, index = False, compression = "gzip")  
