from fastapi import APIRouter
from .. import models
from ..lib.Analysis import hub,checkBugs
from ..lib.Analysis.toExcel import writeExcel
#from ..lib.purch import purchs


router = APIRouter(
    prefix="/analysis",
    tags=['Analysis']
)


@router.get('/section/{section}')
def getVal(section: str):
    data = hub.getVal(section)
    return data

@router.get('/toExcel')
def writeAnalysisReport():
    writeExcel()
    return {'done':'True'}

@router.get('/check')
def fix():
    checkBugs.check()
    return {'done':'True'}

@router.get('/purch')
def checkPurch():
    return {'done':'True'}



