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


def uniqueValues(df, fielsList):
    output = {}
    for field in fielsList:
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

