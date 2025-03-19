import glob
import os
import time
import pandas as pd
import TkEasyGUI as sg

def df_to_setting(df):
    setting = df.groupby("pos")["item"].apply(list)
    return setting.to_dict()

def create_setting_xlsx(item, xlsx_input, start_file = True):
    pos = ["sheet", "row", "col", "cell"]
    item = list(item)
    null = [""] * 5
    max_len = max(len(item), len(pos))
    item = null + item + [""] * (max_len - len(item))
    pos  = null + pos + [""] * (max_len - len(pos))
    df_setting = pd.DataFrame({'pos': pos, 'item': item})
    path_setting = xlsx_input.replace(".xlsx", "_") + 'setting.xlsx'
    if not os.path.exists(path_setting):
        df_setting.to_excel(path_setting, index=False)
    if start_file:
        os.startfile(path_setting) 
    return path_setting

def create_output_xlsx(pivoted, xlsx_input, start_file = True):
    xlsx_output = xlsx_input.replace(".xlsx", "_pivoted.xlsx")
    pivot2xlsx(pivoted, xlsx_output)
    if start_file:
        os.startfile(xlsx_output)
    return xlsx_output


def pivot2xlsx(pivoted, xlsx):
    if type(pivoted) is dict:
        with pd.ExcelWriter(xlsx) as writer:
            for name, df in pivoted.items():
                df.to_excel(writer, sheet_name=str(name), index=False)
    else:
        pivoted.to_excel(xlsx, sheet_name="pivoted", index=False)
    return xlsx

def is_excel_open(filepath):
    dir  = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    file_temp = dir + "/~$" + file
    return os.path.exists(file_temp)
