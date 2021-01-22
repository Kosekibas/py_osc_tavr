import pandas as pd
import os
import numpy as np
import  time # для конвертирования времени
delta_sec=312854400 # мутная константа(секунды), прибавляется к распарсенному времени, чтобы получить правду
bufType = np.dtype(
    [
        ('b1', 'u4'),
        ('b2', 'u4'),
        ('b3', 'u4'),
        ('b4', 'u4'),
        ('b5', 'u4'),
        ('b6', 'u4'),
        ('b7', 'u4'),
        ('b8', 'u4'),
        ('b9', 'u4'),
        ('b10', 'u4'),
        ('b11', 'u4'),
        ('b12', 'u4'),
        ('b13', 'u4'),
        ('b14', 'u4'),
        ('b15', 'u4')
    ]
)

root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'
# root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"

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
        parser_beginning= np.fromfile(osc.root+osc.name,
                        dtype=bufType, count=1, offset=30034)

    else: #если файл не первый, то к существующему массиву прибавляем строку из файла
        parser_beginning=np.append(parser_beginning,np.fromfile(osc.root+osc.name,
                        dtype=bufType, count=1, offset=30034) )

pd_parser=pd.DataFrame(parser_beginning) # конвертируем numpy в pandas
pd_parser=pd_parser.merge(files_osc.name,how='right', left_index=True, right_index=True) # добавление к распарсеному имен файлов

print(pd_parser)
pd_parser.to_csv('parser_ende.csv') # экспорт в csv файл