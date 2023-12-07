from fastapi import APIRouter
from .. import models
from ..lib import materialRep
from ..database.DF__transactions import transactions
from ..lib.MaterialReports import regular


router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)


@router.get('/matReport/{month}/{department}')
def get_matrep(month:int, department:str):
    regular.matReport(repMonth=month, repYear=2023, department = department, transactions=transactions)
    return {'/matReport':'ok'}


