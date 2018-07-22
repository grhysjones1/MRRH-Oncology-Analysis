#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:30:59 2018

@author: garethjones
"""

''' Imports & Global Variables '''


''' CALCULATIONS '''

''' Calculate age buckets '''
data['Age_Bucket'] = data.Age.map(
    lambda x: '70+' if x > 70 
    else ('61-70' if x > 60 
    else ('51-60' if x > 50
    else ('41-50' if x > 40
    else ('31-40' if x > 30
    else ('21-30' if x > 20
    else '0-20'))))))

''' Calculate overall age split '''
total_ages = data[['Age_Bucket']].groupby(['Age_Bucket']).size().to_frame('Total')
total_ages['Percent'] = total_ages.Total/total_ages.Total.sum()*100
total_ages_p = total_ages.drop(['Total'],axis=1)
total_ages_p.columns = ['Total']
total_ages_p = total_ages_p.transpose()

''' Caclulate age split by cancers '''
age_cancer_c = data[['Age_Bucket','Cancer_Type']].groupby(['Cancer_Type','Age_Bucket']).size().to_frame('Total').reset_index()
p_age_cancer_c = age_cancer_c.pivot_table(index='Cancer_Type',columns='Age_Bucket',values='Total',aggfunc=sum,margins=True,margins_name='Total',fill_value=0)
p_age_cancer_cother = p_age_cancer_c[p_age_cancer_c.index.isin(['Total'])] - p_age_cancer_c[p_age_cancer_c.index.isin(bigcancers)].sum()
p_age_cancer_cother.rename(index={'Total':'Others'}, inplace=True)
p_age_cancer_c = p_age_cancer_c[p_age_cancer_c.index.isin(bigcancers)]
p_age_cancer_c = p_age_cancer_c.append(p_age_cancer_cother)

# convert to percentages
cols = p_age_cancer_c.columns.tolist()
for i in cols:
    p_age_cancer_c[i] = p_age_cancer_c[i]/p_age_cancer_c['Total']*100

# append datasets
p_age_cancer_p = total_ages_p.append(p_age_cancer_c).drop(['Total'],axis=1)


''' PLOTTING '''

''' Plot '''
ax = p_age_cancer_p.plot(kind='bar',stacked=True,color=palette10)
patches = ax.patches

labels = []
for j in p_age_cancer_p.columns:
    for i in p_age_cancer_p.index:
        label = p_age_cancer_p.loc[i][j]
        labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels]

for label,rect in zip(labels,patches):
    h = rect.get_height()
    w = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()
    c = rect.get_fc()
    if h > 4:
        if c[0]>0.25 and c[1]>0.25 and c[2]>0.25:
            ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=8,color='black')
        else:
            ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=8,color='white')

        
plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.gca().set_ylim([0,100])
plt.xticks(rotation=45,ha='right',va='top',rotation_mode="anchor",fontsize=10,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tick_params(left=False,bottom=False,labelleft=False)
ax.set_xlabel('Year',visible=False)
plt.title('Percentage of Age Groups by Cancer Type Across All Years',position=(0.5,1.05),fontsize=12,weight='bold')
ax.title.set_position([.5, 1.05]) 
plt.savefig(directory+'Charts/% of Age Groups by Cancer Type All Years.png',bbox_inches='tight',dpi=1000)

plt.show()
del h,i,j,label,labels,cols,total_ages,total_ages_p,w,x,y,patches,age_cancer_c,c,p_age_cancer_cother




