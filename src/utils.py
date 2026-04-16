import pandas as pd
from IPython.display import display,HTML
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
#print(ROOT_DIR)


#=========================================================================================
#READ CSV AND SAVE CSV FUNCSTIONS:

def load_data(rel_path, encoding_type="utf-8"):
    file_path = ROOT_DIR / rel_path
    return pd.read_csv(file_path,encoding = encoding_type, keep_default_na=False)


def create_csv(df,filename):
    rel_path = 'data/processed/'
    file_path = ROOT_DIR / rel_path / filename
    file_path.parent.mkdir(parents = True, exist_ok=True)
    try:
        df.to_csv(file_path, index=False, na_rep="")
        print(f"File saved: {file_path}")
    except PermissionError:
        print(f"The file {filename} is opened by another app, close it and try again")



#=========================================================================================
#PRINT/DISPLAY - CUSTOMIZED        
#HTML Titles and paragraph
# NOTE: Custom style may not display in some notebooks enviroments
# but output ( titles, text, dataframes...) will still be displayed with default styling

h1_color = "#6c37f4"
h2_color = "#8a00cf"
p_color = "#979797"

def print_title(t):
    display(HTML(f"""
                    <style>                        
                        h1 {{color:{h1_color}; font-family:Arial; font-size: 40px; font-weight:normal;margin-top: 26px; margin-bottom: 12px;}}
                    </style>
                    <h1> {t} </h1>
                """))


def print_subtitle(st):
    display(HTML(f"""
                    <style>                        
                        h2 {{color:{h2_color}; font-family:Arial; font-size: 28px; font-weight:bold; margin-top: 0; margin-bottom: 0;padding-bottom: 0;}}
                    </style>
                    <h2> {st} </h2>
                """))
    

def print_text(text):
    display(HTML(f"""
                    <style>                        
                        p {{color:{p_color}; font-family:Arial; font-size: 28px; font-weight:bold; margin-top: 0; margin-bottom: 0;padding-bottom: 0;}}
                    </style>
                    <p>{text}</p>
                """))



# "fix" the problem that one element's tuples have a final commas... -just for aesthetic display. it doesnt change the dataframe value/format
def format_tuple(x):
    return "('"+str(x[0])+"')" if (len(x)==1 and isinstance(x, tuple) ) else x

tuple_cols = ['where_drink','additions', 'brew','purchase','dairy','sweetener','why_drink']
formatters = {col: format_tuple for col in tuple_cols}


# TEMP custom HTML display
# TODO improve display formatting options
def show_df(obj, head=None, tail=None):
    """Display a DataFrame with enhanced visual formatting"""
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
    
    df_preview = df_preview.drop_duplicates()
    
    df_html = df_preview.to_html(index=True, formatters=formatters)
    df_html = df_html.replace('class="dataframe"', 'class="df_table"')

    html = f"""
    <style>
        .df_table {{
            border-collapse: collapse;
            width: max-content;
            max-width: 100%;
            table-layout: auto;
            border: 0px solid #27B0FF !important;
            color: black;
        }}

        .df_table th, .df_table td {{
            font-size: 12px;
            border: 1px solid #FFFFFF !important;
            padding: 6px 8px;
            text-align: left;
            border: 1px solid #0084FF !important;
            white-space: nowrap;
        }}

        .df_table thead th {{
            background-color: #58AEFF !important;
            position: sticky;
            top: 0;
        }}

        tbody tr:nth-child(even) td, th {{
            background-color: #DEDEDE !important;
        }}

        tbody tr:nth-child(odd) td, th {{
            background-color: #C2C0C0 !important;
        }}

        tbody th.row_heading.level1 {{
            background-color: #F54927 !important;
            vertical-align: top;
            font-weight: 600;
            
        }}
        tbody th[rowspan] {{
            background-color: white;
            vertical-align: top;
        }}
    </style>

    <div style="overflow-x:auto; max-width:100%;">
        {df_html}
    </div>
    """
    #print(html)

    display(HTML(html))



# TEMP custom HTML display
# TODO improve display formatting options
def create_html_table(df,df_notes,width,font_size, tclass='summary'):
    # NOTE: Custom style may not display in some notebooks enviroments
    # but output ( titles, text, dataframes...) will still be displayed with default styling
    df_html = df.to_html(index=True, formatters=formatters)
    df_html = df_html.replace('class="dataframe"', f'class="{tclass}"')
    html = f"""
    <style>
        .{tclass} {{
            border-collapse: separate;
            border-radius: 10px !important;
            width: {width};
            max-width: 100%;
            table-layout: auto;
            border: 4px solid #853cc4 !important;
            color: black;
            overflow: hidden;       
        }}

        .{tclass} th, .{tclass} td {{
            font-size: {font_size};
            padding: 6px 8px;
            text-align: left;
            border: 1px solid #B454DA !important;
            white-space: nowrap;
        }}

        .{tclass} thead th {{
            background-color: #C7C7C7 !important;
            position: sticky;
            top: 0;
        }}

        tbody tr:nth-child(even) td, th {{
            background-color: #DEDEDE !important;
        }}

        tbody tr:nth-child(odd) td, th {{
            background-color: #C2C0C0 !important;
        }}

        tbody th.row_heading.level1 {{
            background-color: #F54927 !important;
            vertical-align: top;
            font-weight: 600;
            
        }}
        tbody th[rowspan] {{
            background-color: white;
            vertical-align: top;
        }}

    </style>

    <div style="overflow-x:auto; max-width:100%;">
        <div style="margin-top:6px; font-size:10px; color:gray;">
            {df_notes}
        </div>
        {df_html}

    </div>
    """
    return html



# TEMP custom HTML display
# TODO improve display formatting options

def summary(obj, twidth="max-content",font_size="18px", show="return", notes=False):
    
    """Display a DataFrame with enlarged font size for small summary style dataframes tables """
    # NOTE: Custom style may not display in some notebooks enviroments
    # but output ( titles, text, dataframes...) will still be displayed with default styling

    if hasattr(obj, "to_frame"):
        df = obj.to_frame(name=obj.name or "value")
    else:
        df =obj
    df_notes = df.attrs.get('count', '') if notes else ""
        
    if show=="display":
        
        html_display = create_html_table(df,df_notes,"max-content",font_size,tclass="summary")
        #print(html_display)
        display(HTML(html_display))
    else:
        html_ret = create_html_table(df,df_notes,"100%","12px",tclass="summary_h")
        #print(html_ret)
        return HTML(html_ret)


# TEMP custom HTML display
# TODO improve display formatting options

def display_horizontal(*divs,titles=None):

    """Display multiple DataFrames side by side, for horizontal comparisson"""
    # NOTE: Custom style may not display in some notebooks enviroments
    # but output ( titles, text, dataframes...) will still be displayed with default styling

    html = '<div style="display: flex; gap:16px;">'

    for i, div in enumerate(divs):
        #div.data = (div.data).replace("width: max-content;","width: 100%;")
        #div.data = (div.data).replace("{TABLE_WIDTH}","100%")
        div.data = (div.data).replace("nowrap","normal")
        title=title[i] if titles else ""
        html+='<div style="flex:1; min-width:0;">'
        if title:
            html+=f'<h4>{title}</h4>'
        #print("DIV.data TYPE:",type(div.data))
        html+=div.data
        #print(div.data)
        html+='</div>'
        #print(html)
    html+='</div>'
    
    display(HTML(html))


#=========================================================================================