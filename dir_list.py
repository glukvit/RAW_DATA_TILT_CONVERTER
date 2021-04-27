import os 
# Получение списка полныйх путей к файлам во вложенных директориях передаваемого пути
# На вход полный путь к целевой директории. На выходе список с готовыми путями.
#path ="/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/SRC" #we shall store all the file names in this list filelist = [] 
def get_file_list(path):

    filelist = []
    for root, dirs, files in os.walk(path): 
        for file in files: #append the file name to the list 
                filelist.append(os.path.join(root,file))
    filelist =sorted(filelist)
    #print(filelist)
    # with open("list_of_files.txt", "w") as file:
    #     print(*filelist, file=file)
    print(len(filelist))
    return(filelist)