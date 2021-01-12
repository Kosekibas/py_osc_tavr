import pandas as pd
import os
#import openpyxl
#import sys


#root_path = "C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\"
root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"

def Getfiles_osc(path):
    files_osc_ = pd.DataFrame( columns=['root', 'name','number'])
    for root, dirs, files_osc in os.walk(path):
        for name in files_osc:
            if name.split(".")[1] == "rdf":
                #file = os.path.join(root, name)
                # files_osc_.append(file)
                files_osc_.loc[files_osc_.shape[0]]=[root,name,0]
                
    return files_osc_


# получение номеров тавров
# ! Завернуть в функцию
all_tavr=pd.read_csv(
    "SN_TAVR.csv",
    delimiter=';',
    names=['serial_number','station'] )
print(all_tavr)


     

files_osc = Getfiles_osc(root_path)   
print(files_osc)


# цикл сравнения
if __name__ == '__main__':
    for tavr  in all_tavr.itertuples(): # перебор станций по массиву номеров тавр
         for osc  in files_osc.itertuples(): # перебор путей найденных файлов осцилограм
            folder_name=str.split(osc.root, sep='\\') # разбивка пути файла на названия папок
            for name in folder_name: #перебор названий каждой папки
                if tavr.station==name: # если совпало название папки и название станции
                    print('YES!')
                    print(tavr.serial_number)
                    files_osc.number[osc.Index]=tavr.serial_number #!! записываем в массив номер тавра
                    print(files_osc)
    print('End')
 #todo экспорт в csv файл