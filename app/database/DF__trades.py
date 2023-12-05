from .impo import trades, tradeCodes
from .DF__wo import wo
from .DF__woComponent import woComponent


### 1. Объединение dataFrames
trades = trades.merge(wo,          on='Work Order ID',           how='left')
trades = trades.merge(tradeCodes,  on='Trade Code ID',           how='left')
trades = trades.merge(woComponent, on='Work Order Component ID', how='left')


### 2. Форматирование пустых значений
trades.loc[trades['Account Code'].isnull(), ['Account Code Description']] = 'Not Assigned'
trades.loc[trades['Account Code'].isnull(), ['Account Code']] = '99999999999'



### 3. Удаление trades, для которых actual не назначен, но WO уже закрыт или отменен
unused = trades.loc[(trades['Actual Duration Hours'] == 0) & ((trades['Work Order Status Description'] == 'Closed') | (trades['Work Order Status Description'] == 'Cancelled'))]
trades = trades.drop(unused.index)



### 5. Добавление столбцов, вычисляющих прогнозную и фактическую стоимость
trades.insert(1, 'Actual Cost', trades['Actual Duration Hours'] * trades['Hourly Rate'])
trades.insert(1, 'Estimated Cost', trades['Estimated Duration Hours'] * trades['Hourly Rate'])



### 6. Фильтрованные dataFrames
trades_maintenance = trades.loc[ trades['isMaintenance'] == 'yes' ]
trades_RMPD        = trades.loc[ trades['isRMPD'] == 'yes' ]
