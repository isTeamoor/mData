from fastapi import APIRouter
from .. import models
from ..lib import materialRep, planfact, KPI
from ..database.DF__transactions import transactions


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}/{department}')
def show_matrep(month:int, department:str):
    materialRep.matReport(repMonth=month, repYear=2023, department = department, transactions=transactions)
    return {'/matReport':'ok'}

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