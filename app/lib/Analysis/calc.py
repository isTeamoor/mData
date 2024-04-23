import pandas as pd 
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__assets import byAssets, checkRelationships


### Сумма/количество по 1 полю dataframe
def fieldTotal(df, theField, action, filters=[]):
    df = gen.filterDF(df, filters)

    if action == 'sum':
        output = df[theField].sum()
    if action == 'count':
        output = df[theField].count()
    output = int(output)

    return {'data':output}


### Сумма/количество по 1 полю dataframe с разделением по годам 
def fieldTotal_yearly(df, yearfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)

    data = gen.groupby_1(df, yearfield, theField, action)
    output = {'data': data, 
              'proportion':gen.proportion(data),
              'cumulative':gen.simpleCumulate(data)}
    
    return output


### Сумма/количество по 1 полю dataframe с разделением по годам и месяцам
def fieldTotal_monthly(df, yearfield, monthfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)

    data = gen.groupby_2(df, yearfield, monthfield, theField, action)
    output = {'data':data, 
              'proportion':gen.proportion(data), 
              'cumulative':gen.simpleCumulate(data)}
    
    return output


### Сумма/количество по 2 полям dataframe с разделением по годам
def coupleFields_yearly(df, yearfield, categoryField, valueField, action, filters=[]):
    df = gen.filterDF(df, filters)

    data = gen.groupby_2(df, yearfield, categoryField, valueField, action)
    output = {'data':data, 
              'proportion':gen.proportion(data),
              'cumulative':gen.cumulate(data)}
    
    return output


### Сумма/количество по 2 полям dataframe с разделением по годам и месяцам
def coupleFields_monthly(df, yearfield, monthfield, categoryField, valueField, action, filters=[]):
    df = gen.filterDF(df, filters)

    data = gen.groupby_3(df, yearfield, monthfield, categoryField, valueField, action)
    output = {'data':data, 
              'proportion':gen.proportion(data),
              'cumulative':gen.cumulate(data)}
    
    return output


### Сумма/количество по 1 полю dataframe по Assets (rooted) с разделением по годам
def fieldTotal_Assets_yearly(df, yearfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)

    output = {}
    for year, group in df[[yearfield, 'Asset ID', theField]].groupby(yearfield):
        source = group.groupby('Asset ID')[theField]
        if action == 'count':
            source = source.count()
        if action == 'sum':
            source = source.sum()
        output[year] = byAssets(source, theField)

    output = {'data':output}
    return output


### Сумма/количество по 1 полю dataframe по Assets (rooted) с разделением по годам и месяцам
def fieldTotal_Assets_monthly(df, yearfield, monthfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)

    output = {}
    for year, content in df[[yearfield, monthfield, 'Asset ID', theField]].groupby(yearfield):
        output[year] = {}
        for month, group in content[[monthfield, 'Asset ID', theField]].groupby(monthfield):
            source = group.groupby('Asset ID')
            if action == 'count':
                source = source.count()
            if action == 'sum':
                source = source.sum()
            output[year][month] = byAssets(source, theField)

    output = {'data':output}
    return output


### Сортировка материальных расходов по assets с детализацией по JobTypes
def sorted_matcost_assets(df, filters=[]):
    CM = ['Corrective', 'Corrective after STPdM']
    PM = ['Strategy', 'Strategy Predictive Monitoring/Fault Diagnostic', 'Operational Jobs', 'Modifications','Strategy Preventative','Condition Based Monitoring','Strategy Look Listen Feel']
    OT = ['PPE','Special Tooling','Rework','Construction/Commissioning Works','Administration','Service for Air Product','Vehicle Reservations',
          'undefined', 'Capital or Project Initiatives','Non-Maintanence Reservations', '03']

    df = gen.filterDF(df, filters)


    df.loc[:, ['Total cost', 'PMs cost', 'CMs cost', 'OTs cost']] = 0

    modDF = df.copy()
    for i in df.index:
        modDF.loc[i,'Total cost' ] = df.loc[i,'Actual Cost']
        if df.loc[i, 'Job Type Description'] in CM:
            modDF.loc[i,'CMs cost'] = df.loc[i,'Actual Cost']
        if df.loc[i, 'Job Type Description'] in PM:
            modDF.loc[i,'PMs cost'] = df.loc[i,'Actual Cost']
        if df.loc[i, 'Job Type Description'] in OT:
            modDF.loc[i,'OTs cost'] = df.loc[i,'Actual Cost']
    
    
    modDF = modDF.groupby(['Asset Description', 'Asset Number',]).sum()
    modDF.reset_index(drop=False, inplace=True)

    modDF['CMs'] = modDF['CMs cost']/ modDF['Total cost']
    modDF['PMs'] = modDF['PMs cost']/ modDF['Total cost']
    modDF['OTs'] = modDF['OTs cost']/ modDF['Total cost']
    
    modDF = modDF[['Asset Description', 'Asset Number', 'Total cost', 'CMs', 'PMs', 'OTs','CMs cost', 'PMs cost', 'OTs cost']]
    modDF = modDF.sort_values(by=['Total cost'], ascending = False)

    return modDF


### Сортировка количества raised WO по assets с детализацией по JobTypes
def sorted_woRaised_assets(df, filters=[]):
    df = gen.filterDF(wo, filters)

    df = df[['Work Order ID','Job Type Description', 'Asset Description','Asset Number', 'raisedMonth']]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    CM = ['Corrective', 'Corrective after STPdM']
    PM = ['Strategy', 'Strategy Predictive Monitoring/Fault Diagnostic', 'Operational Jobs', 'Modifications','Strategy Preventative','Condition Based Monitoring','Strategy Look Listen Feel']
    OT = ['PPE','Special Tooling','Rework','Construction/Commissioning Works','Administration','Service for Air Product','Vehicle Reservations',
          'undefined', 'Capital or Project Initiatives','Non-Maintanence Reservations', '03']













    df.loc[:, ['Total raised', 'PMs raised', 'CMs raised', 'OTs raised','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']] = 0


    modDF = df.copy()
    for i in df.index:
        modDF.loc[i,'Total raised' ] = 1
        modDF.loc[ i, months[df.loc[i, 'raisedMonth'] - 1] ] = 1
        if df.loc[i, 'Job Type Description'] in CM:
            modDF.loc[i,'CMs raised'] = 1
        if df.loc[i, 'Job Type Description'] in PM:
            modDF.loc[i,'PMs raised'] = 1
        if df.loc[i, 'Job Type Description'] in OT:
            modDF.loc[i,'OTs raised'] = 1


    modDF = modDF.groupby(['Asset Description', 'Asset Number']).sum()
    modDF.reset_index(drop=False, inplace=True)

    modDF['CMs'] = modDF['CMs raised']/ modDF['Total raised']
    modDF['PMs'] = modDF['PMs raised']/ modDF['Total raised']
    modDF['OTs'] = modDF['OTs raised']/ modDF['Total raised']

    modDF = modDF[['Asset Description', 'Asset Number', 'Total raised', 'CMs', 'PMs', 'OTs','CMs raised', 'PMs raised', 'OTs raised', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    modDF = modDF.sort_values(by=['Total raised'], ascending = False)

    return modDF