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

root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'

def Getfiles_osc(path):
    files_osc_ = pd.DataFrame( columns=['root', 'name'])
    for root, dirs, files_osc in os.walk(path):
        for name in files_osc:
            name_list=name.split(".")
            if name_list[len(name_list)-1] == "rdf":
                # size=os.path.getsize(root+'\\'+name) # получить информацию и размере файла
                files_osc_.loc[files_osc_.shape[0]]=[root,name]
    return files_osc_



files_osc = Getfiles_osc(root_path)   #составления списка осцилограмм

parser_array=pd.DataFrame(columns=bufType.names)
for osc  in files_osc.itertuples(): # перебор путей найденных файлов осцилограм
    parser= np.fromfile(osc.root+osc.name,
                    dtype=bufType, count=1, offset=4)
    pdp=pd.DataFrame(parser)
    # parser_array.loc[osc.Index]=[pdp]
    
    # parser_array=pd.concat([parser_array,parser])
print(parser_array)