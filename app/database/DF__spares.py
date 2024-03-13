from .impo import spares, customFields, uom
from .DF__wo import wo
from .DF__woComponent import woComponent
from .DF__reservations import reservations




spares = spares.merge(reservations, on='Work Order Spare ID',     how='left')
spares = spares.merge(woComponent,  on='Work Order Component ID', how='left')
spares = spares.merge(wo,           on='Work Order ID',           how='left')
spares = spares.merge(customFields, on='Work Order Spare ID',     how='left')
spares = spares.merge(uom,          on='UOMID',                   how='left')



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

spares.loc [ (spares['Account Code']=='100000000012') & (spares['Reserved By']=="To'lqin Berdiyev Omonovich"), 'Short Department Name'] = '4AP'


### Exception 
spares.loc[ (spares['Work Order Number']==85413) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==84124) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 1.866
spares.loc[ (spares['Work Order Number']==86345) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==82418) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==85463) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==85465) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==83927) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.933
spares.loc[ (spares['Work Order Number']==80700) & (spares['Work Order Spare Description']=='Аргон газообразный'), 'Estimated Quantity' ] = 1.866
spares.loc[ (spares['Work Order Number']==85424) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 3.732
spares.loc[ (spares['Work Order Number']==86510) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 1.866
spares.loc[ (spares['Work Order Number']==86773) & (spares['Work Order Spare Description']=='Аргон газ особой чистоты 6.0 ТУ 2114-003-37924839-2016 (99,9999%)'), 'Estimated Quantity' ] = 0.472


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
