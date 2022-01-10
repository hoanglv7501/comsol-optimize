from numpy.lib.function_base import angle
import pandas as pd
import numpy as np
import math
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Div, ColumnDataSource
# def getData(csv_file):
#     Data=pd.read_csv(csv_file)
#     Data=Data.iloc[5:,]
#     return Data
# print(getData("alpha1 - Copy.csv"))

import csv
def getData(csv_file,convert_angle=None,decimals=None):
    with open(csv_file,'r') as roughData, open(csv_file.strip(".csv")+"_Copy.csv",'w+') as newData:
        wr=csv.writer(newData)
        data_in_list=[]
        for row in roughData:
            data_in_list.append(row)
        # print(data_in_list[1][0])
        for i in range(len(data_in_list)):
            if data_in_list[i][0].isdigit():
                newData.write(data_in_list[i-1])
        newData.write(data_in_list[-1])
    data=pd.read_csv(csv_file.strip(".csv")+"_Copy.csv")
    if convert_angle=='rad2deg': data.iloc[:,0]=np.round(data.iloc[:,0]*180/math.pi,3)
    elif convert_angle=='deg2rad': data.iloc[:,0]=np.round(data.iloc[:,0]*math.pi/180,3)

    if decimals!=None: 
        for i in range(np.shape(data)[1]-1):
            data.iloc[:,i]=np.round(data.iloc[:,i],decimals)
    return data



def Transform2D(Data):
    a=list(Data)[0]
    f=list(Data)[-2]
    R=list(Data)[-1]
    list_a=[]
    for alpha in Data[a].values:
        if alpha not in list_a:
            list_a.append(alpha)
    list_f=[]
    for freq in Data[f].values:
        if freq not in list_f:
            list_f.append(freq)
    Data2D=np.zeros((len(list_a),len(list_f)))
    for i in range(len(list_a)):
        for j in range(len(list_f)):
            Data2D[i,j]=Data[(Data[a]==list_a[i])&(Data[f]==list_f[j])][R].values[0]
    return Data2D
    
def dataGenerate(dataFrame,smallerPart,angle_unit="rad",decimals=5):
    a=list(dataFrame)[0]
    f=list(dataFrame)[-2]
    R=list(dataFrame)[-1]
    list_a=[]
    for alpha in dataFrame[a].values:
        if alpha not in list_a:
            list_a.append(alpha)
    list_f=[]
    for freq in dataFrame[f].values:
        if freq not in list_f:
            list_f.append(freq)
     
    stepF=(list_f[1]-list_f[0])/smallerPart
     
    newData=pd.DataFrame()
     
    for alpha in list_a:
        
        for freq in list_f:
            TotalR=dataFrame[(dataFrame[a]==alpha)&(dataFrame[f]==freq)][R].values[0]
            for i in range(smallerPart-1):
                newData=newData.append(pd.DataFrame({a:[alpha],f:[np.round(freq+(i+1)*stepF,decimals)],R:[TotalR]}))
    return newData


def drawSurface(csv_file,smallerPart,angle_unit='rad',decimals=5,output='html'):
    df1=getData(csv_file,'deg',decimals=decimals)
    df=dataGenerate(df1,smallerPart=smallerPart,decimals=decimals)
    Data=Transform2D(df)

    a=list(df)[0]
    f=list(df)[-2]
    R=list(df)[-1]

    list_a=pd.unique(df1[a])
    list_f=pd.unique(df1[f])
    
    if output=='ipynb' : output_notebook()
    s1=ColumnDataSource(data=dict(x=df[a],y=df[f]))
    p=figure(tools="lasso_select,box_select")
    p.circle('x','y',source=s1, fill_color="red",fill_alpha=0.2)
    p.image(image=[Data.T], x=0, y=np.amin(df[f]), dw=np.amax(df[a]), dh=np.amax(df[f])-np.amin(df[f]), palette='Magma256', level="image")
    p.grid.grid_line_width = 0.1


    s2=ColumnDataSource(data=dict(x=[],y=[]))
    div=Div(width=p.width, height=20000)
    p2=figure()
    p2.circle('x','y',source=s2, fill_color="red")

    s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1,s2=s2,div=div), code="""
            const inds=cb_obj.indices;
            const d1 = s1.data;
            const d2 = s2.data;
            d2['x'] = []
            d2['y'] = []
            for (let i = 0; i < inds.length; i++) {
                d2['x'].push(d1['x'][inds[i]])
                d2['y'].push(d1['y'][inds[i]])
                
            }
            div.text=[d2['x'].join(" "), d2['y'].join(" "),inds.length].join("\\n")
                            """)
    )


    layout=column(p,div)
    show(layout)
    