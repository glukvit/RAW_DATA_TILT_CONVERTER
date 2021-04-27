import os
import shutil
import glob
import gzip

def convert_fl(path_to_win_A1_exe, filelist, path_to_asc, path_to_100hz_asc): #Конвертация файлов в asc. Получаем список файлов и название суточной директории.
    curph=os.getcwd() #Текущая директория
    curpath=os.chdir(path_to_asc) # Переходим в директорию куда положим готовые asc /ASC
    #sto_hz=path_to_100hz_as #Будет директория куда закинем 100Гц.
    #dir_100Hz=os.path.join(path_to_asc,path_to_100hz_as)
    
    if  os.path.exists(path_to_100hz_asc): #Если директории нет то:
        shutil.rmtree(path_to_100hz_asc) # Сначала удаляем ее вместе со всем содержимым
        os.mkdir(path_to_100hz_asc) #И заново ее создаем
    else: #Если директории нет то:
        os.mkdir(path_to_100hz_asc) #просто ее создаем 

    for every in filelist: #Из списка всех путей перебираем полные пути к файлу в директории SRC
        command_for_link='ln -sf '+every #Создаем линк на файл в конечную директорию файла который будем обрабатывать
        os.system(command_for_link) #Создаем линк. В директории типа моей /home/gluk/EO_CONVERT/ASC/директория_суток/ появятся линки на соответствующие файлы из SRC
        name=os.path.basename(every) #Извлекаем из полного пути имя обрабатываемого файла, которая находится как ссылка в директории ASC
        command_to_convert=path_to_win_A1_exe+' '+ name #
 #       print(command_to_convert)
        os.system(command_to_convert)
        os.remove(every) #Удаляем линк
        file_to_gzip=''.join(glob.glob ('*.asc')) #Ищем файл с расширением asc, он должен быть один 
        with open(file_to_gzip, 'rb') as f_in:
            file_to_move=file_to_gzip + '.gz'
            with gzip.open(file_to_move, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file_to_gzip)
        shutil.move(file_to_move, path_to_100hz_asc) #Перемещаем файл asc в директорию 100Hz
        break
    os.chdir(curph) #По окончании обработки возвращаемся в текущую директорию 


