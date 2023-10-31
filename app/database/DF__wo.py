from datetime import datetime
import pandas as pd
from . import impo


wo = impo.wo.merge( impo.woStatus,    how='left', on='Work Order Status ID')
wo = wo.merge( impo.contactID,   how='left', left_on='Created By Contact ID', right_on='Contact ID')
wo = wo.merge( impo.priorityID,  how='left', on='Priority ID')
wo = wo.merge( impo.departament, how='left', on='Department ID')
wo = wo.merge( impo.jobType,     how='left', on='Job Type ID')
wo = wo.merge( impo.pm,          how='left', on='Preventative Maintenance ID')
wo = wo.merge( impo.assets,      how='left', on='Asset ID')



wo['Raised Date Time'] = pd.to_datetime(wo['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['raisedYear']  = wo['Raised Date Time'].dt.year
wo['raisedMonth'] = wo['Raised Date Time'].dt.month
wo['raisedDay'] = wo['Raised Date Time'].dt.day

wo['Modified Date Time'] = pd.to_datetime(wo['Modified Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['closedYear']  = wo['Modified Date Time'].dt.year
wo['closedMonth'] = wo['Modified Date Time'].dt.month
wo['closedDay'] = wo['Modified Date Time'].dt.day



### 4. Упорядочивание столбцов и удаление NaN
wo = wo[['raisedYear', 'raisedMonth','raisedDay',  'closedYear', 'closedMonth', 'closedDay',  'Work Order Number', 'Work Order Description', 'Work Order ID',
          'Created By', 'Work Order Closed Contact ID', 'Work Order Status Description', 'Priority Description', 'Department Name', 'Department Description',
         'Job Type Description', 'Preventative Maintenance Number', 'Asset Description', 'Asset Number', 'Asset ID', 'Modified Date Time',]].fillna('undefined')



### 5. Дополнительные поля для фильтра Maintenance и RMPD
wo['Short Department Name'] = wo['Department Name'].copy().map(lambda x: x[:3] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)
wo['Discipline']  = wo['Department Name'].copy().map(lambda x: x.split('-')[1] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)

maintenance = ['Maintenance', 'Maintenance General', 'MECH (Static)', 'MECH (Rotating)', 'Instrumentation', 'Electrical']
wo['isMaintenance'] = wo['Department Description'].copy().map(lambda x: 'yes' if x in maintenance else 'no')

rmpd = ['SLU', 'SGU', 'PWU', 'U&O','Routine Maintenance Planning Department']
wo['isRMPD'] = wo['Short Department Name'].copy().map(lambda x: 'yes' if x in rmpd else 'no')
wo_RMPD        = wo.loc[ wo['isRMPD'] == 'yes' ]