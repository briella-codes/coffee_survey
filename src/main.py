import requests, sys, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Any
from IPython.display import display,HTML
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

def load_data(rel_path, encoding_type):
    file_path = ROOT_DIR / rel_path
    return pd.read_csv(file_path,encoding = encoding_type, keep_default_na=False)
#chequear lo de encoding como se maneja, 1ro prueba con utf-8 y si falla detectar the best,
#mejorar esta parte

def display_styled(obj, head=None, tail=None):
    
    if hasattr(obj, "to_frame"):
        df = obj.to_frame(name=obj.name or "value")
    else:
        df =obj
    if head is None and tail is None:
        df_preview = df
    elif head is not None and tail is None:
        df_preview = df.head(head)
    elif head is None and tail is not None:
        df_preview = df.tail(tail)
    else:
        lst = []
        if head:
            lst.append(df.head(head))
        if tail:
            lst.append(df.tail(tail))
        df_preview = pd.concat(lst)
        #df_preview = pd.concat(lst).drop_duplicates()
    

    html = f"""
    <style>
        table {{
            border-collapse: collapse;
            width: max-content;
            max-width: 100%;
            table-layout: auto;
            font-size: 13px;
            border: 4px solid #A665A0;
            color: black;
        }}

        th, td {{
            border: 1px solid #FFFFFF;
            padding: 6px 8px;
            text-align: left;
            border: 1px solid #A665A0;
            white-space: nowrap;
        }}

        thead th {{
            background-color: #C7C7C7;
            position: sticky;
            top: 0;
        }}

        tbody tr:nth-child(even) td, th {{
            background-color: #DEDEDE;
        }}

        tbody tr:nth-child(odd) td, th {{
            background-color: #C2C0C0;
        }}

        tbody th.row_heading.level1 {{
            background-color: #F54927;
            vertical-align: top;
            font-weight: 600;
            
        }}
        tbody th[rowspan] {{
            background-color: white;
            vertical-align: top;
        }}
    </style>


    <div style="overflow-x:auto; max-width:100%;">
        {df_preview.to_html(index=True)}
    </div>
    """

    display(HTML(html))

def standardize_columns(df):
    df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ","_")
    .str.replace("/","_")
    .str.replace("-","_")
    )
    return df

def simplevalue_str_columns(df, columns):
    for col in columns:
        df[col] = df[col].replace({"NA":pd.NA})
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
        df[col] = (df[col].astype("string").str.split(pattern, regex=True) )
        df[col] = df[col].apply( lambda
                                list_ : [s.strip() for s in list_] if isinstance(list_, list)
                                else list_
                                )    
    return df

def clean_ranges_age(df):
    age_order = [
        '<18 years old',
        '18-24 years old',
        '25-34 years old',
        '35-44 years old',
        '45-54 years old',
        '55-64 years old',
        '>65 years old'
    ]
    
    df["age"]= pd.Categorical(df["age"], categories = age_order, ordered=True)
    return df


#podria agregar higher lower  plus etc
#me falta aplicar separador: corregir eso, veri si me conviene por defecto con guion
#queda por mejorarle para valores negativos pero ahora no aplica
def clean_ranges_improved_minmax(df,col,sep="-"):
    
    index = df.columns.get_loc(col)
    min = f"{col}_from_min"
    max = f"{col}_to_max"

    if min not in df.columns:
        df.insert(index+1,min, np.nan)
    if max not in df.columns:
        df.insert(index+2,max, np.nan)

    df[col] = df[col].replace({"NA":pd.NA})
    mask_NA = df[col].isna()
    df.loc[mask_NA,min] = pd.NA
    df.loc[mask_NA,max] = pd.NA

    df_str = df[col].astype("string").str.lower()
    
    df_str = df_str.mask(df_str == "none", "0")
    df_str = df_str.str.replace(r"[$€,]", "", regex=True)

    #for number alone
    mask = (df_str.str.fullmatch(r"\d+", na=False) & ~ mask_NA )
    df.loc[mask, min] = df_str[mask].astype("Float64")
    df.loc[mask, max] = df_str[mask].astype("Float64")
    #less than
    mask = (
        df_str.str.contains("<", na=False) |
        df_str.str.contains("less", case=False, na=False)
        & ~ mask_NA
    )
    number = df_str[mask].str.extract(r"(\d+)")[0].astype("Float64")
    df.loc[mask, min] = 0
    df.loc[mask, max] = number - 0.01
    #more than
    mask = (
            df_str.str.contains(">", na=False) |
            df_str.str.contains("more", case=False, na=False)
            & ~ mask_NA
        )
    number = df_str[mask].str.extract(r"(\d+)")[0].astype("Float64")
    df.loc[mask, min] = number + 0.01
    
    #ranges
    sep_escaped = re.escape(sep)
    sep_pattern = rf"\d+\s*\b{sep_escaped}\b\s*\d+"
    sep_pattern_xtr = rf"(\d+)\s*\b{sep_escaped}\b\s*(\d+)"
    mask = ( df_str.str.contains(sep_pattern, na=False) & ~ mask_NA )
    ranges = df_str[mask].str.extract(sep_pattern_xtr)
    df.loc[mask, min] = ranges[0].astype("Float64")
    df.loc[mask, max] = ranges[1].astype("Float64")

    df[[min, max]] = df[[min, max]].astype("Float64")
    return df
   
def clean_ranges_columns_minmax(df, columns):
    for col in columns:
        df = clean_ranges_improved_minmax(df,col)
    return df

def create_csv(df,filename):
    rel_path = 'data/processed/'
    file_path = ROOT_DIR / rel_path / filename
    file_path.parent.mkdir(parents = True, exist_ok=True)
    df.to_csv(file_path, index=False, na_rep="")

#conteo por grupo de valores pasando una columna
def column_countBy(df, *columns):
    lst = list(columns)
    df_copy =df.copy()
    for col in lst:
        if df[col].map (lambda x: isinstance(x, list)).any().any():
            #df_copy =df.copy()
            #df_copy[columns+'_x'] = df_copy[columns].str.split(r', (?=[A-Z])', regex=True)
            df_copy = df_copy.explode(col)
    
    return df_copy.groupby(lst, observed=True).size().rename('count')

#conteo por grupo de valores pasando una columna caso especial de rangos
def column_countBy_ranges(df, column):
    lst = [column+'_from_min',column+'_to_max']
    df_count = df[df[column+'_from_min'].notna()]
    df_count = df_count.groupby(lst, dropna=False).size().rename('count')
    return df_count


def color_intercalado(cat_barra:list, col1="#C400D2", col2="#7700FF") ->list[str]:
    '''Recibe una lista de categorias para un gráfico de barras, y genera colores intercalados para las barras
        Devuelve una lista con los colores, 1 color por categoria
    '''
    color=[]
    for x in range(len(cat_barra)):
        color+=[col1] if x%2==0 else [col2]
    return color

def graphic_chart_fav_coffee_by_age(fav_coffee_by_age):
    age_groups = fav_coffee_by_age.index

    for grupo in age_groups:
        fav_count = fav_coffee_by_age.loc[grupo]

        fig, ax = plt.subplots(figsize=(8,4))

        bars = ax.bar(
            fav_count.index,
            fav_count.values,
            color=color_intercalado(list(fav_count.index))
        )

        ax.set_title("Fav Coffees for consumers aged: " + grupo, fontsize=18)
        ax.set_ylabel('Number of consumers', fontsize=12)
        #hide x axis
        ax.set_xticks([])

        for bar, label in zip(bars, fav_count.index):
            x_center = bar.get_x() + bar.get_width() / 2
            ax.text(
                x_center,
                0.04,                           
                label,
                ha='center',
                va='bottom',               
                rotation=90,
                fontsize=9,
                color='black',
                transform=ax.get_xaxis_transform(),
                clip_on=False
            )

        for bar in bars:
            x_center = bar.get_x() + bar.get_width() / 2
            ax.text(
                x_center,
                -0.04,                           
                f'{int(bar.get_height())}',
                ha='center',
                va='top',                   
                fontsize=9,
                transform=ax.get_xaxis_transform(),
                clip_on=False
            )

        plt.subplots_adjust(bottom=0.3)
        ax.set_ylim(0, fav_count.values.max() * 1.15)

        plt.show()