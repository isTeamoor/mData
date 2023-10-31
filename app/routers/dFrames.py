from fastapi import APIRouter
from .. import models
from ..lib import gen
from ..database import DF__transactions, DF__spares


router = APIRouter(
    prefix="/dframes",
    tags=['Data Frames']
)


@router.post('/Spares')
def materialCosts(response:models.Filters):
    filteredDF = gen.filterDF(DF__spares.spares, response.filters).fillna(0).to_dict('split')
    return filteredDF


@router.get('/Spares/filterList')
def getFilters():
    return gen.getFields(DF__spares.spares)
