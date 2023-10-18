from fastapi import APIRouter
from .. import models
from ..lib import materialRep
from ..database import DF__transactions, DF_requisitions, DF__spares


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}')
def show_WO(month:int):
    materialRep.matReport(repMonth=month, repYear=2023, transactions=DF__transactions.transactions)
    return {'/matReport':'ok'}


@router.get('/Spares')
def show_WO():
    DF__spares.spares_RMPD.to_excel('spares_RMPD.xlsx')
    return {'/spares':'ok'}

@router.get('/requisitions')
def show_WO():
    DF_requisitions.reqItems.to_excel('reqItems.xlsx')
    return {'/requisitions':'ok'}