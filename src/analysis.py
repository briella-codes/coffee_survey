#"EDA" RELATED FUNCTIONS:
#Record count by group. (Optional: you can group using subgroups(more than one column name), if you use the parameter columns that is type "*args"


def group_and_count(df, *columns):
    lst = list(columns)  
    #print(lst)
    df_copy =df.copy()
    for col in lst: 
        if df[col].map (lambda x: isinstance(x, tuple)).any():
            #detect if any of that columns is multivalue "type" -multivalues columns'elements were converted to list in preprocessing step
            #if simple value no need to explode, else if it's true... explode:
            df_copy = df_copy.explode(col)
    
    return df_copy.groupby(lst, observed=True).size().rename('count')



def calculate_percentage_by_group(df,group,group_title=None,sort=None):
    total_records = df[group].count()

    #si quiero con Nuls incluidos:
    #df_pct = df.groupby(group).size()
    df_pct = df.copy()
        
    if df[group].map (lambda x: isinstance(x, tuple)).any():
            #detect if any of that columns is multivalue "type" -multivalues columns'elements were converted to list in preprocessing step
            #if simple value no need to explode, else if it's true... explode:
            df_pct = df_pct.explode(group)

    
    #print("columns :",df_pct.columns)
    df_pct = df_pct.groupby(group).size().reset_index(name='count')
    df_pct['pct'] = ((df_pct['count']*100 ) /total_records ).round(1)
    
    if sort=="asc":
        df_pct = df_pct.sort_values( by ='pct',ascending=True)
    elif sort=="desc":
        df_pct = df_pct.sort_values( by ='pct',ascending=False)
    df_pct['pct'] = df_pct['pct'].astype(str)+"%"

    #df_pct= df_pct.to_frame()
    #df_pct= df_pct.reset_index()
    df_pct.index =range(len(df_pct))
    if group_title is None:
        group_title = group
    df_pct.columns = [group_title, 'count','%'] 
    #I summ +1 to index number for visual in percentage ranking:
    df_pct.index = df_pct.index + 1
    
    df_pct.attrs['count'] = "TOTAL Respondents of "+str(group_title)+":" +str(total_records)+" non-NA records"
    df_pct.attrs['note_multiple_sel'] = "For this question multiple selection was allowed . Each percentage represents the real proportion of \n consumers who selected each option , so the total sum of porcentages may exced 100%"
    df_pct.attrs['note_count'] = "Record count doesn't include NA values"
    
    return df_pct