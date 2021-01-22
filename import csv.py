import pandas as pd
import os
import shutil # для копирования файлов


#! drop_duplicates поиск дубликатов на панде

#root_path = "C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\"
#root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"
root_path = '//vault2/Бесконтактная техника/1 ОБТ'
#root_path = '//vault2/Бесконтактная техника'
copy_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'

def Getfiles_osc(path):
    files_osc_ = pd.DataFrame( columns=['root', 'name','number'])
    for root, dirs, files_osc in os.walk(path):
        for name in files_osc:
            name_list=name.split(".")
            if name_list[len(name_list)-1] == "rdf":
                # size=os.path.getsize(root+'\\'+name) # получить информацию и размере файла
                files_osc_.loc[files_osc_.shape[0]]=[root,name,'0']
                
    return files_osc_


def Copyfiles_osc(osc,patch): # копирование файла
    count_=0
    for files_  in osc.itertuples(): # перебор путей найденных файлов осцилограм
        if files_.number =='0': # если номер тавра не определен
            print('номер не определен' )
            continue # пропустим итерацию
        first=files_.root+'\\'+files_.name #откуда копируем
        end= patch + files_.number+'-'+files_.name # куда копируем
        if os.path.exists(end) :   # если такой файл уже есть в куда копируем
            print('файл ', files_.number,'-',files_.name , 'уже присутствует' )
            continue # пропустим итерацию
        else :
            shutil.copy(first, end) # функция копирования
        count_+=1
        # if count_==3:  return False #копирование первых ...
    return True

# импорт номеров тавров из csv файла 
all_tavr=pd.read_csv(
    "SN_TAVR.csv",
    delimiter=';',
    names=['serial_number','station'] )



files_osc = Getfiles_osc(root_path)   #составления списка осцилограмм
print('Нащел ', files_osc.shape[0]-1, 'осцилограмм') 


# цикл сравнения
if __name__ == '__main__':
    count=0
    for tavr  in all_tavr.itertuples(): # перебор станций по массиву номеров тавр
        for osc  in files_osc.itertuples(): # перебор путей найденных файлов осцилограм
            folder_name=str.split(osc.root, sep='\\') # разбивка пути файла на названия папок
            for name in folder_name: #перебор названий каждой папки
                if tavr.station==name: # если совпало название папки и название станции
                    if files_osc.number[osc.Index]=='0':
                        count+=1 #счетчик найденых номеров к осциллограммам
                        files_osc.number[osc.Index]=str(tavr.serial_number) #!! записываем в массив номер тавра
                    else:
                        files_osc.number[osc.Index]=str(files_osc.number[osc.Index])+','+str(tavr.serial_number)
    print('нащел ', count, 'совпадений')
    #no_dublicat=files_osc.drop_duplicates(subset=['name','number']) # поиск дубликатов и удаление дубликатов
    #no_dublicat.to_csv('no_dublicat.csv') # экспорт в csv файл
    files_osc.to_csv('Osc_number.csv') # экспорт в csv файл
    # копирование в папку
    if input("копировать? (y/n)") == 'y':
        if Copyfiles_osc(files_osc,copy_path):
            print('полное копирование ОК')
        else:
            print('частичное копирование ОК')