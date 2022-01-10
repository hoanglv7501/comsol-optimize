from os import path
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector, RectangleSelector
from matplotlib.path import Path 
from matplotlib.patches import Rectangle
# from SpanSelector import onselect

from preprocess import getData,dataGenerate

import pandas as pd



while True:
    try:
        csv_file=input("Path to the data file (.csv): ")
        rough=getData(csv_file)
        print(rough[:5])
        print(rough.iloc[-5:])
        conv=input("Convert rad2deg or deg2rag?: ")
        if conv=="rad2deg": rough=getData(csv_file,'rad2deg')
        elif conv=="deg2rad": rough=getData(csv_file,'deg2rad')
        elif conv=='no' or conv=='No': rough=getData(csv_file)
        else: print("Type 'rad2deg' or 'deg2rad' or 'No'!")
        break
    except:
        print("File error! Try again")

step=int(input("New step of frequency?: "))
# rough=getData("rough.csv",'rad2deg')
smallerPart=int((rough.iloc[1][1]-rough.iloc[0][1])/step)
print(smallerPart)
sct=dataGenerate(rough,smallerPart=smallerPart)

a=list(rough)[0]
f=list(rough)[1]
R=list(rough)[-1]

lista=pd.unique(rough[a])
listf=pd.unique(rough[f])
x,y=np.meshgrid(lista,listf)
Z=np.array(rough[R]).reshape(len(lista),len(listf)).T
ind=[]
sInd=[]
tempInd=[]

def onselect(verts):
    global ind,sInd
    path=Path(verts)
    sInd=np.nonzero(path.contains_points(pts.get_offsets()))[0]
    for i in sInd:
        if i not in ind: ind.append(i)

def mouse_click(event):
    global ind
    if str(event.button)=="MouseButton.MIDDLE":
        ind=[]
        # ax.vlines=[]
        # rec=RectangleSelector(ax,onselect=onselect, button=[1])
        print("Selection Cleared")
        
fig, ax=plt.subplots()
fig.suptitle("Select multiple areas that need to re-sweep\n Press middle mouse to reset, close window for next angle",
                 fontsize=10)
pts=ax.scatter(sct[a],sct[f])
cont=ax.contourf(x,y,Z,512,cmap='plasma')
plt.colorbar(cont)

line={'color':'green','linewidth':2, 'alpha':1}
lss=LassoSelector(ax, onselect=onselect, lineprops=line)

fig.canvas.mpl_connect('button_press_event',mouse_click)
plt.show()

print(ind)
for i in ind:
    print(sct.iloc[i][0],end=" ")
for i in ind:
    print(sct.iloc[i][1],end=" ")
    