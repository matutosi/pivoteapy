import os
import pandas as pd

def df_to_setting(df):
    """
    Converts a DataFrame into a dictionary of settings.

    Args:
        df (pd.DataFrame): A DataFrame with at least two columns:
            - 'pos': The position or category to group by.
            - 'item': The items to aggregate into lists.

    Returns:
        dict: A dictionary where keys are unique values from the 'pos' column,
              and values are lists of corresponding 'item' values.
    """
    setting = df.groupby("pos")["item"].apply(list)
    return setting.to_dict()

def create_setting_xlsx(item, xlsx_input, start_file = True):
    """
    Creates a settings Excel file based on the provided item and input file.

    This function generates a settings Excel file by combining the provided 
    `item` list with predefined positional labels. The resulting DataFrame 
    is saved as a new Excel file with a name derived from the input file. 
    Optionally, the generated file can be opened automatically.
    Args:
        item (list): A list of items to include in the settings file.
        xlsx_input (str): The path to the input Excel file. The settings file 
                          will be named based on this file.
        start_file (bool, optional): If True, the generated settings file will 
                                     be opened automatically. Defaults to True.
    Returns:
        str: The path to the generated settings Excel file.
    """
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
    """
    Generates a new Excel file with pivoted data and optionally opens it.

    Args:
        pivoted (DataFrame): The pivoted data to be written to the Excel file.
        xlsx_input (str): The file path of the input Excel file. The output file
                          will have the same name with "_pivoted" appended before
                          the file extension.
        start_file (bool, optional): If True, automatically opens the generated
                                     Excel file. Defaults to True.
    Returns:
        str: The file path of the generated Excel file.
    """
    xlsx_output = xlsx_input.replace(".xlsx", "_pivoted.xlsx")
    pivot2xlsx(pivoted, xlsx_output)
    if start_file:
        os.startfile(xlsx_output)
    return xlsx_output

def pivot2xlsx(pivoted, xlsx):
    """
    Exports pivoted data to an Excel file.

    If the input `pivoted` is a dictionary, each key-value pair is treated as 
    a sheet name and its corresponding DataFrame, respectively. Each DataFrame 
    is written to a separate sheet in the Excel file. If `pivoted` is a single 
    DataFrame, it is written to a single sheet named "pivoted".

    Args:
        pivoted (dict or pandas.DataFrame): The pivoted data to export. Can be 
            a dictionary of DataFrames or a single DataFrame.
        xlsx (str): The file path for the output Excel file.

    Returns:
        str: The file path of the created Excel file.
    """
    if type(pivoted) is dict:
        with pd.ExcelWriter(xlsx) as writer:
            for name, df in pivoted.items():
                df.to_excel(writer, sheet_name=str(name), index=False)
    else:
        pivoted.to_excel(xlsx, sheet_name="pivoted", index=False)
    return xlsx

def is_excel_open(filepath):
    """
    Checks if an Excel file is currently open by looking for the presence of a temporary file
    created by Excel when the file is opened.

    Args:
        filepath (str): The full path to the Excel file to check.

    Returns:
        bool: True if the Excel file is open (temporary file exists), False otherwise.
    """
    dir  = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    file_temp = os.path.join(dir, "~$" + file)
    return os.path.exists(file_temp)
