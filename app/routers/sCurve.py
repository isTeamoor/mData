from fastapi import APIRouter
from .. import models
from ..lib import gen
from ..database import DF__budget



router = APIRouter(
    prefix="/sCurve",
)



@router.get('/planMonthly')
def show_WO():
    return DF__budget.monthly()
@router.get('/planCumulat')
def show_WO():
    return DF__budget.cumulat()

@router.post('/')
def postReq(requisition:models.requisition):
    return requisition
