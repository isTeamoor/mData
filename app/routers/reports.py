from fastapi import APIRouter
from .. import models
from ..database.DF__transactions import transactions
from ..lib.MaterialReports import regular
from ..lib.KPI import report


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}/{department}')
def get_matrep(month:int, department:str):
    regular.matReport(repMonth=month, repYear=2024, department = department, transactions=transactions)
    return {'/matReport':'ok'}


@router.get('/kpiReport')
def get_kpirep():
    data = report.draw_report()
    return {'/kpiReport':'ok'}
