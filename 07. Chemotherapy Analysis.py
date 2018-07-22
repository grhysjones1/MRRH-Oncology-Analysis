#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 15:35:47 2018

@author: garethjones
"""

''' Imports & Global Variables '''
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


''' CALCULATIONS '''

chemodata = data.loc[(data.Cancer_Type.isin(bigcancers))]
chemodata.Chemo_Type = chemodata.Chemo_Type.fillna(0)
chemocount = chemodata[['Cancer_Type','Chemo_Type']].groupby(['Cancer_Type','Chemo_Type']).size().to_frame('Total').reset_index()
p_chemodata_c = chemocount.pivot_table(values='Total',index='Cancer_Type',columns='Chemo_Type',aggfunc=sum,margins=True,margins_name='Total',fill_value=0)
p_chemodata_p = p_chemodata_c.divide(p_chemodata_c['Total'],axis=0).round(decimals=3)*100

cols = p_chemodata_p.columns.tolist()
cols = cols[1:-1]
cols = ["{:.0f}".format(item) for item in cols] #formats to 0 dp and adds %
cols = ['No Data']+cols+['Total']
p_chemodata_p.columns = cols


''' PLOTTING '''

p_chemodata_p = p_chemodata_p.drop('Total',axis=1)
p_chemodata_p = p_chemodata_p.drop('Total',axis=0)

# Get length and width of data, set bar width
ind_len = np.arange(len(p_chemodata_p.index))
col_len = np.arange(len(p_chemodata_p.columns))
barwidth = 0.5

# Create dictionary with keys as column headers, and values as series of data points (to use on plot for loop)
cols = p_chemodata_p.columns.tolist()
dic = {}
for i in cols:
    dic[i] = p_chemodata_p[i]

# Set graph colours / fonts
colors = ['xkcd:light grey']
for i in col_len:
    colors.append(palette10[i])
plt.rc('font',family='Calibri')

# create labels list of percentages
labels = []
for j in p_chemodata_p.columns:
    for i in p_chemodata_p.index:
        label = p_chemodata_p.loc[i][j]
        labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels] #formats to 0 dp and adds %

# put labels list into a dictionary, 5 values at a time
labelsdic = {}
for i in col_len:
    labelsdic[i] = labels[i*5:i*5+5]

# Plot different stacked graphs on eachother 
base = ind_len*0
for i in col_len:
    globals()['ax%s' % i] = plt.bar(ind_len,dic[cols[i]],barwidth,bottom=base,color=colors[i])
    layer = p_chemodata_p.iloc[:,i]
    base = base + layer
    
    # for each set of stacked bars, assign slice of dictionary to patches
    patches = globals()['ax%s' % i].patches
    dicslice = labelsdic[i]
    for label,rect in zip(dicslice,patches):
        width = rect.get_width()
        height = rect.get_height()
        if height > 4: 
            x = rect.get_x()
            y = rect.get_y()
            color = rect.get_fc()
            if color[0]>0.25 and color[1]>0.25 and color[2]>0.25:
                plt.text(x+width/2,y+height/2,label,ha='center',
                         va='center',color='black',fontsize=8)
            else:
                plt.text(x+width/2,y+height/2,label,ha='center',
                         va='center',color='white',fontsize=8)

# Format chart
plt.gca().invert_yaxis()
plt.xticks(ind_len,p_chemodata_p.index,fontsize=10,weight='bold')
plt.legend((ax0,ax1,ax2,ax3,ax4,ax5,ax6,ax7),cols,loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False) # learn how to automate this 
plt.xlabel('')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.tick_params(left=False,bottom=False,labelleft=False)
plt.title('Percentage of Chemotherapy Use by Cancer Type',position=(0.5,1.05),fontsize=12,weight='bold')
plt.savefig(directory+'Charts/% of Chemotherapy Use by Cancer Type.png',bbox_inches='tight',dpi=1000)

plt.show()

for i in col_len:
    del globals()['ax%s' % i]
del barwidth,base,chemocount,chemodata,col_len,color,colors,cols,dic,dicslice,height,i,ind_len,j,label,labels,labelsdic,layer,patches,width,x,y

