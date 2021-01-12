import pandas as pd
import os
import openpyxl
#import sys


root_path = "C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\"

def GetFiles(path):
    files_ = pd.DataFrame( columns=['root', 'name'])
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.split(".")[1] == "rdf":
                #file = os.path.join(root, name)
                # files_.append(file)
                files_.loc[name]=root[root,name]
                
    return files_


# получение номеров тавров
# ! Завернуть в функцию
data=pd.read_csv(
    "SN_TAVR.csv",
    delimiter=';',
    names=['serial_number','station'] )
print(data)


# цикл сравнения
#if __name__ == '__main__':
#    for idx  in data.itertuples():
#        if idx.station=='Песь':
#            print(idx.serial_number)
#      

files = GetFiles(root_path)   