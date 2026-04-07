#=========================================================================================
#GRAPHICS/CHARTS RELATED FUNCTIONS


def missing_values_bar_chart(ax,missing_df):
    missing_df=missing_df.sort_values("missing", ascending=True)
    missing_count = missing_df["missing"]
    col =missing_df.index
    perc =  missing_df["percentage"].astype(int).astype(str)+'%'
    barras = ax.barh(col,missing_count, height=0.8)
    ax.bar_label(barras,labels=perc,padding=2)
    ax.set_xlabel('Missing values record count')
    ax.set_ylabel('Items')    
    #ax.set_title("MISSING VALUES BAR CHART")