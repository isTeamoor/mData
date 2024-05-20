from fastapi import APIRouter
from ..database.DF__transactions import transactions
from ..database.DF__requisitions import requisitions
from ..lib.MaterialReports import regular
from ..lib.Requisitions import reqData
from ..lib.KPI import report



router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}/{department}')
def get_matrep(month:int, department:str):
    regular.matReport(repMonth=month, repYear=2024, department = department, transactions=transactions)
    return {'/matReport':'ok'}

@router.get('/requisitions')
def get_reqs():
    reqData.divide_source(requisitions)
    return {'/requisitions':'ok'}

@router.get('/kpiReport')
def get_kpirep():
    data = report.draw_report()
    return {'/kpiReport':'ok'}
