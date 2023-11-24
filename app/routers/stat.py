from fastapi import APIRouter
from .. import models
from ..lib import stat
from ..database.DF__wo import wo
from ..database.DF_assets import checkRelationships

router = APIRouter(
    prefix="/stat",
    tags=['Statistics']
)



@router.post('/wo')
def stat_wo(selection:models.Selection):
    values = stat.WorkOrders(wo, selection.sections, selection.filters)
    return values

@router.get('/sectionsList')
def sectionsList():
    return list(wo.columns)

@router.get('/printwo')
def show_wo():
    wo.to_excel('wo.xlsx')
    checkRelationships(wo[['Asset ID', 'Work Order Number']].groupby('Asset ID').count())
    return {}