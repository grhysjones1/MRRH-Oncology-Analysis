#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 16:04:23 2018

@author: garethjones
"""

''' Imports and globals '''
from matplotlib.ticker import PercentFormatter,MultipleLocator
upperbound = 80
lowerbound = 50


''' CALCULATIONS '''
cols  = origindata.columns.tolist()

nancount=[]
for i in cols:
    total = origindata[i].isnull().sum()
    nancount.append(total)
    
nancount = pd.DataFrame(nancount)
nancount.columns = ['N']
nancount.index = cols

nancount['Data Completeness'] = 1-nancount['N']/len(origindata.index)
nancount['Data Completeness'] = nancount['Data Completeness'].round(decimals=2)*100
nancount = nancount.drop('N',axis=1)
nancount = nancount.sort_values('Data Completeness',ascending=False)

filover75 = nancount[nancount['Data Completeness'] >=upperbound]
filover25 = nancount[(nancount['Data Completeness'] >=lowerbound) & (nancount['Data Completeness'] <upperbound)]
filover0 = nancount[(nancount['Data Completeness'] >0) & (nancount['Data Completeness'] <lowerbound)]
filequ0 = nancount[nancount['Data Completeness']==0].sort_index()

# find index point where value changes bucket
nancount['Bucket'] = np.where(nancount['Data Completeness']>=upperbound,1,
                    np.where(nancount['Data Completeness']>=lowerbound,2,
                    np.where(nancount['Data Completeness']>0,3,
                    np.where(nancount['Data Completeness']==0,4,0))))
breaks = nancount['Bucket'].diff()[nancount['Bucket'].diff()!=0].index.tolist()
breakids = []
for i in breaks:
    a = nancount.index.get_loc(i)
    breakids.append(a)
breakids.append(len(nancount)-1)

nancount = nancount.drop('Bucket',axis=1).reset_index()


''' PLOTTING '''
# create change in graph colours based on thresholds
colors = []
for i in nancount['Data Completeness']:
    if i >=upperbound:
        colors.append('#7dc18b')
    elif lowerbound <= i < upperbound:
        colors.append('#f9e47c')
    elif 0 < i < lowerbound:
        colors.append('#AD2E32')
    else:
        colors.append('black')

# plot graph
ax = nancount['Data Completeness'].plot(kind='bar',color=colors)
patches = ax.patches

# add dashed lines at each breakpoint
plt.annotate("", xy=(0,100),xytext=(0,107),
             arrowprops={'arrowstyle':'-','ls':'dashed','lw':0.8,'color':'grey'})
plt.annotate("", xy=(breakids[1],patches[breakids[1]-1].get_height()),xytext=(breakids[1],107),
             arrowprops={'arrowstyle':'-','ls':'dashed','lw':0.8,'color':'grey'})
plt.annotate("", xy=(breakids[2],patches[breakids[2]-1].get_height()),xytext=(breakids[2],107),
             arrowprops={'arrowstyle':'-','ls':'dashed','lw':0.8,'color':'grey'})
plt.annotate("", xy=(breakids[3],0),xytext=(breakids[3],107),
             arrowprops={'arrowstyle':'-','ls':'dashed','lw':0.8,'color':'grey'})
plt.annotate("", xy=(len(nancount.index)-1,0),xytext=(len(nancount.index)-1,107),
             arrowprops={'arrowstyle':'-','ls':'dashed','lw':0.8,'color':'grey'})

# create labels to add between dashed lines
labelpercs = nancount.index.tolist()
labelpercs = [(x+1)/len(labelpercs)*100 for x in labelpercs]
for i in range(0,4):
    if i == 0:
        x = labelpercs[breakids[i+1]]
        x = "{0:.0f}%".format(x)
        globals()['box%s' % i] = ax.text(breakids[i+1]/2,105,x,ha='center',va='center',color='black',fontsize=8,bbox={'boxstyle':'square','color':'w'})
    else:
        x = labelpercs[breakids[i+1]] - labelpercs[breakids[i]]
        x = "{0:.0f}%".format(x)
        globals()['box%s' % i] = ax.text((breakids[i+1]-breakids[i])/2+breakids[i],105,x,ha='center',va='center',color='black',fontsize=8,bbox={'boxstyle':'square','color':'w'})


# create arrows between labels
# w = box1.get_bbox_patch().get_width()   ----   understand why this defauts to 1 when running the code?

for i in range(0,4):
    x = globals()['box%s'%i].get_position()[0]
    y = globals()['box%s'%i].get_position()[1]
    width = globals()['box%s'%i].get_bbox_patch().get_width()
    plt.annotate("", xy=(breakids[i],y),xytext=(x-4,y),annotation_clip=False,arrowprops={'arrowstyle':'->','lw':0.8,'color':'grey'})
    plt.annotate("", xy=(breakids[i+1],y),xytext=(x+4,y),annotation_clip=False,arrowprops={'arrowstyle':'->','lw':0.8,'color':'grey'})


# format and save
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
ax.yaxis.set_major_formatter(PercentFormatter()) 
plt.gca().set_ylim([0,100])
# remove x ticks every 10
#for index, label in enumerate(ax.xaxis.get_ticklabels(which='major')):
  #  if index % 10 != 0:
    #    label.set_visible(False)
plt.margins(x=1) # removes margin on x axis so graph starts at 0
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1))
xticks=[0]
for i in list(range(0,len(nancount.index),10)):
    xticks.append(i)
ax.set_xticklabels(xticks,minor=False,fontsize=10)
plt.xlabel('Variable Index',labelpad=7,fontsize=10,weight='bold')
plt.ylabel('Completeness of Variable',labelpad=7,fontsize=10,weight='bold')
plt.title('Completeness of Variables in Dataset',fontsize=12,weight='bold')
ax.title.set_position([.5, 1.1]) 
plt.savefig(directory+'Charts/Completeness of Dataset Variables.png',bbox_inches='tight',dpi=1000)

plt.show()
del i

variables = pd.DataFrame(origindata.columns.tolist())
variables = variables.set_index(0)
variables.columns = ['Name']


