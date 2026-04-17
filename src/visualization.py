import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#COLOR PALETTES FOR CHARTS
PIE_PALETTE=["#d053d9","#B454DA","#ae63ff","#853cc4","#6c37f4","#3758de", "#0084FF", "#27B0FF","#00E9D9" ,"#00FFBB","#49E678","#72F45E","#AAE84D"]  
PIE_PALETTE2=["#d953c7","#8500dd","#ae63ff","#853cc4","#6c37f4","#3758de", "#0084FF", "#27B0FF","#00E9D9" ,"#00FFBB","#49E678","#72F45E","#AAE84D"]  

BICOLOR_BAR = ["#746AFF", "#AD41FF"]
HORIZ_BAR_GRADIENT = ["#fff292","#fff132","#fcca26","#ff9b21", "#FF5E00","#ff3216", "#C40000"]
HM_FIRE = ["#ffffff","#fbff00","#ffd000","#fc9300","#ff7700", "#FF6200", "#F20C00"]


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


def graphic_pie_chart(ax,column, title, angle=0, shape="pie", color=None):
    if color is None:
        color=PIE_PALETTE[:len(column.values)]
    if shape=="pie":
        wp ={"width":1}
    elif shape=="donut":
        wp ={"width":0.5}
    else:
        print("incorrect shape type")
   
    ax.pie(
    column.values,
    labels = column.index.to_list(),
    labeldistance=1.06,
    autopct = "%0.1f%%",
    pctdistance=0.66,
    startangle=angle,
    wedgeprops = wp,
    colors=color,
    textprops={'fontsize': 10}
    )
    ax.set_title(title, fontsize=17, fontweight='bold')
    
    return ax


def graphic_horizontal_bar_chart(ax,column, title, xy_labels=("","")):
    norm_values = column.values / column.values.max()
    color_cmap = LinearSegmentedColormap.from_list("hm_gradient", HORIZ_BAR_GRADIENT)
    colors_grad = [color_cmap(v) for v in norm_values]

    bars = ax.barh(
        column.index,
        column.values,
        height=0.8,
        color=colors_grad,
    )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.bar_label(bars, padding=5)
    ax.set_title(title, fontsize=17, fontweight='bold')
    ax.set_xlabel(xy_labels[0])
    ax.set_ylabel(xy_labels[1])

    pos = ax.get_position()  
    ax.set_position([pos.x0, pos.y0+0.2, pos.width, pos.height * 0.6])
    return ax


def grouped_bar_chart_fav_coffee_by_age(ax,fav_coffee_by_age_T):

    colors=["#56c700","#ae63ff","#006eff","#00dafc","#ff00b3", "#FF5E00", "#F20C00"]  

    #number of fav coffess types and cant de grupos etarios - age group = 1 age bar per fav coffee
    n_fav_types = len(fav_coffee_by_age_T.index)
    n_bars_age_groups = len(fav_coffee_by_age_T.columns)
    bar_width = 0.5
    space_btw_bars = 0.8
    #x=positions bases where starts each fav "bar group"
    x = np.arange(n_fav_types)  * (n_bars_age_groups* bar_width + space_btw_bars)

    # i= each age
    for i, age_group in enumerate(fav_coffee_by_age_T.columns):
        ax.bar(x + i*bar_width , fav_coffee_by_age_T[age_group],width=bar_width , label=age_group, color=colors[i])
    for j in range(n_fav_types):
        if j%2 == 0:
            ax.axvspan(
                #creo un sector como si fuese rectangulo por cada grupo para darle color de fondo
                x[j] - space_btw_bars/2,                           
                x[j] + bar_width * n_bars_age_groups + space_btw_bars/2,  
                color="#efefef",
                #alpha=0.3,    
                zorder=0      
        )

    #labels in position centered. x_center is array with all the center positions:
    x_center = x + bar_width * n_bars_age_groups / 2
    #ax.set_xticks(x_center)
    #ax.set_xticklabels(fav_coffee_by_age_T.index.tolist())
    ax.margins(x=0)
    ax.set_xticklabels([])

    for x_center,fav_label in zip(x_center, fav_coffee_by_age_T.index.tolist()):
        ax.text(
                x_center,
                0.12,                           
                fav_label,
                ha='center',
                va='bottom',               
                rotation=90,
                fontsize=12,
                fontweight='semibold',
                transform=ax.get_xaxis_transform(),
                clip_on=False
            )

    ax.set_title("Favorite Coffee by Age Group", fontsize=18, fontweight='bold')
    ax.legend(title="Age Groups", loc='upper center',frameon=False)
    return ax