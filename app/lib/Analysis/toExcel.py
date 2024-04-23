import xlsxwriter
from . import hub
from .. import gen
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__trades import trades
from ...database.DF__requisitions import requisitions




def an_requisitions():
    workbook = xlsxwriter.Workbook('reqs.xlsx')

    gen.oneLine(workbook, 'Total Expected Price', 'rq_raised_yearly', 'Raised', year = 2024, index=1, type = 'yearly')
    gen.oneLine(workbook, 'Total Expected Price', 'rq_required_yearly', 'Required', year = 2024, index=2, type = 'yearly', headers=False)
    gen.oneLine(workbook, 'Total Expected Price', 'rq_raised_monthly', 'Raised in 2023', year=2023, index=5, type='monthly')
    gen.oneLine(workbook, 'Total Expected Price', 'rq_raised_monthly', 'Raised in 2024', year=2024, index=6, type='monthly', headers=False)
    gen.oneLine(workbook, 'Total Expected Price', 'rq_required_monthly', 'Required in 2023', year=2023, index=7, type='monthly', headers=False)
    gen.oneLine(workbook, 'Total Expected Price', 'rq_required_monthly', 'Required in 2024', year=2024, index=8, type='monthly', headers=False)

    gen.categorized(workbook, 'By departments', 'rq_raised_Departments_yearly', 'Raised', index=1, type='yearly')
    gen.categorized(workbook, 'By departments', 'rq_required_Departments_yearly', 'Required', index=22, type='yearly')
    gen.categorized(workbook, 'By departments', 'rq_raised_Departments_monthly', 'Raised in 2023', index=43, type='monthly', year=2023)
    gen.categorized(workbook, 'By departments', 'rq_required_Departments_monthly', 'Required in 2023', index=63, type='monthly', year=2023)
    gen.categorized(workbook, 'By departments', 'rq_raised_Departments_monthly', 'Raised in 2024', index=83, type='monthly', year=2024)
    gen.categorized(workbook, 'By departments', 'rq_required_Departments_monthly', 'Required in 2024', index=94, type='monthly', year=2024)

    workbook.close()

    requisitions.to_excel('requisitions.xlsx')

def an_spares():
    workbook = xlsxwriter.Workbook('matCost.xlsx')

    gen.oneLine(workbook, 'Total', 'sp_reserved_yearly', 'Material Cost', year = 2024, index=1, type = 'yearly')
    gen.oneLine(workbook, 'Total', 'sp_reserved_monthly', 'in 2023', year=2023, index=4, type='monthly')
    gen.oneLine(workbook, 'Total', 'sp_reserved_monthly', 'in 2024', year=2024, index=5, type='monthly', headers=False)

    gen.rooted(workbook, 'By Assets 2023', 'sp_reserved_Assets_yearly', 'Actual Cost','Material Cost', year = 2023)
    gen.rooted(workbook, 'By Assets 2024', 'sp_reserved_Assets_yearly', 'Actual Cost','Material Cost', year = 2024)

    gen.categorized(workbook, 'By Priority', 'sp_reserved_Priority_yearly', 'Material Cost', index=1, type='yearly')
    gen.categorized(workbook, 'By Priority', 'sp_reserved_Priority_monthly', 'in 2023', index=12, type='monthly', year=2023)
    gen.categorized(workbook, 'By Priority', 'sp_reserved_Priority_monthly', 'in 2024', index=23, type='monthly', year=2024)

    gen.categorized(workbook, 'By JobType', 'sp_reserved_JobType_yearly', 'Material Cost', index=1, type='yearly')
    gen.categorized(workbook, 'By JobType', 'sp_reserved_JobType_monthly', 'in 2023', index=21, type='monthly', year=2023)
    gen.categorized(workbook, 'By JobType', 'sp_reserved_JobType_monthly', 'in 2024', index=39, type='monthly', year=2024)

    gen.categorized(workbook, 'By Department', 'sp_reserved_Department_yearly', 'Material Cost', index=1, type='yearly')
    gen.categorized(workbook, 'By Department', 'sp_reserved_Department_monthly', 'in 2023', index=19, type='monthly', year=2023)
    gen.categorized(workbook, 'By Department', 'sp_reserved_Department_monthly', 'in 2024', index=36, type='monthly', year=2024)

    gen.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_yearly', 'Material Cost', index=1, type='yearly')
    gen.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_monthly', 'in 2023', index=33, type='monthly', year=2023)
    gen.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_monthly', 'in 2024', index=64, type='monthly', year=2024)

    gen.fillExcelSheet(workbook, 'Top Expensive 2023', hub.getVal('sp_reserved_Assets_sorted_2023'))
    gen.fillExcelSheet(workbook, 'Top Expensive 2024', hub.getVal('sp_reserved_Assets_sorted_2024'))

    workbook.close()

    spares.to_excel('spares.xlsx')

def an_workorders():
    workbook = xlsxwriter.Workbook('workOrders.xlsx')

    gen.oneLine(workbook, 'Total', 'wo_raised_yearly', 'Raised WOs', year = 2024, index=1, type = 'yearly')
    gen.oneLine(workbook, 'Total', 'wo_closed_yearly', 'Closed WOs', year = 2024, index=2, type = 'yearly', headers=False)

    gen.rooted(workbook, 'By Assets 2023', 'wo_raised_Assets_yearly', 'Work Order Number','Raised WOs', year = 2023)
    gen.rooted(workbook, 'By Assets 2024', 'wo_raised_Assets_yearly', 'Work Order Number','Raised WOs', year = 2024)
    gen.rooted(workbook, 'Not Closed by Assets 2023', 'wo_open_Assets_yearly', 'Work Order Number','Not Closed WOs', year = 2023)
    gen.rooted(workbook, 'Not Closed by Assets 2024', 'wo_open_Assets_yearly', 'Work Order Number','Not Closed WOs', year = 2024)

    gen.categorized(workbook, 'By Planer', 'wo_raised_Planer_yearly', 'Raised WOs', index=1, type='yearly')
    gen.categorized(workbook, 'By Planer', 'wo_open_Planer_yearly', 'Not Closed WOs', index=57, type='yearly')
    gen.categorized(workbook, 'By Planer', 'wo_raised_Planer_monthly', 'Raised in 2023', index=94, type='monthly', year=2023)
    gen.categorized(workbook, 'By Planer', 'wo_open_Planer_monthly', 'Not Closed WOs in 2023', index=138, type='monthly', year=2023)
    gen.categorized(workbook, 'By Planer', 'wo_raised_Planer_monthly', 'Raised in 2024', index=170, type='monthly', year=2024)
    gen.categorized(workbook, 'By Planer', 'wo_open_Planer_monthly', 'Not Closed WOs in 2024', index=196, type='monthly', year=2024)

    gen.categorized(workbook, 'By Priority', 'wo_raised_Priority_yearly', 'Raised WOs', index=1, type='yearly')
    gen.categorized(workbook, 'By Priority', 'wo_open_Priority_yearly', 'Not Closed WOs', index=14, type='yearly')
    gen.categorized(workbook, 'By Priority', 'wo_raised_Priority_monthly', 'Raised in 2023', index=24, type='monthly', year=2023)
    gen.categorized(workbook, 'By Priority', 'wo_open_Priority_monthly', 'Not Closed WOs in 2023', index=36, type='monthly', year=2023)
    gen.categorized(workbook, 'By Priority', 'wo_raised_Priority_monthly', 'Raised in 2024', index=46, type='monthly', year=2024)
    gen.categorized(workbook, 'By Priority', 'wo_open_Priority_monthly', 'Not Closed WOs in 2024', index=54, type='monthly', year=2024)

    gen.categorized(workbook, 'By JobType', 'wo_raised_JobType_yearly', 'Raised WOs', index=1, type='yearly')
    gen.categorized(workbook, 'By JobType', 'wo_open_JobType_yearly', 'Not Closed WOs', index=23, type='yearly')
    gen.categorized(workbook, 'By JobType', 'wo_raised_JobType_monthly', 'Raised in 2023', index=42, type='monthly', year=2023)
    gen.categorized(workbook, 'By JobType', 'wo_open_JobType_monthly', 'Not Closed WOs in 2023', index=62, type='monthly', year=2023)
    gen.categorized(workbook, 'By JobType', 'wo_raised_JobType_monthly', 'Raised in 2024', index=77, type='monthly', year=2024)
    gen.categorized(workbook, 'By JobType', 'wo_open_JobType_monthly', 'Not Closed WOs in 2024', index=97, type='monthly', year=2024)

    gen.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_yearly', 'Raised WOs', index=1, type='yearly')
    gen.categorized(workbook, 'By Discipline', 'wo_open_Discipline_yearly', 'Not Closed WOs', index=36, type='yearly')
    gen.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_monthly', 'Raised in 2023', index=67, type='monthly', year=2023)
    gen.categorized(workbook, 'By Discipline', 'wo_open_Discipline_monthly', 'Not Closed WOs in 2023', index=102, type='monthly', year=2023)
    gen.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_monthly', 'Raised in 2024', index=131, type='monthly', year=2024)
    gen.categorized(workbook, 'By Discipline', 'wo_open_Discipline_monthly', 'Not Closed WOs in 2024', index=156, type='monthly', year=2024)

    gen.categorized(workbook, 'By Department', 'wo_raised_Department_yearly', 'Raised WOs', index=1, type='yearly')
    gen.categorized(workbook, 'By Department', 'wo_open_Department_yearly', 'Not Closed WOs', index=20, type='yearly')
    gen.categorized(workbook, 'By Department', 'wo_raised_Department_monthly', 'Raised in 2023', index=35, type='monthly', year=2023)
    gen.categorized(workbook, 'By Department', 'wo_open_Department_monthly', 'Not Closed WOs in 2023', index=54, type='monthly', year=2023)
    gen.categorized(workbook, 'By Department', 'wo_raised_Department_monthly', 'Raised in 2024', index=69, type='monthly', year=2024)
    gen.categorized(workbook, 'By Department', 'wo_open_Department_monthly', 'Not Closed WOs in 2024', index=82, type='monthly', year=2024)

    gen.fillExcelSheet(workbook, 'Top Served 2023', hub.getVal('wo_raised_Assets_sorted_2023'))
    gen.fillExcelSheet(workbook, 'Top Served 2024', hub.getVal('wo_raised_Assets_sorted_2024'))

    workbook.close()

    wo.to_excel('wo.xlsx')


def writeExcel():
    an_requisitions()
    an_spares()
    an_workorders()

### Annual report for D
'''workbook = xlsxwriter.Workbook('СС report for D.xlsx')
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
'''