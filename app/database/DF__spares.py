from .impo import spares, customFields, uom, assetIDcatalogID, catalogueInfo
from .DF__wo import wo
from .DF__woComponent import woComponent
from .DF__reservations import reservations
from .DF__assets import unitChildren


spares = spares.merge(reservations, on='Work Order Spare ID',     how='left')
spares = spares.merge(woComponent,  on='Work Order Component ID', how='left')
spares = spares.merge(wo,           on='Work Order ID',           how='left')
spares = spares.merge(customFields, on='Work Order Spare ID',     how='left')
spares = spares.merge(uom,          on='UOMID',                   how='left', suffixes=('', 'delete'))






spares.fillna({
    'Account Code':'undefined', 'Account Code Description':'undefined',
    'reservMonth':0, 'reservYear':0, 'Reservation Number':0,
    'Group WO number':0,
}, inplace=True)




### Удаление spares, для которых reservation не назначен, но WO уже закрыт или отменен
unused = spares.loc[(spares['Reservation Number'].isna()) 
                   & (spares['Spares Comment'].isna())
                   & ((spares['Work Order Status Description'] == 'Closed') | (spares['Work Order Status Description'] == 'Cancelled'))]
spares = spares.drop(unused.index)



spares['Actual Cost']    = spares['Actual Quantity'] * spares['Estimated Unit Cost']
spares['Estimated Cost'] = spares['Estimated Quantity'] * spares['Estimated Unit Cost']




### Reservations for Air Products
spares.loc [ (spares['Account Code']=='100000000012') & (spares['Reserved By']=="To'lqin Berdiyev Omonovich"), 'Short Department Name'] = '4AP'
spares.loc [ (spares['Asset Number']).isin(unitChildren()) & (spares['Short Department Name']!='4AP'), 'Short Department Name' ] = '4AP'




spares = spares[[
'Work Order Spare ID', 'Work Order ID', 'Work Order Spare Description', 'Reservation Number', 'reservYear', 'reservMonth', 'Reserved By', 'isRMPD_planner',
'Estimated Quantity', 'Actual Quantity','UOMDescription','Estimated Unit Cost', 'Estimated Cost', 'Actual Cost', 
'Work Order Number','Work Order Status Description','raisedYear', 'raisedMonth',
'Work Order Component Description', 'Job Code Major Description', 'Account Code', 'Account Code Description', 
'closedYear', 'closedMonth', 'Priority Description', 'Department Name',
'Short Department Name', 'isMaintenance', 'isRMPD', 'Discipline',
'Department Description', 'Job Type Description', 'Created By',
'Asset Description', 'Asset Number', 'Asset ID', 'Parent Asset ID',
'Is Master Work Order', 'Is Group Work Order', 'Group WO number','Spares Comment',
'WO Account Code Name', 'WO Account Code Description',
'Work Order Description', 'Employee WOSpares', 
]]
#'Material Code',

