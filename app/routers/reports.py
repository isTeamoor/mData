from fastapi import APIRouter
from .. import models
from ..lib import materialRep,gen, planfact, stat
from ..database import DF__transactions, DF__spares


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}')
def show_WO(month:int):
    materialRep.matReport(repMonth=month, repYear=2023, transactions=DF__transactions.transactions)
    return {'/matReport':'ok'}

@router.get('/stat/budget')
def stat_budget():
    values = stat.Budget()
    return values['aCodes']

@router.get('/stat/wo')
def stat_wo():
    values = stat.WorkOrders()
    return values


@router.get('/planFact/')
def show_planFact():
    print('plan Monthly', planfact.plan_Monthly)
    print('\nactual Monthly', planfact.actual_Monthly)
    print('\nplan Cumulat', planfact.plan_Cumulat)
    print('\nactual Cumulat', planfact.actual_Cumulat)
    print('\nforecast', planfact.forecast)
    return {'/planFact':'ok'}



@router.post('/Spares')
def materialCosts(response:models.Filters):
    filteredDF = gen.filterDF(DF__spares.spares, response.filters).fillna(0).to_dict('split')
    return filteredDF



@router.get('/Spares/filterList')
def getFilters():
    return gen.getFields(DF__spares.spares)
