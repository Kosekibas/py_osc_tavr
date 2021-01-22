#TODO открыть файл стандартными средствами
# todo набить скелет стандартный словарь или панду
# todo побайтно проверять данные и закидывать в словарь

import pandas as pd
import os
import numpy as np
import  time # для конвертирования времени

root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'
# root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"

# словарь версий файла
dict_vers = {
    'extension': ".PDF",
    'v1': 0, 
    'v2': 0,
    'v3': 0,
    'v4': 0,
    'v5': 0,
    'v6': 0,
    'time': 0
    }

def Getfiles_osc(path):
    files_osc_ = pd.DataFrame( columns=['root', 'name'])
    for root, dirs, files_osc in os.walk(path):
        for name in files_osc:
            name_list=name.split(".")
            if name_list[len(name_list)-1] == "rdf": #сравнение именно последнего расширения после точки, отсеивается rdf.bak и прочее
                # size=os.path.getsize(root+'\\'+name) # получить информацию и размере файла
                files_osc_.loc[files_osc_.shape[0]]=[root,name]
    return files_osc_

files_osc = Getfiles_osc(root_path)   #составления списка осцилограмм

for osc  in files_osc.itertuples(): # перебор путей найденных файлов осцилограм
    if osc.Index == 0: #если открыли первый файл, то создается массив из файла
        with open (osc.root+osc.name, 'rb') as f_osc:
            #! засунуть проверку на вылет, когда не может декодировать rdf
            dict_vers['extension']=f_osc.read (4).decode('ascii')
            print("формат=",dict_vers['extension'])
            if dict_vers['extension']=="RDF":
                dict_vers['v1']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['v2']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['v3']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['v4']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['v5']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['v6']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                dict_vers['time']=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')
                print(dict_vers)
                log=f_osc.read (30050)
                Len_log=int.from_bytes(f_osc.read (1),byteorder='little',signed='FALSE')
                print('длинна заголовка',Len_log,'hex=',hex(Len_log))
        break


