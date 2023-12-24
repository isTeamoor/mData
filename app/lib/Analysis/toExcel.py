import xlsxwriter
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
        worksheet.write(index, i+14, source['cumulative'][2023][i] if i in source['data'][2023] else 0)

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
        cumulat = source['cumulative'][2023][i] if i in source['data'][2023] else {}
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
    categorized(workbook, 'By Priority', 'materialCost_total_by_Priority', '$ Priority')#11
    categorized(workbook, 'By Priority', 'WO_raised_number_by_Priority', 'WO Priority', 11)

    categorized(workbook, 'By JobType', 'materialCost_total_by_JobType', '$ JobType')#11
    categorized(workbook, 'By JobType', 'WO_raised_number_by_JobType', 'WO JobType', 20)

    categorized(workbook, 'By Discipline', 'materialCost_total_by_Discipline', '$ Discipline')

    workbook.close()

    workbook1 = xlsxwriter.Workbook('raised WO by assets.xlsx')

    rooted(workbook1, 'WO raised by Assets', 'WO_raised_number_by_Assets', 'Work Order Number','Raised WO number')

    workbook1.close()


    workbook2 = xlsxwriter.Workbook('matCost by assets.xlsx')

    rooted(workbook2, 'matCost by Assets', 'materialCost_by_Assets', 'Actual Cost','Material Cost')

    workbook2.close()


    df = filterDF(wo, [
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'raisedYear', "operator":"==", "value":"2023"}
    ])
    modDF = df[['Asset ID', 'Asset Description', 'Asset Number', 'Work Order Number']].groupby(['Asset ID', 'Asset Description', 'Asset Number',]).count()
    modDF.reset_index(drop=False, inplace=True)
    modDF = modDF.sort_values(by=['Work Order Number'], ascending = False)
    modDF.to_excel('wo raised number for every asset.xlsx')


    df = filterDF(spares, [
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'reservYear', "operator":"==", "value":"2023"}
    ])
    modDF = df[['Asset ID', 'Asset Description', 'Asset Number', 'Actual Cost']].groupby(['Asset ID', 'Asset Description', 'Asset Number',]).sum()
    modDF.reset_index(drop=False, inplace=True)
    modDF = modDF.sort_values(by=['Actual Cost'], ascending = False)
    modDF.to_excel('material cost for every asset.xlsx')


    '''workbook = xlsxwriter.Workbook('Appendix 1.xlsx')
    
    oneLine(workbook, 'Material Cost', 'materialCost_total', 'Mat.cost "by reservDate"')
    oneLine(workbook, 'Material Cost', 'materialCost_closed', 'Mat.cost "by closedDate"', 2)

    categorized(workbook, 'Mat.Cost by', 'materialCost_total_by_Planers', 'Created By')#28
    categorized(workbook, 'Mat.Cost by', 'materialCost_total_by_JobType', 'JobType', 28)#44
    categorized(workbook, 'Mat.Cost by', 'materialCost_total_by_Priority', 'Priority', 44)#54
    categorized(workbook, 'Mat.Cost by', 'materialCost_total_by_Department', 'Department', 54)#70
    categorized(workbook, 'Mat.Cost by', 'materialCost_total_by_AccountCodes', 'Account Code', 70)

    rooted(workbook, 'Mat.Cost by Assets', 'materialCost_total(a)', 'Actual Cost','2023y used material expenses' )
    rooted(workbook, 'Mat.Cost by 1 planer', 'materialCost_total(a)_planer', 'Actual Cost','2023y used material expenses - For 1 planer' )
    rooted(workbook, 'Mat.Cost by 1 PriorityType', 'materialCost_total(a)_priority', 'Actual Cost','2023y used material expenses - For 1 PriorityType Emergency 24H' )



    categorized(workbook, 'Closed Cost by', 'materialCost_closed_by_Planers', 'Created By')#28
    categorized(workbook, 'Closed Cost by', 'materialCost_closed_by_JobType', 'JobType', 28)#44
    categorized(workbook, 'Closed Cost by', 'materialCost_closed_by_Priority', 'Priority', 44)#54
    categorized(workbook, 'Closed Cost by', 'materialCost_closed_by_Department', 'Department', 54)#70
    

    rooted(workbook, 'Closed Cost(A)', 'materialCost_closed(a)', 'Actual Cost','2023y Closed material expenses' )
    rooted(workbook, 'Closed Cost(A)-Planer', 'materialCost_closed(a)_planer', 'Actual Cost','2023y Closed material expenses - For 1 planer' )
    rooted(workbook, 'Closed Cost(A)-Priority', 'materialCost_closed(a)_priority', 'Actual Cost','2023y Closed material expenses - For 1 PriorityType Emergency 24H' )

    workbook.close()



    workbook2 = xlsxwriter.Workbook('Appendix 2.xlsx')
    oneLine(workbook2, 'Material Cost', 'f-emerg_materialCost_total', 'Mat.cost "by reservDate"')
    oneLine(workbook2, 'Material Cost', 'f-emerg_materialCost_closed', 'Mat.cost "by closedDate"', 2)

    categorized(workbook2, 'Mat.Cost by', 'f-emerg_materialCost_total_by_Planers', 'Created By')#28
    categorized(workbook2, 'Mat.Cost by', 'f-emerg_materialCost_total_by_JobType', 'JobType', 28)#44
    categorized(workbook2, 'Mat.Cost by', 'f-emerg_materialCost_total_by_Priority', 'Priority', 44)#54
    categorized(workbook2, 'Mat.Cost by', 'f-emerg_materialCost_total_by_Department', 'Department', 54)#70
    categorized(workbook2, 'Mat.Cost by', 'f-emerg_materialCost_total_by_AccountCodes', 'Account Code', 70)

    rooted(workbook2, 'Mat.Cost by Assets', 'f-emerg_materialCost_total(a)', 'Actual Cost','2023y used material expenses - by 1 Planer Emergency 24H' )

    categorized(workbook2, 'Closed Cost by', 'f-emerg_materialCost_closed_by_Planers', 'Created By')#28
    categorized(workbook2, 'Closed Cost by', 'f-emerg_materialCost_closed_by_JobType', 'JobType', 28)#44
    categorized(workbook2, 'Closed Cost by', 'f-emerg_materialCost_closed_by_Priority', 'Priority', 44)#54
    categorized(workbook2, 'Closed Cost by', 'f-emerg_materialCost_closed_by_Department', 'Department', 54)#70
    
    rooted(workbook2, 'Closed Cost(A)', 'f-emerg_materialCost_closed(a)', 'Actual Cost','2023y Closed material expenses - by 1 Planer Emergency 24H' )
    

    workbook2.close()'''