import pandas as pd
import numpy as np
from .Analysis import hub


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


def simple_solidCumulate(obj, prevYear={}):
    newObj = {}
    isContainer = False

    for key, value in obj.items():
        if type(value) == dict:
            isContainer = True
            newObj[key] = simple_solidCumulate(value, newObj[ list(newObj.keys())[-1] ] if len(newObj.keys())>0 else {})

    if not isContainer:
        summary = prevYear[ list(prevYear.keys())[-1] ] if len( prevYear.keys() )>0 else 0
        for key, value in obj.items():
            summary += value
            newObj[key] = summary

    return newObj


def solidCumulate(obj, prev={}):
    newObj = {}
    isContainer = False
    isSubContainer = False

    for key, value in obj.items():
        if type(value) == dict:
            isSubContainer = True
            for k, v in value.items():
                if type(v) == dict:
                    isContainer = True
                    isSubContainer = False

        if isContainer:
            newObj[key] = solidCumulate(value, newObj[ list( newObj.keys() )[-1] ] if len(newObj.keys())>0 else {})

        if isSubContainer:
            prevPeriod = prev[ list( prev.keys() )[-1] ] if prev else {}
            newObj[key] = solidCumulate(value, prevPeriod if not newObj else newObj[ list(newObj.keys())[-1] ])

        if not isContainer and not isSubContainer:
            newObj[key] = value + (prev[key] if key in prev else 0)
            for i,x in prev.items():
                if i not in newObj:
                    newObj[i] = x

    return newObj



def fillExcelSheet(workbook, sheetname, df):
    worksheet = workbook.add_worksheet(sheetname)
    df = df.fillna(0)
    worksheet.write_row(0, 0, df.columns)
    index = 1
    for i, row in df.iterrows():
        worksheet.write_row(index, 0, row)
        index += 1
    
    



def oneLine(workbook, sheetname, sectionname, seriesname, year, index, type, headers = True):
    source = hub.getVal(sectionname)

    if index == 1:
        worksheet = workbook.add_worksheet(sheetname)
    else:
        worksheet = workbook.get_worksheet_by_name(sheetname)

    worksheet.write(index+1, 0, seriesname)
    worksheet.write(index+1, 14, seriesname +' Cumulative')

    periods = []
    data = {}
    if type == 'yearly':
        periods = source['data'].keys()
        data = source['data']
        cumuldata = source['cumulative']
    if type == 'monthly':
        periods = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = source['data'][year]
        cumuldata = source['cumulative'][year]
    for i, val in enumerate(periods):
        if type == 'yearly':
            worksheet.write(index+1, i+1, data[val] if val in data else 0)
            worksheet.write(index+1, i+15, cumuldata[val] if val in cumuldata else 0)
        if type == 'monthly':
            worksheet.write(index+1, i+1, data[i+1] if i+1 in data else 0)
            worksheet.write(index+1, i+15, cumuldata[i+1] if i+1 in cumuldata else 0)

        if headers == True:
            worksheet.write(index, i+1, val)
            worksheet.write(index, i+15, val)



def categorized(workbook, sheetname, sectionname, seriesname, index, type, year=2024):
    source = hub.getVal(sectionname)

    if index == 1:
        worksheet = workbook.add_worksheet(sheetname)
    else:
        worksheet = workbook.get_worksheet_by_name(sheetname)

    worksheet.write(index, 0, seriesname)
    worksheet.write(index, 14, seriesname +' Cumulative')

    periods = []
    if type == 'yearly':
        periods = source['data'].keys()
    if type == 'monthly':
        periods = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    rowNumbers = {}
    row = index+1
    for i, val in enumerate(periods):
        if type == 'yearly':
            data = source['data'][val]
            cumuldata = source['cumulative'][val]
        if type == 'monthly':
            data = source['data'][year][i+1] if i+1 in source['data'][year] else {}
            cumuldata = source['cumulative'][year][i+1] if i+1 in source['cumulative'][year] else {}
        for key in data.keys():
            if key not in rowNumbers:
                rowNumbers[key] = row
                row += 1
            worksheet.write(rowNumbers[key], i+1, data[key])
        for key in cumuldata.keys():
            worksheet.write(rowNumbers[key], i+15, cumuldata[key])
        worksheet.write(index, i+1, val)
        worksheet.write(index, i+15, val)

    for key, value in rowNumbers.items():
        worksheet.write(value, 0, key)
        worksheet.write(value, 14, key)
        

        
def rooted(workbook, sheetName, sectionName, seriesName, header, year = 2024):
    worksheet = workbook.add_worksheet(sheetName) 
    source = hub.getVal(sectionName)
    source = source['data'][year]

    worksheet.write('A1', 'Lvl')
    worksheet.write('B1', 'Asset Description')
    worksheet.write('C1', 'Asset Number')
    worksheet.write('D1', header)

    def rooting(src, index, lvl):
        worksheet.write(index, 0, lvl)
        worksheet.write(index, 1, src['description'])
        worksheet.write(index, 2, src['assetNumber'])
        worksheet.write(index, 3, src[seriesName])

        lvl += 1
        index += 1

        for key in src.keys():
            if key not in ['description', 'assetNumber', seriesName]:
                index = rooting(src[key], index, lvl)
        return index
    rooting(source, 1, 0)



