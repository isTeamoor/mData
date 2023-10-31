from ..database.DF__budget import budget, months
from ..database.DF__wo import wo
from ..database.DF__spares import spares
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
            val = budget[months[month]][row]
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

    output = {}
    for status in ['raised', 'notClosed', *statusLst]:
        output[status] = {}
        output[status]['monthly'] = {}
        output[status]['cumulat'] = {}
        for year in yearsLst:
            year = int(year)
            output[status]['monthly'][year] = {}
            output[status]['cumulat'][year] = {}
            for month in range(0,12):
                output[status]['monthly'][year][month] = 0
                output[status]['cumulat'][year][month] = 0

    for year in yearsLst:
        for month in range(0,12):
            dataChunk = gen.filterDF(df, [{'field':'raisedYear', 'value':year, 'operator':'=='}, 
                                      '&',{'field':'raisedMonth', 'value':month+1, 'operator':'=='} ])[['Work Order Status Description', 'Work Order Number']]
            if dataChunk.size == 0:
                continue
            output['raised']['monthly'][year][month] = int(dataChunk['Work Order Number'].sum().item())
            output['raised']['cumulat'][year][month] = int((output['raised']['monthly'][year][month]) + (output['raised']['cumulat'][year][month-1] if month>0 else 0))      
            output['notClosed']['monthly'][year][month] = int(dataChunk.loc[ (dataChunk['Work Order Status Description'] != 'Closed') & (dataChunk['Work Order Status Description'] != 'Cancelled'), 'Work Order Number'].sum().item())
            output['notClosed']['cumulat'][year][month] = int((output['notClosed']['monthly'][year][month]) + (output['notClosed']['cumulat'][year][month-1] if month>0 else 0))

            for status in dataChunk['Work Order Status Description'].unique():
                val = dataChunk.loc[  dataChunk['Work Order Status Description'] == status, 'Work Order Number' ]
                output[status]['monthly'][year][month]    = int(val)
                output[status]['cumulat'][year][month] = (output[status]['monthly'][year][month]) + (output[status]['cumulat'][year][month-1] if month>0 else 0)

    return output


def Spares(filter=[]):
    df = gen.filterDF(spares, filter)[['Asset ID', 'Account Code Description', 'Actual Cost', 'Estimated Cost','raisedYear','reservMonth','reservYear']]

    output = {}
    output['actual'] = {}
    output['actual']['sum']       = {}
    output['actual']['sumCum']    = {}
    output['actual']['aCodes']    = {}
    output['actual']['aCodesCum'] = {}
    output['forecast'] = {}
    output['forecast']['sum']     = {}
    output['forecast']['aCodes']  = {}

    df = df.groupby(['raisedYear', 'reservYear', 'reservMonth', 'Account Code Description'])[['Estimated Cost', 'Actual Cost']].sum()
    df.reset_index(drop=False, inplace=True)
    acCodesList = df['Account Code Description'].unique()

    for year in df.loc[ df['reservYear'] == 0, 'raisedYear'].unique():
        year = int(year)
        output['forecast']['sum'][year] = df.loc[ (df['reservYear'] == 0) & (df['raisedYear'] == year), 'Estimated Cost' ].sum()
        for aCode in acCodesList:
            if aCode not in output['forecast']['aCodes']:
                output['forecast']['aCodes'][aCode] = {}
            output['forecast']['aCodes'][aCode][year] = df.loc[ (df['reservYear'] == 0) & (df['raisedYear'] == year) & (df['Account Code Description'] == aCode), 'Estimated Cost' ].sum()

  
    for aCode in acCodesList:
        output['actual']['aCodes'][aCode] = {}
        output['actual']['aCodesCum'][aCode] = {}
        for year in df.loc[ df['reservYear'] != 0, 'reservYear'].unique():
            year = int(year)
            output['actual']['aCodes'][aCode][year] = {}
            output['actual']['aCodesCum'][aCode][year] = {}
            output['actual']['sum'][year] = {}
            output['actual']['sumCum'][year] = {}
            for month in range(0,12):
                output['actual']['aCodes'][aCode][year][month] = 0
                output['actual']['aCodesCum'][aCode][year][month] = 0
                output['actual']['sum'][year][month] = 0
                output['actual']['sumCum'][year][month] = 0


    for year in df.loc[ df['reservYear'] != 0, 'reservYear' ].unique():
        year = int(year)
        for month in range(0,12):
            output['actual']['sum'][year][month] = df.loc [ (df['reservYear'] == year) & (df['reservMonth'] == month+1), 'Actual Cost' ].sum()
            output['actual']['sumCum'][year][month] = (output['actual']['sum'][year][month]) + (output['actual']['sumCum'][year][month-1] if month>0 else 0)
            for aCode in acCodesList:
                output['actual']['aCodes'][aCode][year][month] = df.loc [ (df['reservYear'] == year) & (df['reservMonth'] == month+1)
                                                                        & (df['Account Code Description']) == aCode, 'Actual Cost' ].sum()
                output['actual']['aCodesCum'][aCode][year][month] = (output['actual']['aCodes'][aCode][year][month]) + (output['actual']['aCodesCum'][aCode][year][month-1] if month>0 else 0)

    return output