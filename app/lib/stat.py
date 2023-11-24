from datetime import datetime

from ..database.DF__budget import budget, months
from ..database.DF__spares import spares
from ..lib import gen
from ..database.DF_assets import byAssets, checkRelationships

def WorkOrders(wo, sections, filters=[]):
    wo = gen.filterDF(wo, filters)
    uniqs = gen.uniqueValues(wo, [*sections])
    yearsLst  = wo['raisedYear'].unique()
    statusLst = wo['Work Order Status Description'].unique()
    


    data = {}
    


    for field in uniqs.keys():
        data[field] = {}


        df = wo.groupby(['raisedYear', 'raisedMonth', field, 'Asset ID', 'Work Order Status Description']).count()
        df.reset_index(drop=False, inplace=True)
        
        
        for item in uniqs[field]:
            output = {}
            output = gen.initObject(yearsLst, ['raised', 'notClosed', *statusLst])
            output['byAssets'] = {}

            for year in yearsLst:
                for month in range(0,12):
                    
                    chunk = df.loc [ (df['raisedYear']==year) & (df['raisedMonth']==month+1) & (df[field]==item), ['Asset ID', 'Work Order Status Description', 'Work Order Number'] ]

                    output['raised']['monthly'][year][month] = int(chunk['Work Order Number'].sum().item())
                    output['raised']['cumulat'][year][month] = int((output['raised']['monthly'][year][month]) + (output['raised']['cumulat'][year][month-1] if month>0 else 0))  
                    output['notClosed']['monthly'][year][month] = int(chunk.loc[ (chunk['Work Order Status Description'] != 'Closed') & (chunk['Work Order Status Description'] != 'Cancelled'), 'Work Order Number'].sum().item())
                    output['notClosed']['cumulat'][year][month] = int((output['notClosed']['monthly'][year][month]) + (output['notClosed']['cumulat'][year][month-1] if month>0 else 0))
                    
                    for status in chunk['Work Order Status Description'].unique():
                        val = chunk.loc[  chunk['Work Order Status Description'] == status, 'Work Order Number' ].sum().item()
                        output[status]['monthly'][year][month]    = int(val)
                        output[status]['cumulat'][year][month] = (output[status]['monthly'][year][month]) + (output[status]['cumulat'][year][month-1] if month>0 else 0)

                    

                chunk = df.loc [ (df['raisedYear']==year) & (df[field]==item), ['Asset ID', 'Work Order Status Description', 'Work Order Number'] ]

                output['byAssets']['raised'] = byAssets(chunk[['Asset ID', 'Work Order Number']].groupby('Asset ID').sum(), 'woCount')
                output['byAssets']['notClosed'] = byAssets(chunk.loc[ (chunk['Work Order Status Description'] != 'Closed') 
                                                                                            & (chunk['Work Order Status Description'] != 'Cancelled'),['Asset ID', 'Work Order Number']].groupby('Asset ID').sum(), 'woCount')

                #for status in chunk['Work Order Status Description'].unique():
                    #output['byAssets'][status] = byAssets(chunk.loc[chunk['Work Order Status Description'] == status, ['Asset ID', 'Work Order Number']].groupby('Asset ID').sum(), 'woCount')
                
        
            data[field][item] = output
    return data




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