import xlsxwriter
from . import hub
from .. import gen
from . import subF
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__requisitions import requisitions




def an_requisitions():
    workbook = xlsxwriter.Workbook('reqs.xlsx')

    subF.oneLine(workbook, 'Total Expected Price', 'rq_raised_yearly', 'Raised', year = 2024, index=1, type = 'yearly')
    subF.oneLine(workbook, 'Total Expected Price', 'rq_required_yearly', 'Required', year = 2024, index=2, type = 'yearly', headers=False)
    subF.oneLine(workbook, 'Total Expected Price', 'rq_raised_monthly', 'Raised in 2023', year=2023, index=5, type='monthly')
    subF.oneLine(workbook, 'Total Expected Price', 'rq_raised_monthly', 'Raised in 2024', year=2024, index=6, type='monthly', headers=False)
    subF.oneLine(workbook, 'Total Expected Price', 'rq_required_monthly', 'Required in 2023', year=2023, index=7, type='monthly', headers=False)
    subF.oneLine(workbook, 'Total Expected Price', 'rq_required_monthly', 'Required in 2024', year=2024, index=8, type='monthly', headers=False)

    subF.categorized(workbook, 'By departments', 'rq_raised_Departments_yearly', 'Raised', index=1, type='yearly')
    subF.categorized(workbook, 'By departments', 'rq_required_Departments_yearly', 'Required', index=22, type='yearly')
    subF.categorized(workbook, 'By departments', 'rq_raised_Departments_monthly', 'Raised in 2023', index=43, type='monthly', year=2023)
    subF.categorized(workbook, 'By departments', 'rq_required_Departments_monthly', 'Required in 2023', index=63, type='monthly', year=2023)
    subF.categorized(workbook, 'By departments', 'rq_raised_Departments_monthly', 'Raised in 2024', index=83, type='monthly', year=2024)
    subF.categorized(workbook, 'By departments', 'rq_required_Departments_monthly', 'Required in 2024', index=94, type='monthly', year=2024)

    workbook.close()

def an_spares():
    workbook = xlsxwriter.Workbook('matCost.xlsx')

    subF.oneLine(workbook, 'Total', 'sp_reserved_yearly', 'Material Cost', year = 2024, index=1, type = 'yearly')
    subF.oneLine(workbook, 'Total', 'sp_reserved_monthly', 'in 2023', year=2023, index=4, type='monthly')
    subF.oneLine(workbook, 'Total', 'sp_reserved_monthly', 'in 2024', year=2024, index=5, type='monthly', headers=False)

    subF.rooted(workbook, 'By Assets 2023', 'sp_reserved_Assets_yearly', 'Actual Cost','Material Cost', year = 2023)
    subF.rooted(workbook, 'By Assets 2024', 'sp_reserved_Assets_yearly', 'Actual Cost','Material Cost', year = 2024)

    subF.categorized(workbook, 'By Priority', 'sp_reserved_Priority_yearly', 'Material Cost', index=1, type='yearly')
    subF.categorized(workbook, 'By Priority', 'sp_reserved_Priority_monthly', 'in 2023', index=12, type='monthly', year=2023)
    subF.categorized(workbook, 'By Priority', 'sp_reserved_Priority_monthly', 'in 2024', index=23, type='monthly', year=2024)

    subF.categorized(workbook, 'By JobType', 'sp_reserved_JobType_yearly', 'Material Cost', index=1, type='yearly')
    subF.categorized(workbook, 'By JobType', 'sp_reserved_JobType_monthly', 'in 2023', index=21, type='monthly', year=2023)
    subF.categorized(workbook, 'By JobType', 'sp_reserved_JobType_monthly', 'in 2024', index=39, type='monthly', year=2024)

    subF.categorized(workbook, 'By Department', 'sp_reserved_Department_yearly', 'Material Cost', index=1, type='yearly')
    subF.categorized(workbook, 'By Department', 'sp_reserved_Department_monthly', 'in 2023', index=19, type='monthly', year=2023)
    subF.categorized(workbook, 'By Department', 'sp_reserved_Department_monthly', 'in 2024', index=36, type='monthly', year=2024)

    subF.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_yearly', 'Material Cost', index=1, type='yearly')
    subF.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_monthly', 'in 2023', index=33, type='monthly', year=2023)
    subF.categorized(workbook, 'By Discipline', 'sp_reserved_Discipline_monthly', 'in 2024', index=64, type='monthly', year=2024)

    subF.fillExcelSheet(workbook, 'Top Expensive 2023', hub.getVal('sp_reserved_Assets_sorted_2023'))
    subF.fillExcelSheet(workbook, 'Top Expensive 2024', hub.getVal('sp_reserved_Assets_sorted_2024'))

    workbook.close()

def an_workorders():
    workbook = xlsxwriter.Workbook('workOrders.xlsx')

    subF.oneLine(workbook, 'Total', 'wo_raised_yearly', 'Raised WOs', year = 2024, index=1, type = 'yearly')
    subF.oneLine(workbook, 'Total', 'wo_closed_yearly', 'Closed WOs', year = 2024, index=2, type = 'yearly', headers=False)

    subF.rooted(workbook, 'By Assets 2023', 'wo_raised_Assets_yearly', 'Work Order Number','Raised WOs', year = 2023)
    subF.rooted(workbook, 'By Assets 2024', 'wo_raised_Assets_yearly', 'Work Order Number','Raised WOs', year = 2024)
    subF.rooted(workbook, 'Not Closed by Assets 2023', 'wo_open_Assets_yearly', 'Work Order Number','Not Closed WOs', year = 2023)
    subF.rooted(workbook, 'Not Closed by Assets 2024', 'wo_open_Assets_yearly', 'Work Order Number','Not Closed WOs', year = 2024)

    subF.categorized(workbook, 'By Planer', 'wo_raised_Planer_yearly', 'Raised WOs', index=1, type='yearly')
    subF.categorized(workbook, 'By Planer', 'wo_open_Planer_yearly', 'Not Closed WOs', index=57, type='yearly')
    subF.categorized(workbook, 'By Planer', 'wo_raised_Planer_monthly', 'Raised in 2023', index=94, type='monthly', year=2023)
    subF.categorized(workbook, 'By Planer', 'wo_open_Planer_monthly', 'Not Closed WOs in 2023', index=138, type='monthly', year=2023)
    subF.categorized(workbook, 'By Planer', 'wo_raised_Planer_monthly', 'Raised in 2024', index=170, type='monthly', year=2024)
    subF.categorized(workbook, 'By Planer', 'wo_open_Planer_monthly', 'Not Closed WOs in 2024', index=196, type='monthly', year=2024)

    subF.categorized(workbook, 'By Priority', 'wo_raised_Priority_yearly', 'Raised WOs', index=1, type='yearly')
    subF.categorized(workbook, 'By Priority', 'wo_open_Priority_yearly', 'Not Closed WOs', index=14, type='yearly')
    subF.categorized(workbook, 'By Priority', 'wo_raised_Priority_monthly', 'Raised in 2023', index=24, type='monthly', year=2023)
    subF.categorized(workbook, 'By Priority', 'wo_open_Priority_monthly', 'Not Closed WOs in 2023', index=36, type='monthly', year=2023)
    subF.categorized(workbook, 'By Priority', 'wo_raised_Priority_monthly', 'Raised in 2024', index=46, type='monthly', year=2024)
    subF.categorized(workbook, 'By Priority', 'wo_open_Priority_monthly', 'Not Closed WOs in 2024', index=60, type='monthly', year=2024)

    subF.categorized(workbook, 'By JobType', 'wo_raised_JobType_yearly', 'Raised WOs', index=1, type='yearly')
    subF.categorized(workbook, 'By JobType', 'wo_open_JobType_yearly', 'Not Closed WOs', index=23, type='yearly')
    subF.categorized(workbook, 'By JobType', 'wo_raised_JobType_monthly', 'Raised in 2023', index=42, type='monthly', year=2023)
    subF.categorized(workbook, 'By JobType', 'wo_open_JobType_monthly', 'Not Closed WOs in 2023', index=62, type='monthly', year=2023)
    subF.categorized(workbook, 'By JobType', 'wo_raised_JobType_monthly', 'Raised in 2024', index=77, type='monthly', year=2024)
    subF.categorized(workbook, 'By JobType', 'wo_open_JobType_monthly', 'Not Closed WOs in 2024', index=97, type='monthly', year=2024)

    subF.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_yearly', 'Raised WOs', index=1, type='yearly')
    subF.categorized(workbook, 'By Discipline', 'wo_open_Discipline_yearly', 'Not Closed WOs', index=36, type='yearly')
    subF.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_monthly', 'Raised in 2023', index=67, type='monthly', year=2023)
    subF.categorized(workbook, 'By Discipline', 'wo_open_Discipline_monthly', 'Not Closed WOs in 2023', index=102, type='monthly', year=2023)
    subF.categorized(workbook, 'By Discipline', 'wo_raised_Discipline_monthly', 'Raised in 2024', index=131, type='monthly', year=2024)
    subF.categorized(workbook, 'By Discipline', 'wo_open_Discipline_monthly', 'Not Closed WOs in 2024', index=156, type='monthly', year=2024)

    subF.categorized(workbook, 'By Department', 'wo_raised_Department_yearly', 'Raised WOs', index=1, type='yearly')
    subF.categorized(workbook, 'By Department', 'wo_open_Department_yearly', 'Not Closed WOs', index=20, type='yearly')
    subF.categorized(workbook, 'By Department', 'wo_raised_Department_monthly', 'Raised in 2023', index=35, type='monthly', year=2023)
    subF.categorized(workbook, 'By Department', 'wo_open_Department_monthly', 'Not Closed WOs in 2023', index=54, type='monthly', year=2023)
    subF.categorized(workbook, 'By Department', 'wo_raised_Department_monthly', 'Raised in 2024', index=69, type='monthly', year=2024)
    subF.categorized(workbook, 'By Department', 'wo_open_Department_monthly', 'Not Closed WOs in 2024', index=82, type='monthly', year=2024)

    subF.fillExcelSheet(workbook, 'Top Served 2023', hub.getVal('wo_raised_Assets_sorted_2023'))
    subF.fillExcelSheet(workbook, 'Top Served 2024', hub.getVal('wo_raised_Assets_sorted_2024'))

    workbook.close()


def writeExcel():
    an_requisitions()
    an_spares()
    an_workorders()

