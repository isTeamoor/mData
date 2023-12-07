from .impo import trades, tradeCodes
from .DF__wo import wo
from .DF__woComponent import woComponent




trades = trades.merge(wo,          on='Work Order ID',           how='left')
trades = trades.merge(tradeCodes,  on='Trade Code ID',           how='left')
trades = trades.merge(woComponent, on='Work Order Component ID', how='left')



trades.fillna({
    'Account Code':'undefined', 'Account Code Description':'undefined',
}, inplace=True)



### Удаление trades, для которых actual не назначен, но WO уже закрыт или отменен
unused = trades.loc[(trades['Actual Duration Hours'] == 0) 
                    & ((trades['Work Order Status Description'] == 'Closed') | (trades['Work Order Status Description'] == 'Cancelled'))]
trades = trades.drop(unused.index)



trades['Actual Cost']    = trades['Actual Duration Hours'] * trades['Hourly Rate']
trades['Estimated Cost'] = trades['Estimated Duration Hours'] * trades['Hourly Rate']


trades = trades[[
'Work Order ID', 'Trade Code Description', 
'Estimated Duration Hours', 'Actual Duration Hours','Hourly Rate', 'Estimated Cost', 'Actual Cost', 
'Work Order Number','Work Order Status Description','raisedYear', 'raisedMonth',
'Work Order Component Description', 'Job Code Major Description', 'Account Code', 'Account Code Description', 
'closedYear', 'closedMonth', 'Priority Description', 'Department Name',
'Short Department Name', 'isMaintenance', 'isRMPD',
'Department Description', 'Job Type Description', 'Created By',
'Asset Description', 'Asset Number', 'Asset ID', 'Parent Asset ID',
'WO Account Code Name', 'WO Account Code Description',
'Work Order Description',
]]
