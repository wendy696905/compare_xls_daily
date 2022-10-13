#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import pandas as pd
import numpy as np
from itertools import chain
import shutil
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date

#change the file name as date
src = r'//edc.micron.com/twn/FAB030/GDMS/GDMS_dashboard/longterm_action/daily_data/longterm.csv'
dst = r'//edc.micron.com/twn/FAB030/GDMS/GDMS_dashboard/longterm_action/daily_data'
name_list_src = r'//edc.micron.com/twn/FAB030/GDMS/OMT Area Scorecard/Name list/Name_List_for_Area_Scorecard_data.csv'
name_list_dst = r'https://edc.micron.com/twn/FAB030/GDMS/GDMS_dashboard/SharePoint_Excel_New'

folder_time = datetime.now().strftime('%Y%m%d')
dst1 = dst + '\longterm_action_' + folder_time + '.csv'


file = shutil.copy(src,dst1)

#copy name list file to GDM dashboard data source folder
name_list = shutil.copy(name_list_src, name_list_dst)

df = pd.read_csv(file)

df = df[['Action Owner', 'Action Owner Area',  'Area GRP**_by action owner', 'Area GRP**_by case owner', 'Caselink', 'Completed Date', 'Description', 'Deviation Owner', 'Fab', 'GDM No.', 'GDM type', 'Major Deviation Detected', 'Owner Area', 'Planned Date', 'Requested time category', 'Status_']

#read previous date excel
previous_date = date.today() - timedelta(days = 1)
previous_date = previous_date.strftime('%Y%m%d')

previous_file = dst + '\longterm_action_' + previous_date + '.csv'
previous_df = pd.read_csv(previous_file)
previous_df = previous_df['Action Owner', 'Action Owner Area',  'Area GRP**_by action owner', 'Area GRP**_by case owner', 'Caselink', 'Completed Date', 'Description', 'Deviation Owner', 'Fab', 'GDM No.', 'GDM type', 'Major Deviation Detected', 'Owner Area', 'Planned Date', 'Requested time category', 'Status_']
                            
#compare and find the difference of two dataframe
df_all = df.merge(previous_df.drop_duplicates(),how='left', indicator='indicator')
df_diff = df_all[df_all['indicator'] == 'left_only']

#Append date check and WW into dataframe

df_diff['Extension date'] = date.today()
'''
today = date.today() + timedelta(days = 3)
df_diff['Extension WW'] = today.isocalendar()[1]
'''
#read summary table file
summary_file = r'//edc.micron.com/twn/FAB030/GDMS/GDMS_dashboard/longterm_action/longterm_action_extend_summary.xlsx'
df_summary = pd.read_excel(summary_file)
df_summary.drop(columns=df_summary.columns[0], axis=1, inplace=True)

#append the difference into summary table
df_summary = pd.concat([df_summary, df_diff])
df_summary['compare'] = df_summary['Description'] + df_summary['GDM No.']

df_summary.to_excel(r'C:\Users\wendysu\OneDrive - Micron Technology, Inc\GDM\GDM_dashboard\longterm_action_extend_summary.xlsx',sheet_name='sheet1')





# In[ ]:





# In[ ]:




