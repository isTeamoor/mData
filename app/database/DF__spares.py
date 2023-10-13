from . import impo
from .DF__reservations import reservations
from .DF__wo import wo


### 1. Импорт загруженных данных 
spares       = impo.spares
woComponent  = impo.woComponent
accountCodes = impo.accountCodes
jobCodes     = impo.jobCodes
uom          = impo.uom



### 2. Объединение dataFrames
spares = spares.merge(reservations, on='Work Order Spare ID',     how='left')
spares = spares.merge(wo,           on='Work Order ID',           how='left')
spares = spares.merge(woComponent,  on='Work Order Component ID', how='left')
spares = spares.merge(accountCodes, on='Account Code ID',         how='left')
spares = spares.merge(jobCodes,     on='Job Code Major ID',       how='left')
spares = spares.merge(uom,          on='UOMID',                   how='left')



### 3. Форматирование пустых значений
spares.rename(columns={'Account Code Name': 'Account Code'}, inplace=True)
spares.loc[spares['Account Code'].isnull(), ['Account Code Description']] = 'Not Assigned'
spares.loc[spares['Account Code'].isnull(), ['Account Code']] = '99999999999'
spares[['reservMonth', 'reservYear', 'Reservation Number']] = spares[['reservMonth', 'reservYear', 'Reservation Number']].fillna(0)



### 4. Удаление spares, для которых reservation не назначен, но WO уже закрыт или отменен
unused = spares.loc[(spares['Reservation Number'] == 0) & ((spares['Work Order Status Description'] == 'Closed') | (spares['Work Order Status Description'] == 'Cancelled'))]
spares = spares.drop(unused.index)



### 5. Добавление столбцов, вычисляющих прогнозную и фактическую стоимость
spares.insert(1, 'Actual Cost', spares['Actual Quantity'] * spares['Estimated Unit Cost'])
spares.insert(1, 'Estimated Cost', spares['Estimated Quantity'] * spares['Estimated Unit Cost'])



### 6. Фильтрованные dataFrames
spares_maintenance = spares.loc[ spares['isMaintenance'] == 'yes' ]
spares_RMPD        = spares.loc[ spares['isRMPD'] == 'yes' ]

