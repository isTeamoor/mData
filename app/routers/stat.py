from fastapi import APIRouter
from .. import models
from ..lib import stat

router = APIRouter(
    prefix="/stat",
    tags=['Statistics']
)



@router.get('/budget')
def stat_budget():
    values = stat.Budget()
    return values


@router.post('/wo')
def stat_wo(filter:models.Filters):
    values = stat.WorkOrders(filter)
    return values


@router.post('/spares')
def stat_wo(filter:models.Filters):
    values = stat.Spares(filter)
    return values
