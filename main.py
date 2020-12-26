#!/usr/bin/python
import os
import openpyxl
import sys

root_path = "C:\Users\��������\Desktop\q"
param_1 = "kt_i_max_down"
param_2 = "kt-imax_down"

def GetFiles(path):
    files_ = list()
    for root, dirs, files in os.walk(path):
       for name in files:
          file = os.path.join(root, name)
          files_.append(file)
    return files_

if __name__ == '__main__':
        if True:
            files = GetFiles(root_path)        
            for file in files:
                if file.split(".")[1] == "csv":
                    file_1 = open(file,"r")
                    buffer = file_1.read()
                    new_buffer = buffer.replace(param_1,param_2)
                    file_1.close()
                    file_2 = open(file, 'w')
                    file_2.write(new_buffer)
                    file_2.close()
                if file.split(".")[1] == "xlsm":
                    wb = openpyxl.load_workbook(file,keep_vba=True)
                    for sheets in wb:
                        for sheet in sheets:
                            for end in sheet:
                                if end.value == param_1:
                                    end.value = param_2
                                    print(".")
                    wb.save(file)
        print("Ok")   
