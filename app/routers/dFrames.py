from fastapi import APIRouter
from .. import models
from ..lib import gen
from ..database import DF__transactions, DF__spares, DF_requisitions


router = APIRouter(
    prefix="/dframes",
    tags=['Data Frames']
)


@router.post('/spares')
def materialCosts(response:models.Filters):
    filteredDF = gen.filterDF(DF__spares.spares, response.filters).fillna(0).to_dict('split')
    return filteredDF

@router.get('/requisitions')
def requisitions():
    DF_requisitions.reqItems.to_excel('reqItems.xlsx')
    DF_requisitions.reqItems_maintenance.to_excel('reqItems_maint.xlsx')
    DF_requisitions.reqItems_others.to_excel('reqItems_others.xlsx')
    return {'requisitions':'ok'}



@router.get('/Spares/filterList')
def getFilters():
    return gen.getFields(DF__spares.spares)
