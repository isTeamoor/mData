import pandas as pd 
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__assets import byAssets


##############################
###-     Sub Functions    -###
##############################
def sub_fieldTotal(df, theField, action):
    if action == 'sum':
        output = df[theField].sum()
    if action == 'count':
        output = df[theField].count()
    output = int(output)
    return output 

def groupby_1(df, groupField, valueField, action):
    output = df[[groupField, valueField]].groupby(groupField)[valueField]

    if action == 'count':
        output = output.count()
    if action == 'sum':
        output = output.sum()

    output.sort_index(ascending=True, inplace=True)
    output = output.to_dict()
    return output

def groupby_2(df, groupField, subgroupField, valueField, action):
    output = {}
    for name, content in df[[groupField, subgroupField, valueField]].groupby(groupField):
        output[name] = groupby_1(content, subgroupField, valueField, action)
    return output

def groupby_3(df, groupField, subgroupField, lastgroupField, valueField, action):
    output = {}
    for name, content in df[[groupField, subgroupField, lastgroupField, valueField]].groupby(groupField):
        output[name] = groupby_2(content, subgroupField, lastgroupField, valueField, action)
    return output

def proportion(obj):
    newObj = {}
    isContainer = False

    for key, value in obj.items():
        if type(value) == dict:
            isContainer = True
            newObj[key] = proportion(value)

    if not isContainer:
        summary = sum(obj.values())
        for key, value in obj.items():
            newObj[key] = round(obj[key]/summary*100, 1) if summary > 0 else 0
    return newObj

def simpleCumulate(obj):
    newObj = {}
    isContainer = False

    for key, value in obj.items():
        if type(value) == dict:
            isContainer = True
            newObj[key] = simpleCumulate(value)

    if not isContainer:
        summary = 0
        print(obj.keys())
        for key, value in obj.items():
            summary += value
            newObj[key] = summary

    return newObj

def cumulate(obj, prevMonthly={}):
    newObj = {}
    isContainer = False

    for key, value in obj.items():
        if type(value) == dict:
            isContainer = True
            newObj[key] = cumulate(value, newObj[list(newObj.keys())[-1]] if len(newObj.keys())>0 else {})

    if not isContainer:
        for key, value in obj.items():
            newObj[key] = (value) + (prevMonthly[key] if key in prevMonthly else 0)

        for key, value in prevMonthly.items():
            if key not in newObj:
                newObj[key] = value

    return newObj




##############################
###-     Main Functions   -###
##############################


def fieldTotal(df, theField, action, filters=[]):
    df = gen.filterDF(df, filters)
    return {'data':sub_fieldTotal(df, theField, action)}

def fieldTotal_by_year(df, yearfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)
    data = groupby_1(df, yearfield, theField, action)
    output = {'data': data, 
              'proportion':proportion(data),
              'cumulative':simpleCumulate(data)}
    return output

def fieldTotal_by_year_month(df, yearfield, monthfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)
    data = groupby_2(df, yearfield, monthfield, theField, action)
    output = {'data':data, 
              'proportion':proportion(data), 
              'cumulative':simpleCumulate(data)}
    return output

def fieldTotal_by_Assets_year(df, yearfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)
    output = {}
    for year, group in df[[yearfield, theField, 'Asset ID']].groupby(yearfield):
        source = group.groupby('Asset ID')[theField]
        if action == 'count':
            source = source.count()
        if action == 'sum':
            source = source.sum()
        output[year] = byAssets(source, theField)
    output = {'data':output}
    return output

def fieldTotal_by_Assets_year_month(df, yearfield, monthfield, theField, action, filters=[]):
    df = gen.filterDF(df, filters)
    output = {}
    for year, content in df[[yearfield, monthfield, theField, 'Asset ID']].groupby(yearfield):
        output[year] = {}
        for month, group in content[[monthfield, theField, 'Asset ID']].groupby(monthfield):
            source = group.groupby('Asset ID')[theField]
            if action == 'count':
                source = source.count()
            if action == 'sum':
                source = source.sum()
            output[year][month] = byAssets(source, theField)
    output = {'data':output}
    return output

def coupleFields_by_year(df, yearfield, categoryField, valueField, action, filters=[]):
    df = gen.filterDF(df, filters)
    data = groupby_2(df, yearfield, categoryField, valueField, action)
    output = {'data':data, 
              'proportion':proportion(data),
              'cumulative':cumulate(data)}
    return output

def coupleFields_by_year_month(df, yearfield, monthfield, categoryField, valueField, action, filters=[]):
    df = gen.filterDF(df, filters)
    data = groupby_3(df, yearfield, monthfield, categoryField, valueField, action)
    output = {'data':data, 
              'proportion':proportion(data),
              'cumulative':cumulate(data)}
    return output

