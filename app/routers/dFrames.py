from fastapi import APIRouter
from .. import models
from ..lib import gen
from ..database import DF__transactions
from ..database import DF__spares
from ..database import DF__trades
from ..database import DF__wo


router = APIRouter(
    prefix="/dframes",
    tags=['Data Frames']
)

@router.get('/trades')
def dframe_trade():
    DF__trades.trades.to_excel('trades.xlsx')
    return {'trades':'ok'}

@router.get('/spares')
def dframe_spares():
    DF__spares.spares.to_excel('spares.xlsx')
    return {'spares':'ok'}

@router.get('/wo')
def dframe_wo():
    DF__wo.wo.to_excel('wo.xlsx')
    return {'wo':'ok'}

@router.get('/transactions')
def dframe_transactions():
    DF__transactions.transactions.to_excel('transactions.xlsx')
    return {'transactions':'ok'}


@router.post('/spares')
def materialCosts(response:models.Selection):
    filteredDF = gen.filterDF(DF__spares.spares, response.filters).fillna(0).to_dict('split')
    return filteredDF



@router.get('/Spares/filterList')
def getFilters():
    return gen.getFields(DF__spares.spares)
