from ..database.DF__budget import budget, months
from ..database.DF__wo import wo
from ..lib import gen

def Budget():
    output = {}
    output['sum'] = {}
    output['sumCum'] = {}
    output['aCodes'] = {}
    output['aCodesCum'] = {}

    for row in budget.index:
        output['aCodes'][budget['Account Code Description'][row]]    = {}
        output['aCodesCum'][budget['Account Code Description'][row]] = {}

    summary = 0
    for month in range(0,12):
        val = budget[ months[month] ].sum()
        output['sum'][month] = val

        summary += val
        output['sumCum'][month] = summary
        
        for row in budget.index:
            val = budget.loc [ row, months[month] ]
            output['aCodes'][budget['Account Code Description'][row]][month] = val
            output['aCodesCum'][budget['Account Code Description'][row]][month] = val
            if month>0:
                output['aCodesCum'][budget['Account Code Description'][row]][month] += output['aCodesCum'][ budget['Account Code Description'][row] ][month-1]
    return output


def WorkOrders(filter=[]):
    df = gen.filterDF(wo, filter)

    df = df.groupby(['raisedYear', 'raisedMonth', 'Work Order Status Description']).count()
    df.reset_index(drop=False, inplace=True)
    yearsLst  = df['raisedYear'].unique()
    statusLst = df['Work Order Status Description'].unique()

    byStatus = {}
    for status in ['raised', 'notClosed', *statusLst]:
        byStatus[status] = {}
        byStatus[status]['monthly'] = {}
        byStatus[status]['cumulat'] = {}
        for year in yearsLst:
            year = int(year)
            byStatus[status]['monthly'][year] = {}
            byStatus[status]['cumulat'][year] = {}
            for month in range(0,12):
                byStatus[status]['monthly'][year][month] = 0
                byStatus[status]['cumulat'][year][month] = 0

    for year in yearsLst:
        for month in range(0,12):
            dataChunk = gen.filterDF(df, [{'field':'raisedYear', 'value':year, 'operator':'=='}, 
                                            '&', {'field':'raisedMonth', 'value':month+1, 'operator':'=='} ])[['Work Order Status Description', 'Work Order Number']]
            if dataChunk.size == 0:
                continue
            byStatus['raised']['monthly'][year][month] = int(dataChunk['Work Order Number'].sum().item())
            byStatus['raised']['cumulat'][year][month] = int((byStatus['raised']['monthly'][year][month]) + (byStatus['raised']['cumulat'][year][month-1] if month>1 else 0))      
            byStatus['notClosed']['monthly'][year][month] = int(dataChunk.loc[ (dataChunk['Work Order Status Description'] != 'Closed') & (dataChunk['Work Order Status Description'] != 'Cancelled'), 'Work Order Number'].sum().item())
            byStatus['notClosed']['cumulat'][year][month] = int((byStatus['notClosed']['monthly'][year][month]) + (byStatus['notClosed']['cumulat'][year][month-1] if month>1 else 0))

            for row in dataChunk.index:
                statusName = dataChunk.loc[  row, 'Work Order Status Description' ]
                woCount    = dataChunk.loc[  row, 'Work Order Number' ]
                byStatus[statusName]['monthly'][year][month]    = int(woCount)
                byStatus[statusName]['cumulat'][year][month] = (byStatus[statusName]['monthly'][year][month]) + (byStatus[statusName]['cumulat'][year][month-1] if month>1 else 0)

    output = {}
    output['byStatus'] = byStatus
    return output


def Spares(spares, byAssets, param='all', filter='all'):
    ### 1. Выбор только Spares либо взятых в текущем году либо еще не взятых, но созданных в текущем году
    ###    и фильтрация dataFrame если указывается поле и значение для фильтра
    if param != 'all':
        spares = spares.loc[ spares[param] == filter ]
    spares = spares.loc[ (spares['reservYear'] == repYear) | ((spares['reservYear'] == 0) & (spares['raisedYear'] == repYear)), 
                         ['Asset ID', 'Account Code Description', 'Actual Cost', 'Estimated Cost','raisedYear','reservMonth','reservYear'] ]



    ### 2. Инициализация объекта
    output = {}
    output['actual']   = {}
    output['forecast'] = {}
    output['actual']['sum']       = {}
    output['actual']['sumCum']    = {}
    output['actual']['aCodes']    = {}
    output['actual']['aCodesCum'] = {}
    


    #### 3. Forecast Spares by assets
    forecast = spares.loc[ (spares['reservYear'] == 0) & (spares['raisedYear'] == repYear), ['Asset ID', 'Account Code Description', 'Estimated Cost'] ]
    output['forecast']['by Assets'] = byAssets(forecast[['Asset ID', 'Estimated Cost']].groupby('Asset ID').sum(), 'spares')



    #### 4. Forecast Spares by account Codes & summary:
    forecast = forecast[['Account Code Description','Estimated Cost']].groupby('Account Code Description').sum()
    output['forecast']['sum']    = forecast.sum().item()
    output['forecast']['aCodes'] = forecast.to_dict()
    


    #### 5. Actual Spares by assets 
    spares = spares.loc[ spares['reservYear'] == repYear, ['Asset ID', 'Account Code Description', 'Actual Cost', 'reservMonth'] ]
    output['actual']['by Assets'] = byAssets(spares[['Asset ID', 'Actual Cost']].groupby('Asset ID').sum(), 'spares')



    #### 6. Подготовка данных для анализа actual spares cost и создание списка account Codes
    spares = spares[['Account Code Description', 'Actual Cost', 'reservMonth']].groupby(['reservMonth','Account Code Description']).sum()   
    spares.reset_index(drop=False, inplace=True)
    acCodesList = spares['Account Code Description'].unique()



    ### 7. Инициализация подобъекта для каждого account Code
    for aCode in acCodesList:
        output['actual']['aCodes'][aCode] = {}
        output['actual']['aCodesCum'][aCode] = {}



    #### 8. Для каждого месяца
    for i in range(1, 13):
        ### 1. Если в данном месяце нет spares - установка всех значений = 0
        if i not in spares['reservMonth'].unique():
            output['actual']['sum'][months[i-1]] = 0
            if i == 1:
                output['actual']['sumCum'][months[i-1]] = 0
            else:
                output['actual']['sumCum'][months[i-1]] = output['actual']['sumCum'][months[i-2]]
            for aCode in acCodesList:
                output['actual']['aCodes'][aCode][months[i-1]] = 0
                if i == 1:
                    output['actual']['aCodesCum'][aCode][months[i-1]] = 0
                else:
                    output['actual']['aCodesCum'][aCode][months[i-1]] = output['actual']['aCodesCum'][aCode][months[i-2]]



        ### 2. Фильтраяция сгруппированного dataFrame по текущему месяцу
        spareList = spares.loc[ spares['reservMonth'] == i ]
        


        ### 3. Заполнение месячной суммы для каждого account Code и с накопительным итогом
        for aCode in acCodesList:
            if aCode not in list(spareList['Account Code Description']):
                aCodeVal = 0
            else:
                aCodeVal = spareList.loc[ spareList['Account Code Description'] == aCode, 'Actual Cost' ].item()
            output['actual']['aCodes'][aCode][months[i-1]] = aCodeVal
            ### Для накопительного итога берется значение текущего месяца + предыдущего
            if i == 1:
                output['actual']['aCodesCum'][aCode][months[i-1]] = aCodeVal
            else:
                output['actual']['aCodesCum'][aCode][months[i-1]] = aCodeVal + output['actual']['aCodesCum'][aCode][months[i-2]]
        


        ### 4. Заполнение месячных материальных расходов и с накопительным итогом
        val = spareList['Actual Cost'].sum()
        output['actual']['sum'][months[i-1]] = val
        if i == 1:
            output['actual']['sumCum'][months[i-1]] = val
        else:
            output['actual']['sumCum'][months[i-1]] = val + output['actual']['sumCum'][months[i-2]]

    return output