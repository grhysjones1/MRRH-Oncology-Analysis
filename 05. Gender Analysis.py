#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:02:56 2018

@author: garethjones
"""

''' Imports & Global Variables '''
import pandas as pd
import matplotlib.pyplot as plt

''' CALCULATIONS '''

''' Calculate overall gender split '''
gender_c = data[['Gender']].groupby(['Gender']).size().to_frame('Total')
gender_c['Percent'] = gender_c.Total/gender_c.Total.sum()*100
gender_p = gender_c.drop(['Total'],axis=1)
gender_p.columns = ['Total']
gender_p = gender_p.transpose()
gender_p.columns = ['Female %','Male %']

''' Calculate gender split of big cancers '''
gender_cancer_c = data[['Gender','Cancer_Type']].groupby(['Cancer_Type','Gender']).size().to_frame('Total').reset_index()
p_gender_cancer_c = gender_cancer_c.pivot_table(index='Cancer_Type',columns='Gender',values='Total',aggfunc=sum,margins=True,margins_name='Total',fill_value=0)
p_gender_cancer_cother = p_gender_cancer_c[p_gender_cancer_c.index.isin(['Total'])] - p_gender_cancer_c[p_gender_cancer_c.index.isin(bigcancers)].sum()
p_gender_cancer_cother.rename(index={'Total':'Others'}, inplace=True)
p_gender_cancer_c = p_gender_cancer_c[p_gender_cancer_c.index.isin(bigcancers)]
p_gender_cancer_c = p_gender_cancer_c.append(p_gender_cancer_cother)
p_gender_cancer_c['Male %'] = p_gender_cancer_c['Male']/p_gender_cancer_c['Total']*100
p_gender_cancer_c['Female %'] = p_gender_cancer_c['Female']/p_gender_cancer_c['Total']*100
p_gender_cancer_p = p_gender_cancer_c.drop(['Male','Female','Total'],axis=1)

''' Append both dataframes together '''
p_gender_cancer_p = gender_p.append(p_gender_cancer_p)


''' PLOTTING '''

ax = p_gender_cancer_p.plot(kind='bar',stacked=True,color=['#F0C8D4','#94BED1'],width=0.55,legend=False)
patches = ax.patches 

labels = []
for j in p_gender_cancer_p.columns:
    for i in p_gender_cancer_p.index:
        label = p_gender_cancer_p.loc[i][j]
        labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels]

for label,rect in zip(labels,patches):
    w = rect.get_width()
    h = rect.get_height()
    x = rect.get_x()
    y = rect.get_y()
    c = rect.get_fc()
    if h > 0:
        if c[0]>0.25 and c[1]>0.25 and c[2]>0.25:
            plt.text(x+w/2,y+h/2,label,ha='center',va='center',color='black',fontsize=8)
        else:
            plt.text(x+w/2,y+h/2,label,ha='center',va='center',color='white',fontsize=8)


plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.gca().set_ylim([0,100])
plt.xticks(rotation=45,ha='right',va='top',rotation_mode="anchor",fontsize=10,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tick_params(left=False,bottom=False,labelleft=False)
ax.set_xlabel('Year',visible=False)
plt.title('Percentage of Genders by Cancer Type Across All Years',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
plt.savefig(directory+'Charts/% of Genders by Cancer Type All Years.png',bbox_inches='tight',dpi=1000)


plt.show()
del gender_c,gender_cancer_c,gender_p,h,i,j,w,x,y,label,labels,p_gender_cancer_c,patches,c






