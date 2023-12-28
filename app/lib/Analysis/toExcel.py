import xlsxwriter
import re
import pandas as pd
from . import hub
from ..gen import filterDF
from ...database.DF__wo import wo
from ...database.DF__spares import spares


def oneLine(workbook, sheetName, sectionName, seriesName, index = 1 ):
    if index == 1:
        worksheet = workbook.add_worksheet(sheetName)
    else:
        worksheet = workbook.get_worksheet_by_name(sheetName)
    source = hub.getVal(sectionName)

    if index == 1:
        for i in range(0,12):
            worksheet.write(0, i+1, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i])
            worksheet.write(0, i+15, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i])

    worksheet.write(index, 0, seriesName)
    worksheet.write(index, 14, seriesName+' Cumulative')

    for i in range(1,13):
        worksheet.write(index, i, source['data'][2023][i] if i in source['data'][2023] else 0)
        worksheet.write(index, i+14, source['cumulative'][2023][i] if i in source['cumulative'][2023] else 0)

def categorized(workbook, sheetName, sectionName, seriesName, index = 1 ):
    if index == 1:
        worksheet = workbook.add_worksheet(sheetName)
    else:
        worksheet = workbook.get_worksheet_by_name(sheetName)
    source = hub.getVal(sectionName)

    for i in range(0,12):
        worksheet.write(index -1, i+1, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i])
        worksheet.write(index -1, i+15, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i])

    
    worksheet.write(index-1, 0, seriesName)
    worksheet.write(index-1, 14, seriesName+' Cumulative')

    rowNumbers = {}
    row = index
    for i in range(1,13):
        data = source['data'][2023][i] if i in source['data'][2023] else {}
        cumulat = source['cumulative'][2023][i] if i in source['cumulative'][2023] else {}
        for key in data.keys():
            if key not in rowNumbers:
                rowNumbers[key] = row
                row += 1
            worksheet.write(rowNumbers[key], i, data[key])
        for key in cumulat.keys():
            worksheet.write(rowNumbers[key], i+14, cumulat[key])
        
    for key, value in rowNumbers.items():
        worksheet.write(value, 0, key)
        worksheet.write(value, 14, key)

def rooted(workbook, sheetName, sectionName, seriesName, header):
    worksheet = workbook.add_worksheet(sheetName) 
    source = hub.getVal(sectionName)
    source = source['data'][2023]

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


def writeExcel():
    workbook = xlsxwriter.Workbook('СС report for D.xlsx')
    oneLine(workbook, 'Overall Cost', 'materialCost_total', 'Mat.cost "by reservDate"')
    categorized(workbook, 'By Priority', 'materialCost_total_by_Priority', '$ Priority')
    categorized(workbook, 'By Priority', 'WO_raised_number_by_Priority', 'WO Priority', 11)
    categorized(workbook, 'By JobType', 'materialCost_total_by_JobType', '$ JobType')
    categorized(workbook, 'By JobType', 'WO_raised_number_by_JobType', 'WO JobType', 20)
    categorized(workbook, 'By Discipline', 'materialCost_total_by_Discipline', '$ Discipline')
    workbook.close()



    workbook1 = xlsxwriter.Workbook('WO_raised_number by assets.xlsx')
    rooted(workbook1, 'WO raised by Assets', 'WO_raised_number_by_Assets', 'Work Order ID','Raised WO number')
    workbook1.close()

    df = filterDF(wo, [
    {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
    "&",
    {"field":'raisedYear', "operator":"==", "value":"2023"}
    ])
    total = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    CM = ['Corrective', 'Corrective after STPdM']
    PM = ['Strategy', 'Strategy Predictive Monitoring/Fault Diagnostic', 'Operational Jobs', 'Modifications']
    OT = ['PPE','Special Tooling','Rework','Construction/Commissioning Works','Administration','Service for Air Product','Vehicle Reservations',]
    df.loc[:, ['Total raised', 'PMs raised', 'CMs raised', 'OTs raised']] = 0

    modDF = df.copy()
    for i in df.index:
        modDF.loc[i,'Total raised' ] = 1
        modDF.loc[ i, total[df.loc[i, 'raisedMonth'] - 1] ] = 1
        if df.loc[i, 'Job Type Description'] in CM:
            modDF.loc[i,'CMs raised'] = 1
        if df.loc[i, 'Job Type Description'] in PM:
            modDF.loc[i,'PMs raised'] = 1
        if df.loc[i, 'Job Type Description'] in OT:
            modDF.loc[i,'OTs raised'] = 1

    modDF = modDF.groupby(['Asset Description', 'Asset Number',]).sum()
    modDF.reset_index(drop=False, inplace=True)
    modDF['CMs'] = modDF['CMs raised']/ modDF['Total raised']
    modDF['PMs'] = modDF['PMs raised']/ modDF['Total raised']
    modDF['OTs'] = modDF['OTs raised']/ modDF['Total raised']
    modDF = modDF[['Asset Description', 'Asset Number', 'Total raised', 'CMs', 'PMs', 'OTs','CMs raised', 'PMs raised', 'OTs raised', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    modDF = modDF.sort_values(by=['Total raised'], ascending = False)
    modDF.to_excel('WO_raised_number sorted by assets.xlsx')



    workbook2 = xlsxwriter.Workbook('matCost by assets.xlsx')
    rooted(workbook2, 'matCost by Assets', 'materialCost_by_Assets', 'Actual Cost','Material Cost')
    workbook2.close()

    df = filterDF(spares, [
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'reservYear', "operator":"==", "value":"2023"}
    ])
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

    
    eqpt = pd.read_excel('eqpt1.xlsx')
    eqpt = eqpt.iloc[5:, [5,6,9]]
    eqpt.rename(columns={'Unnamed: 5':'tagNumber', 'Unnamed: 6':'Description', 'Unnamed: 9':'Cost'}, inplace=True)
    eqpt = eqpt.loc[~eqpt['tagNumber'].isna()]

    usedTags = []
    for i, row in modDF.iterrows():
        elems = row['Asset Number'].split('-')
        modDF.loc[i, 'Asset Cost'] = 0
        if len(elems)>=3:
            regexp = f"{elems[0]}.*{elems[1]}.*{elems[2][:3]}"
            for i, item in eqpt.iterrows():
                if re.search(regexp, item['tagNumber']): 
                    modDF.loc[i, 'Asset Cost'] = item['Cost']
                    usedTags.append(item.name)

    modDF.to_excel('matCost by assets.xlsx')
    eqpt.loc[~eqpt.index.isin(usedTags)].to_excel('unusedEqptTags.xlsx')


