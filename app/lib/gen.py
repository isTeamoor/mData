import pandas as pd
import numpy as np


def filter(df,  filters = 'all' ):
    if (filters == 'all') or (len(filters) == 0):
        return df
    
    def conditionString(filters):
        condstring = ''
        for item in filters:
            if type(item)==dict:
                condstring += f'({ item["field"] } {item["math"]} {item["value"]})'
            if type(item)==str:
                condstring += f" {item} "
            if type(item)==list:
                condstring += f'({conditionString(item)})'
        return condstring
    
    condition = conditionString(filters)
    return df.query(condition)




def group(df, fields, action):
    df = df.groupby(fields)
    if action == 'sum':
        df = df.sum()
    if action == 'count':
        df = df.count()
    df.reset_index(drop=False, inplace=True)
    return df, [ df[field].unique() for field in fields ]




def newObj(years, sections):
    output = {}
    for section in sections:
        output[section] = {}
        output[section]['monthly'] = {}
        output[section]['cumulat'] = {}
        for year in years:
            year = int(year)
            output[section]['monthly'][year] = {}
            output[section]['cumulat'][year] = {}
            for month in range(1,13):
                output[section]['monthly'][year][month] = 0
                output[section]['cumulat'][year][month] = 0
    return output



### 7. Функция для создания json-объекта статистика по spares
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

