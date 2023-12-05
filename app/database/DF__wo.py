import pandas as pd
from .impo import wo, priority, departments, jobType, status, isMasterWO, closedDates, contactID, assets, accountCodes



wo = wo.merge(priority,     how='left', on='Priority ID')
wo = wo.merge(departments,  how='left', on='Department ID')
wo = wo.merge(jobType,      how='left', on='Job Type ID')
wo = wo.merge(status,       how='left', on='Work Order Status ID')
wo = wo.merge(assets,       how='left', on='Asset ID')



contactID = contactID[['Contact ID', 'Created By']]
wo = wo.merge(contactID,    how='left', left_on='Created By Contact ID', right_on='Contact ID')



wo = wo.merge(accountCodes, how='left', on='Account Code ID')
wo.rename(columns={'Account Code Name':'WO Account Code Name', 'Account Code Description':'WO Account Code Description'}, inplace=True)



isMasterWO['Is Master Work Order'] = 'yes'
wo = wo.merge(isMasterWO,   how='left', on='Work Order ID')



woNumbers = wo[['Work Order ID', 'Work Order Number']].copy()
woNumbers.rename(columns={'Work Order Number':'Group WO number'}, inplace=True)
wo = wo.merge( woNumbers, how='left', left_on='Group Work Order ID', right_on='Work Order ID', suffixes=(None,'to_delete'))



closedDates['Closed Date Time'] = pd.to_datetime(closedDates['Closed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
closedDates = closedDates.sort_values(by='Closed Date Time', ascending=False)
closedDates = closedDates.drop_duplicates(subset='Work Order ID', keep='first')
closedDates['closedYear']  = closedDates['Closed Date Time'].dt.year
closedDates['closedMonth'] = closedDates['Closed Date Time'].dt.month
closedDates['closedDay'] = closedDates['Closed Date Time'].dt.day
wo = wo.merge( closedDates, how='left', on='Work Order ID' )
wo[['closedYear', 'closedMonth', 'closedDay']] = wo[['closedYear', 'closedMonth', 'closedDay']].fillna(0)



wo['Raised Date Time'] = pd.to_datetime(wo['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['raisedYear']  = wo['Raised Date Time'].dt.year
wo['raisedMonth'] = wo['Raised Date Time'].dt.month
wo['raisedDay'] = wo['Raised Date Time'].dt.day



wo = wo[['raisedYear', 'raisedMonth', 'closedYear', 'closedMonth', 'Work Order Number', 'Work Order Description', 
         'Created By', 'Work Order Status Description', 'Priority Description', 'Department Name', 'Department Description', 'Work Order ID',
         'Job Type Description', 'Asset Description', 'Asset Number', 'Asset ID', 'Group WO number','Is Master Work Order','WO Account Code Name','WO Account Code Description']].fillna('undefined')



wo['Short Department Name'] = wo['Department Name'].copy().map(lambda x: x[:3] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)
wo['Discipline']  = wo['Department Name'].copy().map(lambda x: x.split('-')[1] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)

maintenance = ['Maintenance', 'Maintenance General', 'MECH (Static)', 'MECH (Rotating)', 'Instrumentation', 'Electrical']
wo['isMaintenance'] = wo['Department Description'].copy().map(lambda x: 'yes' if x in maintenance else 'no')

rmpd = ['SLU', 'SGU', 'PWU', 'U&O','Routine Maintenance Planning Department']
wo['isRMPD'] = wo['Short Department Name'].copy().map(lambda x: 'yes' if x in rmpd else 'no')
wo_RMPD = wo.loc[ wo['isRMPD'] == 'yes' ]