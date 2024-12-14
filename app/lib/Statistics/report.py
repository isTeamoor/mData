import xlsxwriter
from . import hub
from .. import gen
from . import subF
from .subF import oneLine, categorized, rooted, fillExcelSheet
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__requisitions import requisitions


def an_requisitions():
    workbook = xlsxwriter.Workbook('reqs.xlsx')


    sheetName = 'Total Expected Price'
    oneLine(workbook, sheetName, src='rq_raised_yearly',    title='Raised',           type='yearly',  index=1,  headers=True)
    oneLine(workbook, sheetName, src='rq_required_yearly',  title='Required',         type='yearly',  index=3,  headers=True)
    #oneLine(workbook, sheetName, src='rq_raised_monthly',   title='Raised in 2024',   type='monthly', index=7,  headers=False, year=2024)
    #oneLine(workbook, sheetName, src='rq_required_monthly', title='Required in 2024', type='monthly', index=9,  headers=False, year=2024)

    sheetName = 'By planers'
    categorized(workbook, sheetName, src='rq_raised_Planer_yearly',    title='Raised',           type='yearly',  index=1)

    sheetName = 'By approval path'
    categorized(workbook, sheetName, src='rq_raised_Departments_yearly',    title='Raised',           type='yearly',  index=1)
    #categorized(workbook, sheetName, src='rq_required_Departments_yearly',  title='Required',         type='yearly',  index=22)
    #categorized(workbook, sheetName, src='rq_raised_Departments_monthly',   title='Raised in 2024',   type='monthly', index=83, year=2024)
    #categorized(workbook, sheetName, src='rq_required_Departments_monthly', title='Required in 2024', type='monthly', index=94, year=2024)

    
    workbook.close()

def an_spares():
    workbook = xlsxwriter.Workbook('matCost.xlsx')

    sheetName = 'Total'
    oneLine(workbook, sheetName, src='sp_reserved_monthly', title='in 2024',       type='monthly', index=1, headers=True, year=2024)
    oneLine(workbook, sheetName, src='sp_reserved_monthly', title='in 2023',       type='monthly', index=4, headers=True, year=2023)
    #oneLine(workbook, sheetName, src='sp_reserved_yearly',  title='Material Cost', type='yearly',  index=1, headers=True)

    sheetName = 'By Discipline'
    categorized(workbook, sheetName, src='sp_reserved_Discipline_yearly', title='Material Cost', type='yearly', index=1)
    #categorized(workbook, sheetName, src='sp_reserved_Discipline_monthly', title='in 2024',      type='monthly', index=64, year=2024)

    sheetName = 'By Assets'
    rooted(workbook, sheetName, src='sp_reserved_Assets_yearly', title='Actual Cost', header='Material Cost', year = 2024)

    sheetName = 'Top Expensive 2024'
    fillExcelSheet(workbook, sheetName, hub.getVal('sp_reserved_Assets_sorted_2024'))

    sheetName = 'By Priority'
    categorized(workbook, sheetName, src='sp_reserved_Priority_yearly',  title='Material Cost', type='yearly',  index=1)
    #categorized(workbook, sheetName, src='sp_reserved_Priority_monthly', title='in 2024',       type='monthly', index=23, year=2024)

    sheetName = 'By JobType'
    categorized(workbook, sheetName, src='sp_reserved_JobType_yearly',  title='Material Cost', type='yearly',  index=1)
    #categorized(workbook, sheetName, src='sp_reserved_JobType_monthly', title='in 2024',       type='monthly', index=39, year=2024)

    #sheetName = 'By Department'
    #categorized(workbook, sheetName, src='sp_reserved_Department_yearly', title='Material Cost', type='yearly', index=1)
    #categorized(workbook, sheetName, src='sp_reserved_Department_monthly', title='in 2024',      type='monthly', index=36, year=2024)  

    
    workbook.close()

def an_workorders():
    workbook = xlsxwriter.Workbook('workOrders.xlsx')

    sheetName = 'By Assets 2024'
    rooted(workbook, sheetName, src='wo_raised_Assets_yearly', title='Work Order Number', header='Raised WOs', year = 2024)

    sheetName = 'Top Served 2024'
    fillExcelSheet(workbook, sheetName, hub.getVal('wo_raised_Assets_sorted_2024'))

    sheetName = 'Total'
    oneLine(workbook, 'Total', src='wo_raised_yearly', title='Raised WOs', type = 'yearly',year = 2024, index=1, headers=True)
    oneLine(workbook, 'Total', src='wo_open_yearly', title='Not Closed WOs', type = 'yearly', year = 2024, index=3, headers=True)

    sheetName = 'By Priority'
    categorized(workbook, sheetName, src='wo_raised_Priority_yearly', title='Raised WOs', type='yearly', index=1, )
    #categorized(workbook, sheetName, src='wo_open_Priority_yearly', title='Not Closed WOs', type='yearly', index=14, )
    #categorized(workbook, sheetName, src='wo_raised_Priority_monthly', title='Raised in 2024', type='monthly', index=46, year=2024)
    #categorized(workbook, sheetName, src='wo_open_Priority_monthly', title='Not Closed WOs in 2024', type='monthly', index=60, year=2024)

    sheetName = 'By JobType'
    categorized(workbook, sheetName, src='wo_raised_JobType_yearly', title='Raised WOs', type='yearly', index=1, )
    #categorized(workbook, sheetName, src='wo_open_JobType_yearly', title='Not Closed WOs', type='yearly', index=23, )
    #categorized(workbook, sheetName, src='wo_raised_JobType_monthly', title='Raised in 2024', type='monthly', index=77, year=2024)
    #categorized(workbook, sheetName, src='wo_open_JobType_monthly', title='Not Closed WOs in 2024', type='monthly', index=97, year=2024)

    sheetName = 'By Planer'
    categorized(workbook, sheetName, src='wo_open_Planer_yearly', title='Not Closed WOs', type='yearly',index=1, )
    #categorized(workbook, sheetName, src='wo_raised_Planer_yearly', title='Raised WOs', type='yearly', index=1, )
    #categorized(workbook, sheetName, src='wo_raised_Planer_monthly', title='Raised in 2024', type='monthly', index=170, year=2024)
    #categorized(workbook, sheetName, src='wo_open_Planer_monthly', title='Not Closed WOs in 2024', type='monthly', index=196, year=2024)

    """
    sheetName = 'Not Closed by Assets 2024'
    rooted(workbook, sheetName, src='wo_open_Assets_yearly', title='Work Order Number',header='Not Closed WOs', year = 2024)

    sheetName = 'By Discipline'
    categorized(workbook, sheetName, src='wo_raised_Discipline_yearly', title='Raised WOs', type='yearly', index=1, )
    categorized(workbook, sheetName, src='wo_open_Discipline_yearly', title='Not Closed WOs', type='yearly', index=36, )
    categorized(workbook, sheetName, src='wo_raised_Discipline_monthly', title='Raised in 2024', type='monthly', index=131, year=2024)
    categorized(workbook, sheetName, src='wo_open_Discipline_monthly', title='Not Closed WOs in 2024', type='monthly', index=156, year=2024)

    sheetName = 'By Department'
    categorized(workbook, sheetName, src='wo_raised_Department_yearly', title='Raised WOs', type='yearly', index=1, )
    categorized(workbook, sheetName, src='wo_open_Department_yearly', title='Not Closed WOs', type='yearly', index=20, )
    categorized(workbook, sheetName, src='wo_raised_Department_monthly', title='Raised in 2024', type='monthly', index=69, year=2024)
    categorized(workbook, sheetName, src='wo_open_Department_monthly', title='Not Closed WOs in 2024', type='monthly', index=82, year=2024)
    """
    
    workbook.close()


def writeExcel():
    an_requisitions()
    an_spares()
    an_workorders()

