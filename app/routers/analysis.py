from fastapi import APIRouter
from .. import models
from ..lib.Analysis import hub 


router = APIRouter(
    prefix="/analysis",
    tags=['Analysis']
)



@router.get('/{section}')
def getVal(section: str):
    data = hub.getVal(section)
    return data



