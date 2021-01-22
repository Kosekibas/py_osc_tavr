#TODO открыть файл стандартными средствами
# todo набить скелет стандартный словарь или панду
# todo побайтно проверять данные и закидывать в словарь

import pandas as pd
import os
import numpy as np
import  time # для конвертирования времени

# root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'
# root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"
root_path = 'C:\\KOS\\pyKos\\py_osc_tavr\\Osc\\'
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
dict_graph = {} #пустой словарь настроек отображения графиков
style = { #словарь свойств линий графиков
    'pbChannels':{},
    'pcrColor':{},
    'piLineWidth':{},
    'piLineStyle':{}
}

def Getfiles_osc(path): # Получение списка осциллограмм
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
    # if osc.Index == 0: #если открыли первый файл, то создается массив из файла
        with open (osc.root+osc.name, 'rb') as f_osc:
            #! засунуть проверку на вылет, когда не может декодировать rdf
            dict_vers['extension']=f_osc.read (4).decode('ANSI')
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
                # сообщение в заголовке
                title_log=int.from_bytes(f_osc.read (1),byteorder='little',signed='FALSE') #длинна байт
                title_msg=f_osc.read (title_log).decode(encoding='ANSI') # само сообщение
                # отображение графиков
                osc_graph_format_string_count=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE') #читаем количество отоброжаемых окон графиков
                for n in range(osc_graph_format_string_count): 
                    osc_graph_format_line_count = int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE') #количество графиков в окне
                    for m in range(osc_graph_format_line_count):
                        dict_graph[n]=style
                        dict_graph[n]['pbChannels'][m]=int.from_bytes(f_osc.read (1),byteorder='little',signed='FALSE') # ar>>pView->pCustomPD[i].pbChannels[j]; 1b
                        dict_graph[n]['pcrColor'][m]=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE')     # ar>>pView->pCustomPD[i].pcrColor[j];    4b
                        dict_graph[n]['piLineWidth'][m]=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE') # ar>>pView->pCustomPD[i].piLineWidth[j]; 4b
                        dict_graph[n]['piLineStyle'][m]=int.from_bytes(f_osc.read (4),byteorder='little',signed='FALSE') # ar>>pView->pCustomPD[i].piLineStyle[j]; 4b
                        print(  'nn=',n,
                                'mm=',m, 
                                'pbChannels',(dict_graph[n]['pbChannels'][m]),
                                'pcrColor', dict_graph[n]['pcrColor'][m],
                                'piLineWidth', dict_graph[n]['piLineWidth'][m],
                                'piLineStyle', dict_graph[n]['piLineStyle'][m] 
                                )
                    fDigOnly=f_osc.read (4)  # ar>>pView->pCustomPD[i].fDigOnly;   4b
                    rect=f_osc.read (16)       # ar>>pView->pCustomPD[i].rect;       4*4b
                m_fCaptionEnable=f_osc.read (4) # ar>>pView->m_fCaptionEnable;
                m_fLegendEnable=f_osc.read (4)  # ar>>pView->m_fLegendEnable;
                m_iTotalKadr=f_osc.read (4)    # ar>>m_iTotalKadr;
                iAmountKadr=f_osc.read (4)  # ar>>ViewData.iAmountKadr;
                iFromKadr= f_osc.read (4) # ar>>ViewData.iFromKadr;
                m_iMessageCount=int.from_bytes(f_osc.read (1),byteorder='little',signed='FALSE') #количество сообщений
                print('количество сообщений= ',m_iMessageCount)



        # break


