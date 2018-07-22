#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:41:43 2018

@author: garethjones
"""

''' Imports & Global Variables '''


''' CALCULATIONS '''

# Select Other Cancers Columns and Format
othercancers = data.Other_Cancer_Type.dropna()
othercancers = othercancers.str.upper()
total = othercancers.count()

# Select Cancer Strings to Search
cancerlist = ['CARCINOMA','LYMPHOMA','SARCOMA','WILM','CML','AML','LEUKEMIA','MYELOMA']

# Search for strings in dataset and sum into single column
cancerflags = pd.DataFrame()
for i in cancerlist:
    a = othercancers.str.contains(i).astype('int').to_frame(i)
    cancerflags = pd.concat([cancerflags,a],axis=1)
    
totalothercancers = cancerflags.sum()
totalothercancers = totalothercancers.rename('Total')

# Replace indices as necessary, add remainder
totalothercancers = pd.DataFrame(totalothercancers).reset_index()
totalothercancers.columns = ['Cancer','Total']
totalothercancers = totalothercancers.replace('AML','LEUKEMIA')
totalothercancers = totalothercancers.replace('CML','LEUKEMIA')
totalothercancers = totalothercancers.groupby('Cancer').sum().sort_values('Total',ascending=False)

# Format table into percentages
totalothercancersp = (totalothercancers/total*100)
remainder = pd.DataFrame([100-totalothercancersp.Total.sum()],columns=['Total']).rename(index={0:'OTHERS'})
totalothercancersp = totalothercancersp.append(remainder)
totalothercancersp.index = totalothercancersp.index.str.lower().str.title()


''' PLOTTING '''
totalothercancersp = totalothercancersp.transpose()
ax = totalothercancersp.plot(kind='bar',stacked=True,color=palette10,width=0.035) 
patches = ax.patches

labels=[]
# create labels list of percentages
for j in totalothercancersp.columns:
    for i in totalothercancersp.index:
        label = totalothercancersp.loc[i][j]
        labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels] #formats to 0 dp and adds %

# assign labels to patches on chart
for label, rect in zip(labels,patches):
    width = rect.get_width()
    height = rect.get_height()
    if height > 4: 
        x = rect.get_x()
        y = rect.get_y()
        c = rect.get_fc()
        if c[0]>0.25 and c[1]>0.25 and c[2]>0.25:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='black',fontsize=8)
        else:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='white',fontsize=8)

# create annotations of district names against graph
for label,rect in zip(totalothercancersp.columns,patches):
    x = rect.get_x()
    y = rect.get_y()
    height = rect.get_height()
    width = rect.get_width()
    plt.annotate("", xy=(x+width,y+height/2),xytext=(0.04,y+height/2),arrowprops=dict(arrowstyle="-"))
    plt.annotate(label,xy=(0.04,y+height/2),xytext=(0.04,y+height/2),ha='left',va='center',fontsize=10)

# format
plt.tick_params(left=False,bottom=False,labelleft=False,labelbottom=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
ax.legend_.remove()
plt.savefig(directory+'Charts/% of Other Cancer Types.png',bbox_inches='tight',dpi=1000)

plt.show()
del a,cancerflags,cancerlist,i,othercancers,total,remainder,totalothercancers,x,y,label,labels,j,c,height,patches,width







