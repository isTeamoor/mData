from fastapi import APIRouter
from .. import models
from ..lib import materialRep, planfact, KPI, checkStore
from ..database.DF__transactions import transactions
from ..lib.MaterialReports import regular


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}/{department}')
def get_matrep(month:int, department:str):
    regular.matReport(repMonth=month, repYear=2023, department = department, transactions=transactions)
    return {'/matReport':'ok'}

@router.get('/checkStore/{month}')
def warehouseTransactions(month:int):
    checkStore.exec(transactions=transactions, repMonth=month, repYear=2023)
    return {'/warehouseTransactions':'ok'}

@router.get('/kpi')
def show_kpi():
    KPI.kpiRep()
    return {'/kpi':'ok'}


@router.get('/planFact/')
def show_planFact():
    print('plan Monthly', planfact.plan_Monthly)
    print('\nactual Monthly', planfact.actual_Monthly)
    print('\nplan Cumulat', planfact.plan_Cumulat)
    print('\nactual Cumulat', planfact.actual_Cumulat)
    print('\nforecast', planfact.forecast)
    return {'/planFact':'ok'}