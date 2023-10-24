from ..database.DF__spares import spares_maintenance as spares
from ..database.DF__trades import trades_maintenance as trades
from ..database.DF__budget import budget, months



plan_Monthly = []
actual_Monthly = []
actual_Spares_Monthly = []
actual_Trades_Monthly = []

plan_Cumulat = []
actual_Cumulat = []
actual_Spares_Cumulat = []
actual_Trades_Cumulat = []




summary = 0
for month in months:
    plan_Monthly.append(budget[month].sum())
    summary += budget[month].sum()
    plan_Cumulat.append(summary)

summary = 0
arr = spares.loc [ (spares['reservYear'] == 2023), 'reservMonth' ].unique()
for i in range(1,13):
    if i in arr:
        val = spares.loc [ (spares['reservYear'] == 2023) & (spares['reservMonth'] == i), 'Actual Cost' ].sum()
        actual_Spares_Monthly.append(val)
        summary += val
        actual_Spares_Cumulat.append(summary)
    else:
        actual_Spares_Monthly.append(0)
        actual_Spares_Cumulat.append(0)




summary = 0
arr = trades.loc [ (trades['Work Order Status Description'] == 'Closed') 
                 & (trades['raisedYear'] == 2023), 'closedMonth' ].unique()
for i in range(1,13):
    if i in arr:
        val = trades.loc [ (trades['Work Order Status Description'] == 'Closed') 
                         & (trades['raisedYear'] == 2023)
                         & (trades['closedMonth'] == i), 'Actual Cost' ].sum()
        actual_Trades_Monthly.append(val)
        summary += val
        actual_Trades_Cumulat.append(summary)
    else:
        actual_Trades_Monthly.append(0)
        actual_Trades_Cumulat.append(0)




for i in range(0,12):
    actual_Monthly.append(actual_Spares_Monthly[i] + actual_Trades_Monthly[i])
    actual_Cumulat.append(actual_Spares_Cumulat[i] + actual_Trades_Cumulat[i])


forecast_Spares = spares.loc [ (spares['raisedYear'] == 2023) & (spares['reservYear'] == 0), 'Estimated Cost' ].sum()
forecast_Trades = trades.loc [ (trades['raisedYear'] == 2023) & (trades['Work Order Status Description'] != 'Closed'), 'Estimated Cost' ].sum()
forecast = forecast_Spares + forecast_Trades


