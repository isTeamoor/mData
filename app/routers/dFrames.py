from fastapi import APIRouter
from ..database import DF__transactions
from ..database import DF__spares
from ..database import DF__trades
from ..database import DF__wo
from ..database import DF__requisitions
from ..database import DF__assets
from ..database import DF__requests
from ..database import DF__tasks


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

@router.get('/requisitions')
def dframe_transactions():
    DF__requisitions.requisitions.to_excel('requisitions.xlsx')
    return {'requisitions':'ok'}

@router.get('/assetChildren')
def dframe_assetChildren():
    print(DF__assets.unitChildren())
    return {'assetChildren':DF__assets.AssetsRelationships}

@router.get('/requests')
def dframe_requests():
    DF__requests.requests.to_excel('requests.xlsx')
    return {'requests':'ok'}

@router.get('/tasks')
def dframe_tasks():
    DF__tasks.tasks.to_excel('tasks.xlsx')
    return {'tasks':'ok'}

