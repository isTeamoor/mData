from . import impo
from .DF__reservations import reservations
from .DF__wo import wo


### 1. Импорт загруженных данных 
spares       = impo.spares



### 2. Объединение dataFrames
spares = spares.merge(reservations, on='Work Order Spare ID',     how='left')
spares = spares.merge(wo,           on='Work Order ID',           how='left')



### 3. Форматирование пустых значений
spares.rename(columns={'Account Code Name': 'Account Code'}, inplace=True)
spares.loc[spares['Account Code'].isnull(), ['Account Code Description']] = 'Not Assigned'
spares.loc[spares['Account Code'].isnull(), ['Account Code']] = '99999999999'
spares[['reservMonth', 'reservYear', 'Reservation Number']] = spares[['reservMonth', 'reservYear', 'Reservation Number']].fillna(0)
spares['Group WO number'] = spares['Group WO number'].fillna('undefined')



### 4. Удаление spares, для которых reservation не назначен, но WO уже закрыт или отменен
unused = spares.loc[(spares['Reservation Number'] == 0) 
                   & (spares['Group WO number']=='undefined')
                   & ((spares['Work Order Status Description'] == 'Closed') | (spares['Work Order Status Description'] == 'Cancelled'))]
spares = spares.drop(unused.index)



### 5. Добавление столбцов, вычисляющих прогнозную и фактическую стоимость
spares.insert(1, 'Actual Cost', spares['Actual Quantity'] * spares['Estimated Unit Cost'])
spares.insert(1, 'Estimated Cost', spares['Estimated Quantity'] * spares['Estimated Unit Cost'])



### 6. Фильтрованные dataFrames
spares_maintenance = spares.loc[ spares['isMaintenance'] == 'yes' ]
spares_RMPD        = spares.loc[ spares['isRMPD'] == 'yes' ]
