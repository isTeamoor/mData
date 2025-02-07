from .impo import trades, tradeCodes, contactID
from .DF__wo import wo
from .DF__woComponent import woComponent




trades = trades.merge(wo,          on='Work Order ID',           how='left')
trades = trades.merge(tradeCodes,  on='Trade Code ID',           how='left')
trades = trades.merge(woComponent, on='Work Order Component ID', how='left')

trades = trades.merge(contactID[['Contact ID', 'Trade Name']], how = 'left', left_on = 'Trade Contact ID', right_on = 'Contact ID')




trades.fillna({
    'Account Code':'undefined', 'Account Code Description':'undefined',
}, inplace=True)



### Удаление trades, для которых actual не назначен, но WO уже закрыт или отменен
unused = trades.loc[(trades['Actual Duration Hours'] == 0) 
                    & ((trades['Work Order Status Description'] == 'Closed') | (trades['Work Order Status Description'] == 'Cancelled'))]
trades = trades.drop(unused.index)



trades['Actual Cost']    = trades['Actual Duration Hours'] * trades['Hourly Rate']
trades['Estimated Cost'] = trades['Estimated Duration Hours'] * trades['Hourly Rate']

cofe_trades = ['WELDER','INSULATE','Scaffolder','PIPING JUNIOR','Metrology Engineer','HVAC ENG','JET TECH','SUPV PSV','Fire and Gas engineer','WELD ENG','Field instrumentation Junior technician','Valve technician','Workshop machinist junior','F&G Supervisor','HVAC Supervisor','Piping Engineer','Work Shop machinist']
trades['isCofETrade'] = trades['Trade Code Description'].copy().map(lambda x: 'yes' if x in cofe_trades else 'no')


trades = trades[[
'Work Order ID', 'Trade Code Description', 'Trade Name','isCofETrade',
'Estimated Duration Hours', 'Actual Duration Hours','Hourly Rate', 'Estimated Cost', 'Actual Cost', 
'Work Order Number','Is Master Work Order','Work Order Status Description','raisedYear', 'raisedMonth',
'Work Order Component Description', 'Job Code Major Description', 'Account Code', 'Account Code Description', 
'closedYear', 'closedMonth', 'Priority Description', 'Department Name',
'Short Department Name', 'isMaintenance', 'isRMPD',
'Department Description', 'Job Type Description', 'Created By',
'Asset Description', 'Asset Number', 'Asset ID', 'Parent Asset ID',
'WO Account Code Name', 'WO Account Code Description',
'Work Order Description',
]]
