from . import DF__wo
from . import impo


### 1. Импорт загруженных данных
trades       = impo.trades
woComponent  = impo.woComponent
accountCodes = impo.accountCodes
jobCodes     = impo.jobCodes
tradeID      = impo.tradeID



### 2. Объединение dataFrames
trades = trades.merge(DF__wo.wo,           on='Work Order ID',           how='left')
trades = trades.merge(woComponent,  on='Work Order Component ID', how='left')
trades = trades.merge(accountCodes, on='Account Code ID',         how='left')
trades = trades.merge(tradeID,      on='Trade Code ID',           how='left')
trades = trades.merge(jobCodes,     on='Job Code Major ID',       how='left')



### 3. Форматирование пустых значений
trades.rename(columns={'Account Code Name': 'Account Code'}, inplace=True)
trades.loc[trades['Account Code'].isnull(), ['Account Code Description']] = 'Not Assigned'
trades.loc[trades['Account Code'].isnull(), ['Account Code']] = '99999999999'



### 4. Удаление trades, для которых actual не назначен, но WO уже закрыт или отменен
unused = trades.loc[(trades['Actual Duration Hours'] == 0) & ((trades['Work Order Status Description'] == 'Closed') | (trades['Work Order Status Description'] == 'Cancelled'))]
trades = trades.drop(unused.index)



### 5. Добавление столбцов, вычисляющих прогнозную и фактическую стоимость
trades.insert(1, 'Actual Cost', trades['Actual Duration Hours'] * trades['Hourly Rate'])
trades.insert(1, 'Estimated Cost', trades['Estimated Duration Hours'] * trades['Hourly Rate'])



### 6. Фильтрованные dataFrames
trades_maintenance = trades.loc[ trades['isMaintenance'] == 'yes' ]
trades_RMPD        = trades.loc[ trades['isRMPD'] == 'yes' ]
