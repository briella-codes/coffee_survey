import pandas as pd
from typing import Any


#=========================================================================================
#PREPROCESSING , DATA STRUCTURE RELATED FUNCTIONS:

def standardize_columns(df):
    df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ","_")
    .str.replace("?","")
    .str.replace("/","_")
    .str.replace("-","_")
    )
    return df


def simplevalue_str_columns(df, columns):
    for col in columns:
        df[col] = df[col].replace({"NA":pd.NA})
        df[col] = df[col].replace({"":pd.NA})
        df[col] = (df[col].astype("string").str.strip())
    return df


def int_value_columns(df, columns):
    for col in columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace({"":pd.NA, "NA":pd.NA}).astype(float)
        df[col] = df[col].astype("Int64")
    return df


def split_multivalue_columns(df, columns, default_pattern = r', ', col_patterns = None):
    if col_patterns is None:
        col_patterns = {}
    
    for col in columns:
        pattern = col_patterns.get(col, default_pattern)
        #'String' es la evolucion de 'str', me evita usar dropna con 'str'
        df[col] = df[col].replace({"NA":pd.NA})
        df[col] = (df[col].astype("string").str.split(pattern, regex=True))
        
        df[col] = df[col].map( lambda
                                x : tuple(s.strip() for s in x) if isinstance(x, list)
                                else x
                                )

    return df


def set_ordinal_categories(df, order_config):
    """
    set categories type to categorical columns and gives order,
    order_config must be a dictionary where keys are columns names
    and values are lists with orderer elements that represents the ordered categories

    """

    for column_name, order in order_config.items():
        df[column_name]= pd.Categorical(df[column_name], categories = order, ordered=True)

    return df


#=========================================================================================
#MISSING DATA RELATED FUNCTIONS:
def missing_data_count(df,porc=10):
    total = len(df)
    missing = df.isnull().sum()
    perc = (missing*100)/total
    missing_df = pd.DataFrame({
            "missing" : missing ,
            "total" : total,
            "percentage" : perc
        }).sort_values("missing", ascending=False)
    missing_df = missing_df[missing_df["percentage"]>porc]
    return missing_df
