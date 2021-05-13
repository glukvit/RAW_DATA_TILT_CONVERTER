import os
import shutil
import glob
import gzip
# Модуль конвертирует файлы win формата с регистратора с помощью пакета win2asc и сохраняет их в path_to_100hz_asc.
# Вызывается модуль из скрипта HKS_convert.py
#Директория path_to_asc рабочая, в нее создается линк обрабатываемого win-файла , затем win2asc сохраняет в нее обработанных asc-файл, который архивируется и потом перемещается в path_to_100hz_asc
#path_to_win_A1_exe путь где лежит пакет win2asc, используемый для конвертации
# filelist список всех полных путей к обрабатываемым файлам во всех директориях расположенных в SRC (исходные файлы). filelist создается с помощью модуля dir_list.py
def convert_fl(path_to_win_A1_exe, filelist, path_to_asc, path_to_100hz_asc): #Конвертация файлов в asc. Получаем список файлов и название суточной директории.
    curph=os.getcwd() #Текущая директория
    curpath=os.chdir(path_to_asc) # Переходим в директорию куда положим готовые asc /ASC

    for every in filelist: #Из списка всех путей перебираем полные пути к файлу в директории SRC
        command_for_link='ln -sf '+every #Создаем линк на файл в конечную директорию файла который будем обрабатывать
        os.system(command_for_link) #Создаем линк. В директории типа моей /home/gluk/EO_CONVERT/ASC/директория_суток/ появятся линки на соответствующие файлы из SRC
        name=os.path.basename(every) #Извлекаем из полного пути имя обрабатываемого файла, которая находится как ссылка в директории ASC
        command_to_convert=path_to_win_A1_exe+' '+ name #
        print('Конвертирую ', name)
        os.system(command_to_convert)
        os.remove(every) #Удаляем линк
        file_to_gzip=''.join(glob.glob ('*.asc')) #Ищем файл с расширением asc, он должен быть один 
        with open(file_to_gzip, 'rb') as f_in:
            file_to_move=file_to_gzip + '.gz'
            with gzip.open(file_to_move, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file_to_gzip)
        shutil.move(file_to_move, path_to_100hz_asc) #Перемещаем файл asc в директорию 100Hz
      #  break # Можно включить для проверки программа будет работать только с одним файлом из исходников
    os.chdir(curph) #По окончании обработки возвращаемся в текущую директорию 


