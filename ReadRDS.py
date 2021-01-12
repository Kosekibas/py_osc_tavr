# 
# todo  распарсить аналоги 
# todo  распарсить журнал
# todo  сравнить времена записи осцилограммы и записи журнала
# todo  установка маркеров согласно алгоритму. хотябы поиск первичного события
# ! приоритет
# !! эта куча оживет если смогу сопоставить к какому тавру какие осцилограммы относятся 
    # todo информация может содержаться только в пути файла (какая нпска) эту информацию необходимо поместить в имя файла, желательно чтобы № устройства
    # ? * файлы будут повторяться, проверку осуществлять по аналоговому сигналу напруги
    # ? перебираем по очереди все файлы
        # ? из пути извлекаем инфу
        # ? прогоняем инфу по таблице, чтобы привязать номер тавра к устройству
        # ? сохраняем файл в новой директории с новым именем NNN_date.rdf
            # ? если в этой директории файл уже есть то * и откидываем его или сохраняем как копию NNN_date_001.rdf
            

import matplotlib.pyplot as plt
import numpy as np
import time
dio_name = {
            1: 'o_1',
            2: 'o_2',
            3: 'o_3',
            4: 'o_4',
            5: 'o_5',
            6: 'o_6',
            7: 'o_7',
            8: 'o_8',
            9: 'o_9',
            10: 'o_10',
            11: 'o_11',
            12: 'o_12',
            13: 'i_cb2_on',
            14: 'i_cbs_on',
            15: 'i_cb1_on',
            16: 'empty',
            17: 'i_kt_imax',
            18: 'i_kt_imin2',
            19: 'i_kt_imin3',
            20: 'i_sync_ready',
            21: 'i_cb1_phase',
            22: 'i_cb1_u08',
            23: 'i_cb1_u06',
            24: 'i_cb1_imax',
            25: 'i_cb1_imin',
            26: 'i_cb1_u09',
            27: 'i_cb2_phase',
            28: 'i_cb2_u08',
            29: 'i_cb2_u06',
            30: 'i_cb2_imax',
            31: 'i_cb2_imin',
            32: 'i_cb2_u09',
            }

bufType = np.dtype(
    [
        ('Ia1', 'i2'),
        ('Ic1', 'i2'),
        ('Ia2', 'i2'),
        ('Ic2', 'i2'),
        ('Iakt', 'i2'),
        ('Ickt', 'i2'),
        ('Uab1', 'i2'),
        ('Uab2', '<i2'),
        ('Dio', 'u4')
    ]
)

osc = np.fromfile('E:/KosPy/Samples/py_osc_tavr/Osc/2.rdf',
                     dtype=bufType, count=1500, offset=34)


# График мультизонный
# https://nbviewer.jupyter.org/github/whitehorn/Scientific_graphics_in_python/blob/master/P2%20Chapter%207%20Subplots.ipynb
# https://pyprog.pro/mpl/mpl_main_components.html

# DIO
fig, axes = plt.subplots(nrows=32, ncols=1)

n = 1
for ax in axes.flat:
    ax.set(xticks=[], yticks=[])
    ax.set_ylim(ymin=-0.1, ymax=1.1)
    ax.set_xlim(xmin=0, xmax=1500)
    ax.text(-150, 0.0, str(dio_name[n]), color='black')
    ax.stem(~(osc['Dio'] >> n-1) & 1, linefmt='C0-',
            markerfmt='C0-', basefmt='C0-')
    n += 1
plt.show()

#Analog
#!
#save('pic_7_2_1', fmt='png')
#save('pic_7_2_1', fmt='pdf')
