def _prepare_data(df, row, col, value, split, sep="_"):
    """
    Prepares the data for pivoting by converting categorical columns to strings,
    combining multiple columns if necessary, and handling split columns.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    row (list): List of row labels.
    col (list): List of column labels.
    value (list): List of value labels.
    split (list): List of columns to split by.
    sep (str): Separator used to join multiple columns.

    Returns:
    tuple: A tuple containing the modified DataFrame, new column name, new value name, and new split name (if any).
    """
    cat_cols = df.select_dtypes(include='category').columns
    for col in cat_cols:
        if df[col].dtype.name == 'category':
            df[col] = df[col].astype(str)
    cols = row + col + value + split
    if not all(c in df.columns for c in cols):
        raise ValueError("DataFrame does not contain the specified columns")
    # columns for pivoting
    if 1 < len(col):
        df[col] = df[col].astype(str)
        combined_col = sep.join(col)
        df[combined_col] = df[col].astype(str).apply(sep.join, axis=1)
    else:
        combined_col = col[0]
    # values for pivoting
    if 1 < len(value):
        df[value] = df[value].astype(str)
        combined_value = sep.join(value)
        df[combined_value] = df[value].astype(str).apply(sep.join, axis=1)
    else:
        combined_value = value[0]  # If there's only one value column
    # split for pivoting
    if split:
        combined_split = sep.join(split)
        if 1 < len(split):
            df[combined_split] = df[split].astype(str).apply(sep.join, axis=1)
            df = df.drop(split, axis=1)
        return df, combined_col, combined_value, combined_split
    else:
        return df, combined_col, combined_value, None

def _pivot_data(df, row, combined_col, combined_value, combined_split, sep="_"):
    """
    Pivots the DataFrame based on the provided row, column, value, and split parameters.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    row (list): List of row labels.
    combined_col (str): The new column name created during data preparation.
    combined_value (str): The new value name created during data preparation.
    combined_split (str): The new split name created during data preparation (if any).
    sep (str): Separator used to join multiple columns.

    Returns:
    pd.DataFrame or dict: The pivoted DataFrame or a dictionary of DataFrames if split is provided.
    """
    tmp_col = "tmp_col"
    if combined_split:
        names = []
        values = []
        df_grouped = df.groupby(combined_split, observed=True)
        for name, df_g in df_grouped:
            df_sub_grouped = _add_group_sub(df_g, group = row + [combined_col], sep=sep, tmp_col=tmp_col)
            pivoted = df_sub_grouped.pivot_table(index=row + [tmp_col], columns=combined_col, values=combined_value, aggfunc='first', observed=True)
            pivoted = pivoted.reset_index()
            pivoted = pivoted.drop(tmp_col, axis=1)
            # re-order columns
            combined_cols = str(combined_split).split(sep)
            pivoted.loc[:, combined_cols] = str(name).split(sep)
            cols = [col for col in pivoted.columns if col not in combined_cols]
            pivoted = pivoted[combined_cols + cols]
            names.append(name)
            values.append(pivoted)
        return dict(zip(names, values))
    else:
        df_sub_grouped = _add_group_sub(df, group = row + [combined_col], sep=sep, tmp_col=tmp_col)
        pivoted = df_sub_grouped.pivot_table(index=row + [tmp_col], columns=combined_col, values=combined_value, aggfunc='first', observed=True)
        pivoted = pivoted.reset_index()
        pivoted = pivoted.drop(tmp_col, axis=1)
        return pivoted

def _add_group_sub(df, group, sep="_", tmp_col="tmp_col"):
    """
    Adds a temporary column to the DataFrame for grouping purposes.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    group (list or str): The column(s) to group by.
    sep (str): Separator used to join multiple columns.
    tmp_col (str): The name of the temporary column to be added.

    Returns:
    pd.DataFrame: The modified DataFrame with the temporary column added.
    """
    if isinstance(group, str):
        group = [group]
    g_0 = df[group[0]].astype(str)
    digits = len(str(df.index.max()))
    n_in_group = df.groupby(group).cumcount().astype(str).str.zfill(digits)
    df[tmp_col] = g_0 + sep + n_in_group
    return df


def _clean_data(result):
    """Cleans up the pivoted data."""
    if isinstance(result, dict):
        result = {key: value for key, value in result.items() if len(value) > 0}
        result = {key: _na2empty(value) for key, value in result.items() if len(value) > 0}
    else:
        result = result.fillna('')
    return result

def _na2empty(df):
    return df.fillna('')

def pivot(df, row, col, value, split=None, sep="_", rm_empty_df=True):
    """
    Pivots the DataFrame based on the provided row, column, value, and split parameters.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    row (list): List of row labels.
    col (list): List of column labels.
    value (list): List of value labels.
    split (list, optional): List of columns to split by. Defaults to None.
    sep (str, optional): Separator used to join multiple columns. Defaults to "_".
    rm_empty_df (bool, optional): Flag to remove empty DataFrames from the result. Defaults to True.

    Returns:
    pd.DataFrame or dict: The pivoted DataFrame or a dictionary of DataFrames if split is provided.
    """
    if split is None:
        split = []
    df, combined_col, combined_value, combined_split = _prepare_data(df, row, col, value, split, sep)
    result = _pivot_data(df, row, combined_col, combined_value, combined_split)
    result = _clean_data(result)
    return result
