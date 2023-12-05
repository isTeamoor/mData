from .impo import spares, customFields, uom
from .DF__wo import wo
from .DF__woComponent import woComponent
from .DF__reservations import reservations


spares = spares.merge(reservations, on='Work Order Spare ID',     how='left')
spares = spares.merge(woComponent,  on='Work Order Component ID', how='left')
spares = spares.merge(wo,           on='Work Order ID',           how='left')
spares = spares.merge(customFields, on='Work Order Spare ID',     how='left')
spares = spares.merge(uom,          on='UOMID',                   how='left')


### 2. Форматирование пустых значений
spares.loc[spares['Account Code'].isnull(), ['Account Code Description']] = 'Not Assigned'
spares.loc[spares['Account Code'].isnull(), ['Account Code']] = '99999999999'

spares[['reservMonth', 'reservYear', 'Reservation Number']] = spares[['reservMonth', 'reservYear', 'Reservation Number']].fillna(0)
spares['Group WO number'] = spares['Group WO number'].fillna('undefined')



### 3. Удаление spares, для которых reservation не назначен, но WO уже закрыт или отменен
unused = spares.loc[(spares['Reservation Number'] == 0) 
                   & (spares['Group WO number']=='undefined')
                   & ((spares['Work Order Status Description'] == 'Closed') | (spares['Work Order Status Description'] == 'Cancelled'))]
spares = spares.drop(unused.index)




spares.insert(1, 'Actual Cost', spares['Actual Quantity'] * spares['Estimated Unit Cost'])
spares.insert(1, 'Estimated Cost', spares['Estimated Quantity'] * spares['Estimated Unit Cost'])
spares.loc [spares['Account Code']=='100000000012', 'Short Department Name'] = '4AP'




### 6. Фильтрованные dataFrames
spares_maintenance = spares.loc[ spares['isMaintenance'] == 'yes' ]
spares_RMPD        = spares.loc[ spares['isRMPD'] == 'yes' ]
