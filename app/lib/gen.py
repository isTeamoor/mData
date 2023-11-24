import pandas as pd
import numpy as np


def filterDF(df,  filters = 'all' ):
    if (filters == 'all') or (not filters):
        return df
    
    def conditionString(filters):
        conditions = ''
        for item in filters:
            if type(item)==dict:
                conditions += f'(   `{ item["field"] }` {item["operator"]} {item["value"]}   )'
            if type(item)==str:
                conditions += f" {item} "
            if type(item)==list:
                conditions += f'( {conditionString(item)} )'
        return conditions
    
    print(conditionString(filters))
    return df.query(conditionString(filters))


def uniqueValues(df, fieldsList):
    output = {}
    for field in fieldsList:
        output[field] = df[field].unique()
    return output


def initObject(yearsLst, fields):
    output = {}
    for field in fields:
        output[field] = {}
        output[field]['monthly'] = {}
        output[field]['cumulat'] = {}
        for year in yearsLst:
            year = int(year)
            output[field]['monthly'][year] = {}
            output[field]['cumulat'][year] = {}
            for month in range(0,12):
                output[field]['monthly'][year][month] = 0
                output[field]['cumulat'][year][month] = 0
    return output



def getFields(df):
    df = df.fillna(0)
    output = {}
    for column in df.columns:
        output[column] = []
        for item in df[column].unique():
            if type(item) not in [str, float, pd.Timestamp, int]:
                item = item.item()
            if type(item) == str:
                if ' ' in item:
                    item = f'"{item}"'
            output[column].append(item)
    return output



def woCalc(field, uniqs, df, byAssets):
    output = {}
    
    df = df.groupby(['raisedYear', 'raisedMonth', field, 'Work Order Status Description']).count()
    df.reset_index(drop=False, inplace=True)
    yearsLst  = df['raisedYear'].unique()
    statusLst = df['Work Order Status Description'].unique()
    
    for item in uniqs[field]:
        output[item] = initObject(yearsLst, ['raised', 'notClosed', *statusLst])
        
        for year in yearsLst:
            for month in range(0,12):
                part = df.loc [ (df['raisedYear']==year) & (df['raisedMonth']==month+1) & (df[field]==item), ['Work Order Status Description', 'Work Order Number'] ]
                if part.size == 0:
                    continue
                
                output[item]['raised']['monthly'][year][month] = int(part['Work Order Number'].sum().item())
                output[item]['raised']['cumulat'][year][month] = int((output[item]['raised']['monthly'][year][month]) + (output[item]['raised']['cumulat'][year][month-1] if month>0 else 0))      
                output[item]['notClosed']['monthly'][year][month] = int(part.loc[ (part['Work Order Status Description'] != 'Closed') & (part['Work Order Status Description'] != 'Cancelled'), 'Work Order Number'].sum().item())
                output[item]['notClosed']['cumulat'][year][month] = int((output[item]['notClosed']['monthly'][year][month]) + (output[item]['notClosed']['cumulat'][year][month-1] if month>0 else 0))
                
                for status in part['Work Order Status Description'].unique():
                    val = part.loc[  part['Work Order Status Description'] == status, 'Work Order Number' ].item()
                    output[item][status]['monthly'][year][month]    = int(val)
                    output[item][status]['cumulat'][year][month] = (output[item][status]['monthly'][year][month]) + (output[item][status]['cumulat'][year][month-1] if month>0 else 0)

    return output