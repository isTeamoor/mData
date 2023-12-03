from datetime import datetime
import pandas as pd
from .impo import wo, assets, isGrouppedWO, contactID



isGrouppedWO['Is Group Work Order'] = 'yes'

woNumbers = wo[['Work Order ID', 'Work Order Number']].copy()
woNumbers.rename(columns={'Work Order Number':'Group WO number'}, inplace=True)



wo = wo.merge( contactID,     how='left', left_on='Created By Contact ID', right_on='Contact ID')
wo = wo.merge( assets,        how='left', on='Asset ID')
wo = wo.merge( isGrouppedWO,  how='left',on='Work Order ID')
wo = wo.merge( woNumbers,     how='left', left_on='Group Work Order ID', right_on='Work Order ID', suffixes=(None,'to_delete'))




wo['Raised Date Time'] = pd.to_datetime(wo['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['raisedYear']  = wo['Raised Date Time'].dt.year
wo['raisedMonth'] = wo['Raised Date Time'].dt.month
wo['raisedDay'] = wo['Raised Date Time'].dt.day


wo['Closed Date Time'] = pd.to_datetime(wo['Closed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['closedYear']  = wo['Closed Date Time'].dt.year
wo['closedMonth'] = wo['Closed Date Time'].dt.month
wo['closedDay'] = wo['Closed Date Time'].dt.day




wo = wo[['raisedYear', 'raisedMonth','raisedDay', 'Closed Date Time', 'closedYear', 'closedMonth', 'closedDay',  'Work Order Number', 'Work Order Description', 
         'Created By', 'Work Order Status Description', 'Priority Description', 'Department Name', 'Department Description', 'Work Order ID',
         'Job Type Description', 'Asset Description', 'Asset Number', 'Asset ID', 'Group WO number','Is Group Work Order']].fillna('undefined')



### 5. Дополнительные поля для фильтра Maintenance и RMPD
wo['Short Department Name'] = wo['Department Name'].copy().map(lambda x: x[:3] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)
wo['Discipline']  = wo['Department Name'].copy().map(lambda x: x.split('-')[1] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)

maintenance = ['Maintenance', 'Maintenance General', 'MECH (Static)', 'MECH (Rotating)', 'Instrumentation', 'Electrical']
wo['isMaintenance'] = wo['Department Description'].copy().map(lambda x: 'yes' if x in maintenance else 'no')

rmpd = ['SLU', 'SGU', 'PWU', 'U&O','Routine Maintenance Planning Department']
wo['isRMPD'] = wo['Short Department Name'].copy().map(lambda x: 'yes' if x in rmpd else 'no')
wo_RMPD        = wo.loc[ wo['isRMPD'] == 'yes' ]