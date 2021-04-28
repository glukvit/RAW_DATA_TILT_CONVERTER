import os 
# Получение списка полныйх путей к файлам во вложенных директориях передаваемого пути
# На вход полный путь к целевой директории. На выходе список с готовыми путями.
#path ="/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/SRC" 
def get_file_list(path):

    filelist = []
    for root, dirs, files in os.walk(path): 
        for file in files: #append the file name to the list 
                filelist.append(os.path.join(root,file))
    filelist =sorted(filelist)
    return(filelist)