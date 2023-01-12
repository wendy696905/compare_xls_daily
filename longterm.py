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
src = r'file'
dst = r'file_folder'
name_list_src = r'changed_file_full_path'
name_list_dst = r'changed_file_dst_folder'

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
summary_file = r'summary_file_path'
df_summary = pd.read_excel(summary_file)
df_summary.drop(columns=df_summary.columns[0], axis=1, inplace=True)

#append the difference into summary table
df_summary = pd.concat([df_summary, df_diff])
df_summary['compare'] = df_summary['Description'] + df_summary['GDM No.']

df_summary.to_excel(r'summary_file_path',sheet_name='sheet1')





# In[ ]:





# In[ ]:




