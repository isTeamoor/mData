from fastapi import APIRouter
from .. import models
from ..lib import gen
from ..database import DF__wo



router = APIRouter(
    prefix="/workOrders",
    tags=['Work Orders']
)


@router.get('/')
def show_WO():
    return DF__wo.wo_test
