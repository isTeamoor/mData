import pandas as pd
from .impo import requests, priorityAnswer, priorityAnswerDescription
from .impo import priority, departments, jobType, contactID, assets, woNumbers

requests = requests.loc[requests['Cancelled Date Time'].isna()]

requests = requests.merge(priorityAnswer, left_on='Request ID', right_on='Entity ID', how='left')
requests = requests.merge(priorityAnswerDescription, on='Priority Matrix Answer ID', how='left')
requests = requests.merge(priority,     how='left', on='Priority ID')
requests = requests.merge(departments,  how='left', on='Department ID')
requests = requests.merge(jobType,      how='left', on='Job Type ID')
requests = requests.merge(assets,       how='left', on='Asset ID')
requests = requests.merge(contactID[['Contact ID', 'Requested By']], how='left', left_on='Requested By Contact ID', right_on='Contact ID')
requests = requests.merge(woNumbers[['Work Order ID', 'Work Order Number']], how='left', on='Work Order ID')

requests['Requested Date Time'] = pd.to_datetime(requests['Requested Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requests['requestYear']  = requests['Requested Date Time'].dt.year
requests['requestMonth'] = requests['Requested Date Time'].dt.month

requests['Completed Date Time'] = pd.to_datetime(requests['Completed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requests['completeYear']  = requests['Completed Date Time'].dt.year
requests['completeMonth'] = requests['Completed Date Time'].dt.month


requests = requests[[
'Request Number','Requested By','Department Name','Department Description', 'Request Description','Requester Detail','Response', 
'Priority Description',
'Priority Matrix Safety Description', 'Priority Matrix Repair Cost Description','Priority Matrix Production Description','Priority Matrix Environmental Description',
'Safety Risk Score','Repair Cost Risk Score','Production Risk Score','Environmental Risk Score',
'Job Type Description','Asset Description', 'Asset Number',
'Estimated Cost','Work Order Number','requestYear', 'requestMonth', 'completeYear','completeMonth'
]]