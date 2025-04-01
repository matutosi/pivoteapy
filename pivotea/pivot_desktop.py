import os
import time
import glob
import pandas as pd
import TkEasyGUI as sg

import pivot
import utils

# read and open input file
xlsxs = glob.glob("./*.xlsx")
xlsxs = [file for file in xlsxs if "setting" not in file and "pivoted" not in file]
if 1 != len(xlsxs):
    xlsx_input = sg.popup_get_file('Select an input file', file_types = (("Excel File", ".xlsx"),))
else:
    xlsx_input = xlsxs[0]

df_input = pd.read_excel(xlsx_input)
cols = df_input.columns
os.startfile(xlsx_input)

# create and open setting file
xlsx_setting = utils.create_setting_xlsx(cols, xlsx_input, start_file=True)

while utils.is_excel_open(xlsx_setting):
    time.sleep(0.1)

# read and set settings
df_setting = pd.read_excel(xlsx_setting)
setting = utils.df_to_setting(df_setting)

col   = setting.get('col')
row   = setting.get('row')
value = setting.get('cell')
split = setting.get('sheet')
if split is None:
    split = []

# pivot
pivoted = pivot.pivot(df_input, row = row, col = col, value = value, split = split)

# save and open Excel
xlsx_output = utils.create_output_xlsx(pivoted, xlsx_input, start_file=True)

os.startfile(xlsx_output)
