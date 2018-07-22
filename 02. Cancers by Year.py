#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 11:35:18 2018

@author: garethjones
"""

''' Imports '''
from matplotlib.ticker import PercentFormatter,MultipleLocator,FormatStrFormatter
import matplotlib.font_manager



''' CALCULATIONS '''

''' Count Cancer N All Years '''
cancer_count = pd.Series(data['Cancer_Type'].value_counts())
cancer_count = cancer_count[1:len(cancer_count)].append(cancer_count[0:1])
cancer_perc = cancer_count/cancer_count.sum()*100
cancer_perc = ["{:.0f}%".format(item) for item in cancer_perc]

''' Count Cancer N by Year '''    
canceryr_count = data[['Appt_Year','Cancer_Type']].groupby(['Appt_Year','Cancer_Type']).size().to_frame('Total').reset_index()
p_canceryr_c = canceryr_count.pivot_table(index='Appt_Year',columns='Cancer_Type',values='Total',aggfunc=sum,margins=True,margins_name='Total',fill_value=0)
sumothercancers = p_canceryr_c.drop(bigcancers,axis=1)
sumothercancers = sumothercancers.drop('Total',axis=1)
sumothercancers = sumothercancers.sum(axis=1)
sumothercancers = pd.Series(sumothercancers,name='Others')
p_canceryr_c2 = pd.concat([p_canceryr_c[bigcancers],sumothercancers,p_canceryr_c[['Total']]],axis=1)

''' Count Cancer % by Year '''   
p_canceryr_p = p_canceryr_c.divide(p_canceryr_c['Total'],axis=0).round(decimals=3)*100
sumothercancers_per = p_canceryr_p.drop(bigcancers,axis=1)
sumothercancers_per = sumothercancers_per.drop('Total',axis=1)
sumothercancers_per = sumothercancers_per.sum(axis=1)
sumothercancers_per = pd.Series(sumothercancers_per,name='Others')
p_canceryr_p2 = pd.concat([p_canceryr_p[bigcancers],sumothercancers_per,p_canceryr_p[['Total']]],axis=1)

''' Cancer by Month '''
monthyr_count = data[['Appt_Year','Appt_Month']].groupby(['Appt_Year','Appt_Month']).size().to_frame('Total').reset_index()
monthyr_count = monthyr_count.replace({'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'})



''' PLOTTING '''


''' Plot Total Cancers '''
# plot chart
ax = cancer_count.plot(kind='bar',color=palette10[0])

# create annotation of summed total
xaxis = np.arange(len(cancer_count.index))
for i,j in zip(xaxis,cancer_count):
    ax.text(i,cancer_count[i]+10,j,ha='center',fontsize=8)

for i,j in zip(xaxis,cancer_perc):
    ax.text(i,cancer_count[i]+30,j,ha='center',fontsize=8)

# format chart
plt.xticks(rotation=45,ha='right',va='top',rotation_mode='anchor',fontsize=8,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.title('Total Patients by Cancer Across All Years',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
plt.tick_params(left=False,labelleft=False)
plt.savefig(directory+'Charts/Total Patients by Cancer All Years.png',bbox_inches='tight',dpi=1000)
plt.show()


''' Plot Cancer N by Year '''
# create variables needed and plot graph
total = p_canceryr_c2['Total']
xaxis = [0,1,2,3,4]
p_canceryr_c2 = p_canceryr_c2.drop('Total',axis=1)
p_canceryr_c2 = p_canceryr_c2.drop('Total')
ax = p_canceryr_c2.plot(kind='bar',stacked=True,color=palette10)

# create annotation of summed total
for i,j in zip(xaxis,total):
    ax.text(i,total[i]+10,j,ha='center',fontsize=8)
  
# format chart
plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.xticks(rotation=0,fontsize=10,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xlabel('')
plt.ylabel('Patients',fontsize=10,weight='bold')
plt.title('Total Patients by Cancer 2013-17',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
plt.tick_params(bottom=False)
plt.savefig(directory+'Charts/Total Patients by Cancer 2013-17.png',bbox_inches='tight',dpi=1000)
plt.show()


''' Plot Cancer % by Year '''
# create variables needed and plot chart
p_canceryr_p2 = p_canceryr_p2.drop('Total',axis=1)
p_canceryr_p2 = p_canceryr_p2.drop('Total')
ax = p_canceryr_p2.plot(kind='bar',stacked=True,color=palette10)
#plt.style.use('gj')
patches = ax.patches
labels = []

# create labels list of percentages
for j in p_canceryr_p2.columns:
    for i in p_canceryr_p2.index:
        label = p_canceryr_p2.loc[i][j]
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

     
# format chart and save to directory
plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.gca().set_ylim([0,100])
plt.xticks(rotation=0,fontsize=10,weight='bold')
plt.xlabel('')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.tick_params(left=False,bottom=False,labelleft=False)
plt.title('Percentage of Patients by Cancer 2013-17',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
ax.yaxis.set_major_formatter(PercentFormatter()) 
plt.savefig(directory+'Charts/% of Patients by Cancer 2013-17.png',bbox_inches='tight',dpi=1000)


''' Plot Appts by Month '''
ax = monthyr_count.plot(kind='line',color=palette10)

# set minor and major x ticks
# I don't know why, but when using mutliple locator to space the ticks, it starts at index 1 instead of 0
# therefore I'm having to reset the indices of years and months
years = ['x','2013','2014','2015','2016','2017']
a = pd.Series([0])
b = monthyr_count.Appt_Month
months = a.append(b)
ax.xaxis.set_major_locator(MultipleLocator(12))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.set_xticklabels(years,minor=False,fontsize=10,weight='bold')
ax.set_xticklabels(months,minor=True,rotation=90,va='top',fontsize=11)
# remove x ticks every 3
for index, label in enumerate(ax.xaxis.get_ticklabels(which='minor')):
    if index % 3 != 0:
        label.set_visible(False)
        
# format
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
ax.legend_.remove()
plt.margins(x=0) # removes margin on x axis so graph starts at 0
ax.tick_params(which='major',axis='x',length=30,color='#AD2E32')
ax.tick_params(which='minor',axis='x',length=4)
ax.tick_params(axis='y',labelsize=10)
ax.grid(which='minor',linewidth=.3)
ax.grid(which='major',linewidth=.7)
plt.title('Total Patients by Month 2013-17',fontsize=12,weight='bold')
ax.title.set_position([.5, 1.05]) 
plt.ylabel('Patients',fontsize=12,labelpad=10,weight='bold')
plt.savefig(directory+'Charts/Total Patients by Month 2013-17.png',bbox_inches='tight',dpi=1000)


plt.show()
del sumothercancers,sumothercancers_per,canceryr_count,a,b,months,years,height,i,index,j,labels,patches,p_canceryr_c2,p_canceryr_p2,total,width,x,xaxis,y,c




'''
p_canceryr_c.loc['Total'] = p_canceryr_c.sum() # adds column totals
rowsum = pd.Series(p_canceryr_c.sum(axis=1),name='Total') # create series of row totals
p_canceryr_c = pd.concat([p_canceryr_c,rowsum],axis=1) # concat row series to dataframe
'''



