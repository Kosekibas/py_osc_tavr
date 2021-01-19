import pandas as pd
import os
import numpy as np

bufType = np.dtype(
    [
        ('b1', 'i2'),
        ('b2', 'i2'),
        ('b3', 'i2'),
        ('b4', 'i2'),
        ('b5', 'i2'),
        ('b6', 'i2'),
        ('b7', 'i2'),
        ('b8', 'i2'),
        ('b9', 'i2'),
        ('b10', 'i2'),
        ('b11', 'i2'),
        ('b12', 'i2'),
        ('b13', 'i2'),
        ('b14', 'i2'),
        ('b15', 'i2')
    ]
)

# root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'
root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"
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
                        dtype=bufType, count=1, offset=4)
        # parser_beginning=
    else: #если файл не первый, то к существующему массиву прибавляем строку из файла
        parser_beginning=np.append(parser_beginning,np.fromfile(osc.root+osc.name,
                        dtype=bufType, count=1, offset=4) )
      
pd_parser=pd.DataFrame(parser_beginning) # конвертируем numpy в pandas
pd_parser.merge(files_osc.name,how='left', left_on='index',right_on='index')
print(pd_parser)