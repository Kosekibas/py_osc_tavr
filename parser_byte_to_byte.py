# todo набить скелет стандартный словарь или панду
# todo побайтно проверять данные и закидывать в словарь
        # TODO засовывать сообщение в таблицу через обращение UPDATE table1 SET name = ‘Людмила Иванова’ WHERE id = 2; 

import os
import pandas as pd
import numpy as np
import  time # для конвертирования времени

import sqlite3
from sqlite3 import Error

# root_path = 'C:\\Users\\Владелец\\Desktop\\Examples\\python\\Osc\\dir\\'
# root_path = "E:\\KosPy\\Samples\\py_osc_tavr\\Osc\\"
root_path = 'C:\\KOS\\pyKos\\py_osc_tavr\\Osc\\dir\\'
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

#собираем SQL запрос динамически 
q_create_table_msg = """ 

"""

dict_graph = {} #пустой словарь настроек отображения графиков
# style = { #словарь свойств линий графиков
#     'pbChannels':{},
#     'pcrColor':{},
#     'piLineWidth':{},
#     'piLineStyle':{}
# }

#пустой словарь настроек отображения графиков


dict_code={
    0:'СЕКЦИOHHЫЙ BKЛЮЧЕH',
    1:'BBOДНОЙ 1 OTKЛЮЧEH',
    2:'BBOДНОЙ 2 OTKЛЮЧEH',
    3:'KT B KOHTPOЛ.ПОЛОЖEH',
    4:'ЗАЩИТНЫЙ ОТКЛЮЧЕ',
    5:'OЖИДАHИE',
    6:'KЛЮЧ - ABP',
    7:'ЗАПРЕТ ПО НАПРЯЖЕНИЮ',
    8:'КЗ НА ШИНАХ',
    9:'ПРОБОЙ КТ-ЗМВ ОТКЛ.',
    10:'Imax КТ-ЗМВ ОТКЛ.',
    11:'ВКЛ. АВТОМАТИЧ. ВНР',
    12:'АВТОМАТИЧ. ВНР ОТКЛ',
    13:'НЕ ВКЛЮЧЕН ПОДОГРЕВ',
    14:'U СШ - НЕТ НОРМЫ',
    15:'НЕСООТВ-ИЕ УРОВНЕЙ U',
    16:'ЗАПРЕТ-СИГНАЛ 3Uo',
    17:'ЗАПРЕТ-ВНЕШН.ЗАПРЕТ',
    18:'ТН ВВОДА - НЕТ НОРМЫ',
    19:'СИГНАЛ: U1 ОТСТАЕТ',
    20:'СИГНАЛ: U2 ОТСТАЕТ',
    21:'СИГНАЛ: Imin КТ',
    22:'НЕТ СИНХРОНИЗАЦИИ',
    100:'OTKAЗПИТАНИЯ',
    101:'OTKAЗГУ',
    102:'OTKAЗНТМИ',
    103:'OTKAЗ-',
    104:'OTKAЗU1: <0.6',
    105:'OTKAЗU2: <0.6',
    106:'OTKAЗОТКЛ ВВОДА 1',
    107:'OTKAЗОТКЛ ВВОДА 2',
    108:'OTKAЗОТКЛ СЕКЦИОН',
    109:'OTKAЗОТКЛ ЗАЩИТН',
    110:'OTKAЗВКЛ ВВОДА 1',
    111:'OTKAЗВКЛ ВВОДА 2',
    112:'OTKAЗВКЛ СЕКЦИОН.',
    113:'OTKAЗВКЛ КТ',
    114:'OTKAЗ-',
    115:'OTKAЗКТ:Imax',
    116:'OTKAЗДАТЧИКА U СШ',
    117:'OTKAЗU1:КЗ',
    118:'OTKAЗU2:КЗ',
    200:'TABP:ОТКЛ ВВ1-НОРМА',
    201:'TABP:ОТКЛ ВВ1-2ФАЗЫ',
    202:'TABP:ОТКЛ ВВ2-НОРМА',
    203:'TABP:ОТКЛ ВВ2-2ФАЗЫ',
    204:'BO3BPAT:BKЛ ВВ1',
    205:'BO3BPAT:BKЛ ВВ2'
}
dict_osc={} #словарь всей осицлограммы

def Getfiles(path,extension): # Получение списка файлов в папке
    files_ = pd.DataFrame( columns=['root', 'name'])
    for root, dirnames , filenames in os.walk(path):
        for name_full in filenames:
            name=name_full.split(".")
            if name[len(name)-1] == extension: #сравнение именно последнего расширения после точки, отсеивается rdf.bak и прочее
                files_.loc[files_.shape[0]]=[root,name_full]
    return files_


def Parsing_osc (root_path):
    connect=sql_connection()
    sql_table(connect)
    for osc  in files_osc.itertuples(): # перебор путей найденных файлов осцилограм
        with open (osc.root+osc.name, 'rb') as file:
            # dict_osc[osc.Index]=RdfVersion1(file,osc.name) #парсинг в словарь питона
            RdfToDb(file,osc.Index,osc.name,connect)


# парсинг в словарь питона
def RdfVersion1(file,name): 
    dict_msg={}
    #! засунуть проверку на вылет, когда не может декодировать rdf
    dict_vers['extension']=file.read (4).decode('ANSI')
    # print("формат=",dict_vers['extension'])
    if dict_vers['extension']=="RDF":
        dict_vers['v1']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['v2']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['v3']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['v4']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['v5']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['v6']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        dict_vers['time']=int.from_bytes(file.read (4),byteorder='little',signed=0)
        # print(dict_vers)
        log=file.read (30050)
        # сообщение в заголовке
        title_log=int.from_bytes(file.read (1),byteorder='little',signed=0) #длинна байт
        title_msg=file.read (title_log).decode(encoding='ANSI') # само сообщение
        # отображение графиков
        osc_graph_format_string_count=int.from_bytes(file.read (4),byteorder='little',signed=0) #читаем количество отоброжаемых окон графиков
        for n in range(osc_graph_format_string_count): 
            osc_graph_format_line_count = int.from_bytes(file.read (4),byteorder='little',signed=0) #количество графиков в окне
            for m in range(osc_graph_format_line_count):
                #? бесполезная для меня информация об отображении графиков, но посколку ее длинна переменна двумя циклами перебираем....
                # dict_graph[n]=style
                # dict_graph[n]['pbChannels'][m]=int.from_bytes(file.read (1),byteorder='little',signed=0) # ar>>pView->pCustomPD[i].pbChannels[j]; 1b
                # dict_graph[n]['pcrColor'][m]=int.from_bytes(file.read (4),byteorder='little',signed=0)     # ar>>pView->pCustomPD[i].pcrColor[j];    4b
                # dict_graph[n]['piLineWidth'][m]=int.from_bytes(file.read (4),byteorder='little',signed=0) # ar>>pView->pCustomPD[i].piLineWidth[j]; 4b
                # dict_graph[n]['piLineStyle'][m]=int.from_bytes(file.read (4),byteorder='little',signed=0) # ar>>pView->pCustomPD[i].piLineStyle[j]; 4b
                #?.... и пропускаем нужное количество байт
                file.seek(file.tell()+13)
            #? бесполезная пока инфа но переменная от цикла..
            # fDigOnly=file.read (4)  # ar>>pView->pCustomPD[i].fDigOnly;   4b
            # rect=file.read (16)       # ar>>pView->pCustomPD[i].rect;       4*4b
            #? ... пропускаем
            file.seek(file.tell()+20)
        #? бесполезная пока инфа постоянной величины..
        # m_fCaptionEnable=file.read (4) # ar>>pView->m_fCaptionEnable;
        # m_fLegendEnable=file.read (4)  # ar>>pView->m_fLegendEnable;
        # m_iTotalKadr=file.read (4)    # ar>>m_iTotalKadr;
        # iAmountKadr=file.read (4)  # ar>>ViewData.iAmountKadr;
        # iFromKadr= file.read (4) # ar>>ViewData.iFromKadr;
        #? ... пропускаем
        file.seek(file.tell()+20)
        # парсим сообщения
        m_iMessageCount=int.from_bytes(file.read (4),byteorder='little',signed=0) #количество сообщений
        for m in range(m_iMessageCount):
            dict_msg[m]={'num':0,'time':0,'msg':0,'style':0,'code':0}   
            dict_msg[m]['num']=int.from_bytes(file.read (2),byteorder='little',signed=0)
            dict_msg[m]['time']=int.from_bytes(file.read (4),byteorder='little',signed=0)
            dict_msg[m]['msg']=file.read (1).decode('ANSI')
            dict_msg[m]['style']=file.read (1).decode('ANSI')
            dict_msg[m]['code']=dict_code[int.from_bytes(file.read (1),byteorder='little',signed=0 )]
            if dict_msg[m]['time'] == dict_vers['time']:
                event_counter=1
                event= dict_msg[m]['code']
            elif dict_msg[m]['time']+1 == dict_vers['time']:
                event_counter=2
                event= dict_msg[m]['code']
            elif dict_msg[m]['time']+2 == dict_vers['time']:
                event_counter=3
                event= dict_msg[m]['code']
            else:
                event_counter=0
                event= 'не найден'
        return {"name":name,"info":dict_vers,"msg":dict_msg}

#парсинг в БД
def RdfToDb(file,Index,name,con): 
    cursor = con.cursor() # обьявляем курсор
    #! засунуть проверку на вылет, когда не может декодировать rdf
    file_extension =file.read (4).decode('ANSI')
    if file_extension=="RDF":
        list_version=[ #парсим заголовок
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v1
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v2
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v3
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v4
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v5
            int.from_bytes(file.read (4),byteorder='little',signed=0), # v6
        ]
        file_date=int.from_bytes(file.read (4),byteorder='little',signed=0) # date
        # прыгнуть курсором в первый аналоговый вход записать его в контрольный. На основане данного контрольного и вермени создания проверять на повторы
        file.seek(46) # скачем к первым выборкам Uab по вводам
        file_control=int.from_bytes(file.read (4),byteorder='little',signed=0) # читаем их вместе
        file.seek(32)
        # тут производить проверу на уникальность.
        cursor.execute('SELECT id FROM files WHERE "date"=? AND "control"=?',(file_date,file_control))
        is_duplicate = cursor.fetchall()
        if is_duplicate:
            print("Уже в списке")
            return
        
        #парсим выборки
        sample_count=int.from_bytes(file.read (2),byteorder='little',signed=0)//10 #количество выборок на осцилограмму(10 байт на выборку(//деление int без остатка)) 
        list_sample=[]
        for n in range(sample_count): 
            # строка выборок 
            list_sample.append([
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (2),byteorder='little',signed=1), #
                int.from_bytes(file.read (1),byteorder='little',signed=0), #
                int.from_bytes(file.read (1),byteorder='little',signed=0), #
                int.from_bytes(file.read (1),byteorder='little',signed=0), #
                int.from_bytes(file.read (1),byteorder='little',signed=0), #
            ])
        print(121)
        # log=file.read (30050)

        # сообщение в заголовке
        title_log=int.from_bytes(file.read (1),byteorder='little',signed=0) #длинна байт
        title_msg=file.read (title_log).decode(encoding='ANSI') # само сообщение 

        #!! кривенько компонуем строку, нужно пересмотреть метод
        list_files=[file_date,name,title_msg,file_control]
        list_files.extend(list_version)
        # TODO экспорт в БД производить вне функции выплевывая из нее массив данных.
        cursor.execute('INSERT INTO "files"("date","name","usr_msg","control","v1","v2","v3","v4","v5","v6") VALUES(?,?,?,?,?,?,?,?,?,?)', list_files)
        # получаем индекс присвоенный в бД
        index=cursor.execute('SELECT LAST_INSERT_ROWID()').lastrowid
        # прописываем индекс в список выборок
        for n in range(sample_count): 
            list_sample[n].append(index)
        # прописываем в БД
        cursor.executemany('INSERT INTO "samples" VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)', list_sample)

        # отображение графиков
        osc_graph_format_string_count=int.from_bytes(file.read (4),byteorder='little',signed=0) #читаем количество отображаемых окон графиков
        for n in range(osc_graph_format_string_count): 
            osc_graph_format_line_count = int.from_bytes(file.read (4),byteorder='little',signed=0) #количество графиков в окне
            for m in range(osc_graph_format_line_count):
                file.seek(file.tell()+13) #? ... пропускаем
            file.seek(file.tell()+20) #? ... пропускаем
        file.seek(file.tell()+20)#? ... пропускаем

        # парсим сообщения
        m_iMessageCount=int.from_bytes(file.read (4),byteorder='little',signed=0) #количество сообщений
        #TODO проверка если сообщений 0
        event= 'не найден'
        for m in range(m_iMessageCount): # парсим сообщения построчно
            list_msg=[
                int.from_bytes(file.read (2),byteorder='little',signed=0), #num
                int.from_bytes(file.read (4),byteorder='little',signed=0), #time
                file.read (1).decode('ANSI'),   #msg
                file.read (1).decode('ANSI'),   #style
                dict_code[int.from_bytes(file.read (1),byteorder='little',signed=0 )], #code
                index
                ]
            # переносим в таблицу сообщений
            cursor.execute('INSERT INTO "msg"(num, date, msg, style, code, id_osc) VALUES(?, ?, ?, ?, ?,?)', list_msg)
            # ищем событие соответствующее времени создания осцилограммы 
            if event== 'не найден':
                if list_msg[1] == file_date:
                    print('событие смещено по времени на ', 0 ,'сек.')
                    event= list_msg[4]
                elif list_msg[1]+1 ==file_date:
                    print('событие смещено по времени на ', 1 ,'сек.')
                    event= list_msg[4]
                elif list_msg[1]+2 == file_date:
                    print('событие смещено по времени на ', 2 ,'сек.')
                    event= list_msg[4]
                if event== 'АВТОМАТИЧ. ВНР ОТКЛ':
                    event='не найден'
        # добавляем найденное событие
        cursor.execute("""UPDATE files SET "event" =?  WHERE "id" = ?""",[event,index])
        con.commit() 


def sql_connection(): # подключение базы данных
    try:
        con = sqlite3.connect("kos_sqllite_temp.db")
        return con
    except Error:
        print(Error)

def sql_table(con): # создание таблицы
    cursor = con.cursor() # обьявляем курсор
    #создаем таблицу сообщений если она еще не существует
    cursor.execute("""CREATE TABLE IF NOT EXISTS "msg" (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    num INTEGER, 
    date INTEGER, 
    msg TEXT, 
    style TEXT, 
    code TEXT,
    id_osc INTEGER
    )""") 

    #  таблица файлов
    cursor.execute("""CREATE TABLE IF NOT EXISTS "files" (
    "id" INTEGER PRIMARY KEY UNIQUE, 
    "number"INTEGER,
    "event" TEXT, 
    "date" INTEGER, 
    "name" TEXT, 
    "usr_msg" TEXT,
    "v1" INTEGER, 
    "v2" INTEGER, 
    "v3" INTEGER, 
    "v4" INTEGER, 
    "v5" INTEGER, 
    "v6" INTEGER,
    "control" INTEGER
    )""")

    # таблица выборок 
    cursor.execute("""CREATE TABLE IF NOT EXISTS "samples" (
    "id" INTEGER PRIMARY KEY UNIQUE, 
    "Ia1"INTEGER,
    "Ic1" INTEGER, 
    "Ia2" INTEGER, 
    "Ic2" INTEGER, 
    "Iakt" INTEGER,
    "Ickt" INTEGER, 
    "Uab1" INTEGER, 
    "Uab2" INTEGER, 
    "DIO_1" INTEGER, 
    "DIO_2" INTEGER, 
    "DIO_3" INTEGER,
    "DIO_4" INTEGER,
    "id_osc" INTEGER
    )""")

    con.commit()    # сохраняем изменения

if __name__ == '__main__':
    files_osc = Getfiles(root_path,"rdf")   #составления списка осцилограмм
    Parsing_osc (root_path)
    # print (dict_osc[1])