import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

from preprocess import getData

import pandas as pd


while True:
    try:
        csv_file=input("Path to the data file (.csv): ")
        conv=input("Convert rad2deg or deg2rag?: ")
        if conv=="rad2deg": rough=getData(csv_file,'rad2deg')
        elif conv=="deg2rad": rough=getData(csv_file,'deg2rad')
        elif conv=='no' or conv=='No': rough=getData(csv_file)
        else: print("Type 'rad2deg' or 'deg2rad' or 'No'!")
        break
    except:
        print("File error! Try again")
# rough=getData("rough.csv")
step=int(input("New step of frequency?: "))

a=list(rough)[0]
f=list(rough)[1]
R=list(rough)[-1]

lista=pd.unique(rough[a])
listf=pd.unique(rough[f])

ind=[]
sInd=[]
tempInd=[]

def onselect(xmin, xmax):
    sInd=rough[(rough[a]==alpha)&(rough[f]>xmin)&(rough[f]<xmax)][f].values
    # ax.vlines([xmin, xmax], 0,1,linestyles='dashed',colors='red')
    
    try:
        tempInd.append(sInd[0])
        tempInd.append(sInd[-1])
    except:
        print('No range is choosen!')
        
def mouse_click(event):
    global tempInd,ax
    if str(event.button)=="MouseButton.MIDDLE":
        tempInd=[]
        # ax.vlines=[]
        # rec=RectangleSelector(ax,onselect=onselect, button=[1])
        print("Selection Cleared")


for alpha in lista[:3]:
    tempInd=[]
    
    fig, ax=plt.subplots()
    pts=ax.scatter(rough[rough[a]==alpha].values[:,1],rough[rough[a]==alpha].values[:,-1])
    line=ax.plot(rough[rough[a]==alpha].values[:,1],rough[rough[a]==alpha].values[:,-1])
    fig.suptitle("Select multiple areas that need to re-sweep\n Press middle mouse to reset, close window for next angle",
                 fontsize=10)
    plt.xlim(np.amin(rough[rough[a]==alpha][f].values),np.amax(rough[rough[a]==alpha][f].values))
    ax.set_ylim(np.amin(rough[rough[a]==alpha][R].values)*0.9,np.amax(rough[rough[a]==alpha][R].values)*1.1)
    plt.xlabel(f"{f}\n{R} at {a} = {alpha}")
    plt.ylabel(R)
    
    spn=SpanSelector(ax,onselect=onselect, button=[1],direction="horizontal")
    fig.canvas.mpl_connect('button_press_event',mouse_click)
    
    plt.show()
    ind.append(tempInd)

tempRange=[]    
finalFreq=[]
finalAlpha=[]
print(ind)

for i in range(len(ind)):
    tempRange.append([])
    for j in range(int(len(ind[i])/2)):
        
        tempRange[i].append(np.round(np.arange(ind[i][2*j],ind[i][2*j+1],step),4))
        for k in tempRange[i][j]:
            if k not in rough[rough[a]==lista[i]][f].values:
                finalFreq.append(k)
                finalAlpha.append(lista[i])
    

print(*finalAlpha)
print(*finalFreq)
print(len(finalFreq))