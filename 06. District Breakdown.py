#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:15:48 2018

@author: garethjones
"""

''' Imports & Global Variables '''
import matplotlib.pyplot as plt
percentlimit = 5

''' Reformat district names '''
rename_dict = {'Bundubugyo':'Bundibujo',
               'Kibale':'Kabale',
               'Kabalole':'Kabarole',
                'Kyegegya':'Kyegegwa',
                'Kyejerwa':'Kyerwa',
                'Mbarra':'Mbarara',
                'Mitoma':'Mitooma',
                'Ruburizi':'Rubirizi',
                np.nan:'Unknown'}
district_list = data['District'].str.lower().str.title()
district_list = district_list.replace(rename_dict)


''' CALCULATIONS '''

''' Sum total district numbers '''
district_list_sum = len(district_list)
district_list_count = district_list.value_counts(dropna=False).sort_values(ascending=False).rename('Total')
district_list_per = ((district_list_count / district_list_sum)*100).round(decimals=2).rename('Percent')
districts = pd.concat([district_list_count,district_list_per],axis=1)

''' Get List of small districts '''
smalldistricts = districts['Percent'] < percentlimit
smalldistricts = districts[smalldistricts]
smalldistricts = smalldistricts.index.tolist()

''' Sum together small districts '''
smalldistricts_sum = districts[districts.Percent < percentlimit].sum().rename('Others')
districts = districts.drop(districts[districts.Percent < percentlimit].index)
districts = districts.append(smalldistricts_sum)

''' Reorder Unknown to bottom '''
unknown = districts.loc[['Unknown'],list(districts)]
districts = districts.drop(['Unknown'])
districts = districts.append(unknown)

''' Look at districts by Year '''
districtsyr = pd.concat([district_list,data['Appt_Year']],axis=1)
districtsyr_count = districtsyr.groupby(['Appt_Year','District']).size().to_frame('Total').reset_index()
p_districtsyr_c = districtsyr_count.pivot_table(index='Appt_Year',columns='District',values='Total',aggfunc=sum,margins=True,margins_name='Total',fill_value=0)
p_districtsyr_c = p_districtsyr_c.drop(smalldistricts,axis=1)
otherdistrictssum = (p_districtsyr_c.Total - p_districtsyr_c.drop(['Total'],axis=1).sum(axis=1)).rename('Others')#.to_frame('Others')
p_districtsyr_c = pd.concat([p_districtsyr_c,otherdistrictssum],axis=1)
colsorder = p_districtsyr_c.drop(['Total','Unknown','Others'],axis=1).sort_values('Total',axis=1,ascending=False).columns.tolist()
colsorder.extend(['Others','Unknown','Total'])
p_districtsyr_c = p_districtsyr_c[colsorder]
p_districtsyr_p = p_districtsyr_c.divide(p_districtsyr_c['Total'],axis=0).round(decimals=3)*100


''' PLOTTING  '''

'''Plot Districts %s for all years'''
# create variables / lists needed
labels = []
districtst = districts.transpose()

# plot horizontal stacked bar and get patches
ax = districtst.loc[['Percent']].plot(kind='barh',stacked=True,color=palette10,width=0.1,legend=False) # plot the horizontal bar chart with no formatting or labels yet
patches = ax.patches 

# create labels list of values to place on graph
for j in districtst.columns:
    label = districtst.loc['Percent'][j]
    labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels] #formats to 0 dp and adds %

# place each value label on the relevant patch of the graph
for label, rect in zip(labels, patches):  
    width = rect.get_width()  
    if width > 0:
        x = rect.get_x() 
        y = rect.get_y() 
        height = rect.get_height()
        c = rect.get_fc()
        if c[0]>0.25 and c[1]>0.25 and c[2]>0.25:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='black',fontsize=8)
        else:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='white',fontsize=8) 

# create annotations of district names against graph
for label,rect in zip(districtst.columns,patches):
    x = rect.get_x()
    y = rect.get_y()
    height = rect.get_height()
    width = rect.get_width()
    plt.annotate("", xy=(x+width/2,y+height),xytext=(x+width/2,0.10),arrowprops=dict(arrowstyle="-"))
    plt.annotate(label,xy=(x+width/2,0.10),xytext=(x+width/2,0.10),ha='left',va='bottom',rotation=45,rotation_mode="anchor",fontsize=10)

# format graph and save
plt.gca().set_xlim([0,100])
plt.axis('off')
plt.title('Percentage of Patients by District Across All Years',weight='bold',fontsize=12)
plt.savefig(directory+'Charts/% of Patients by District All Years.png',bbox_inches='tight',dpi=1000)


''' Plot district total by year '''
# get variables needed
totals = p_districtsyr_c.Total[:5].tolist()
p_districtsyr_c = p_districtsyr_c.drop('Total',axis=1)
p_districtsyr_c = p_districtsyr_c.drop('Total')

# plot graph
ax = p_districtsyr_c.plot(kind='bar',stacked=True,color=palette10)

# add totals to top of stacked bars
#xaxis = [0,1,2,3,4]
#for i,j in zip(xaxis,totals):
    #plt.text(i,j+8,totals[i],ha='center', va='bottom',fontsize=8)

# format graph and save
plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.xticks(rotation=0,fontsize=10,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tick_params(bottom=False)
plt.xlabel('')
plt.ylabel('Patients',weight='bold')
plt.title('Total Patients by District 2013-17',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
plt.savefig(directory+'Charts/Total Patients by District 2013-17.png',bbox_inches='tight',dpi=1000)


''' Plot district % by year '''
# get variables needed
labels = []
p_districtsyr_p = p_districtsyr_p.drop('Total',axis=1)
p_districtsyr_p = p_districtsyr_p.drop('Total')

# create labels list and reformat
for j in p_districtsyr_p.columns:
    for i in p_districtsyr_p.index:
        label = p_districtsyr_p.loc[i][j]
        labels.append(label)
labels = ["{:.0f}%".format(item) for item in labels] #formats to 0 dp and adds %

# plot graph and patches
ax = p_districtsyr_p.plot(kind='bar',stacked=True,color=palette10) 
patches = ax.patches 

# assign labels to patches on chart
for label, rect in zip(labels, patches): 
    width = rect.get_width()  
    height = rect.get_height()
    if height > 4: # only adds series label if the patch height is large enough
        x = rect.get_x() 
        y = rect.get_y() 
        c = rect.get_fc()
        if c[0]>0.25 and c[1]>0.25 and c[2]>0.25:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='black',fontsize=8)
        else:
            ax.text(x+width/2,y+height/2,label,ha='center',va='center',color='white',fontsize=8) 

# format graph and save
plt.legend(loc='upper left',bbox_to_anchor=(1.0, 1.045),fontsize=8,frameon=False)
plt.gca().set_ylim([0,100])
plt.xticks(rotation=0,fontsize=10,weight='bold')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tick_params(left=False,bottom=False,labelleft=False)
ax.set_xlabel('Year',visible=False)
plt.title('Percentage of Patients by District 2013-17',weight='bold',fontsize=12)
ax.title.set_position([.5, 1.05]) 
plt.savefig(directory+'Charts/% of Patients by District 2013-17.png',bbox_inches='tight',dpi=1000)

# show graphs and delete unnecessary variables
plt.show()
del i,j,x,y,width,district_list_count,district_list_per,district_list_sum,district_list,smalldistricts,unknown,rename_dict,percentlimit,colsorder,districtst,districtsyr,otherdistrictssum,smalldistricts_sum,label,labels,totals,height,districts,c#,xaxis



