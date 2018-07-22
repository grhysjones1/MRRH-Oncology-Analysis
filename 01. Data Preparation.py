han#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:49:08 2018

@author: garethjones
"""

''' Import Dataset '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
directory = '/Users/garethjones/Documents/Data Analysis/MRRH Oncology Analysis/'
file1 = 'Data/Oncology Dataset.csv'
file2 = 'Data/Screening Dataset.csv'
origindata = pd.read_csv(directory+file1, encoding='utf-8')
screeningdata = pd.read_csv(directory+file2, encoding='ISO-8859-1')

''' Create Global Variables '''
bigcancers = ['Breast','KS','Prostate','Stomach','Esophagus']
palette10 = ['#094675','#AD2E32','#F6E8A5','#A2CFAB','#FCC46B','#E7F5F6','#F8C2CD','#C9CACB','#713F6E','#DBC757']
plt.rc('font',family='Calibri')

'''Select Relevant Columns'''
columns = ['enrol_d','gender','age','district','cancer','othercancertype','chemotype']
data = origindata[columns]

'''Rename Column Headers and Capitalize'''
data.columns = ['Appt_Date','Gender','Age','District','Cancer_Type','Other_Cancer_Type','Chemo_Type']
data.Cancer_Type = data.Cancer_Type.str.title()

''' Change date format and substring year/month info '''
data.loc[:,'Appt_Date'] = pd.to_datetime(data.loc[:,'Appt_Date'])
data = data.dropna(how='any',subset=['Appt_Date','Cancer_Type'])
data.Appt_Date = data.Appt_Date.apply(lambda x: x.strftime('%d%m%Y'))
appt_year = []
appt_month = []
for i in data.Appt_Date:
    appt_year.append(i[slice(4,8)])
    appt_month.append(i[slice(2,4)])
data['Appt_Year'] = appt_year
data['Appt_Month'] = appt_month

''' Remove irrelevant years '''
data = data[data['Appt_Year']!='2011']
data = data[data['Appt_Year']!='2012']
data = data[data['Appt_Year']!='2018']

''' Reorder Columns '''
data = data[['Appt_Date','Appt_Year','Appt_Month','Gender','Age','District','Cancer_Type','Other_Cancer_Type','Chemo_Type']]

''' Reformat cancer names '''
rename_dict = {'Ks':'KS',
               'Non_Hodgkins_Lymphoma':'Non Hodgkins Lymphoma',
               'Hodgkins_Lymphoma':'Hodgkins Lymphoma',
                'Headneck':'Head & Neck',
                'Rhaydomyo_Sarcoma':'Rhaydomyo Sarcoma',
                'Yolk_Sac':'Yolk Sac',
                'Castle_Mans':'Castle Mans',
                np.nan:'Unknown'}
data['Cancer_Type'] = data['Cancer_Type'].replace(rename_dict)

del columns,i,appt_year,appt_month,rename_dict

