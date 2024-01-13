import pandas as pd
from .impo import wo, priority, departments, jobType, status, isMasterWO, closedDates, contactID, assets, accountCodes, isMasterWO, woNumbers




wo = wo.merge(priority,     how='left', on='Priority ID')
wo = wo.merge(departments,  how='left', on='Department ID')
wo = wo.merge(jobType,      how='left', on='Job Type ID')
wo = wo.merge(status,       how='left', on='Work Order Status ID')
wo = wo.merge(assets,       how='left', on='Asset ID')
wo = wo.merge(isMasterWO,   how='left', on='Work Order ID')
wo = wo.merge(closedDates,  how='left', on='Work Order ID' )
wo = wo.merge(accountCodes, how='left', on='Account Code ID')
wo = wo.merge(contactID[['Contact ID', 'Created By']], how='left', left_on='Created By Contact ID', right_on='Contact ID')
wo = wo.merge(woNumbers[['Work Order ID', 'Group WO number']], how='left', left_on='Group Work Order ID', right_on='Work Order ID', suffixes=(None,'to_delete'))




wo['Raised Date Time'] = pd.to_datetime(wo['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
wo['raisedYear']  = wo['Raised Date Time'].dt.year
wo['raisedMonth'] = wo['Raised Date Time'].dt.month

wo['closedYear']  = wo['Closed Date Time'].dt.year
wo['closedMonth'] = wo['Closed Date Time'].dt.month





wo.rename(columns={'Account Code Name':'WO Account Code Name', 'Account Code Description':'WO Account Code Description'}, inplace=True)

wo.fillna({
    'closedYear':0, 'closedMonth':0, 'closedDay':0,'Group WO number':0,'raisedYear':0, 'raisedMonth':0,
    'Work Order Description':'undefined', 'Created By':'undefined', 'Work Order Status Description':'undefined', 
    'Priority Description':'undefined', 'Department Name':'undefined', 'Department Description':'undefined',
    'Job Type Description':'undefined', 'Asset Description':'undefined', 'Asset Number':'undefined', 'Asset ID':'undefined', 
    'Is Master Work Order':'undefined','WO Account Code Name':'undefined','WO Account Code Description':'undefined'
}, inplace=True)





wo['Short Department Name'] = wo['Department Name'].copy().map(lambda x: x[:3] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)
wo['Discipline']  = wo['Department Name'].copy().map(lambda x: x.split('-')[1] if x.startswith(('SLU', 'SGU', 'PWU', 'U&O')) else x)



maintenance = ['Maintenance', 'Maintenance General', 'MECH (Static)', 'MECH (Rotating)', 'Instrumentation', 'Electrical']
rmpd        = ['SLU', 'SGU', 'PWU', 'U&O','Routine Maintenance Planning Department']

wo['isMaintenance'] = wo['Department Description'].copy().map(lambda x: 'yes' if x in maintenance else 'no')
wo['isRMPD'] = wo['Short Department Name'].copy().map(lambda x: 'yes' if x in rmpd else 'no')



wo = wo[['Work Order ID', 'Work Order Number', 'Work Order Status Description','raisedYear', 'raisedMonth','closedYear', 'closedMonth',
        'Priority Description','Department Name','Short Department Name','Discipline','isMaintenance', 'isRMPD', 'Department Description', 'Job Type Description','Created By',
        'Asset Description','Asset Number', 'Asset ID', 'Parent Asset ID',
        'Is Master Work Order', 'Is Group Work Order', 'Group WO number', 
        'WO Account Code Name','WO Account Code Description','Work Order Description',]]