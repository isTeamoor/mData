from fastapi import APIRouter
from ..database.DF__transactions import transactions
from ..database.DF__requisitions import requisitions
from ..lib.MaterialReports import regular
from ..lib.Statistics import report
from ..lib.PO import reqData
from ..lib.PO import payments
from ..lib.Utils import checkBugs
from ..lib.Utils import checkStore

router = APIRouter(
    prefix="/report",
    tags=['Reports']
)



@router.get('/matReport/{month}/{department}')
def get_matrep(month:int, department:str):
    regular.matReport(repMonth=month, repYear=2024, department = department, transacts=transactions)
    return {'/matReport':'ok'}

@router.get('/requisitions')
def get_reqs():
    reqData.divide_source(requisitions)
    return {'/requisitions':'ok'}

@router.get('/payments/{department}')
def get_payments(department:str):
    payments.sumPayments('overall')
    payments.sumPayments('rmpd')
    payments.sumPayments('cofe')
    payments.sumPayments('tar')
    payments.sumPayments('mtk')
    
    data = payments.draw_report(department = department)
    return {'/payments':'ok'}

@router.get('/toExcel')
def writeAnalysisReport():
    report.writeExcel()
    return {'done':'True'}

@router.get('/checkbugs')
def fix():
    checkBugs.check()
    return {'done':'True'}

@router.get('/checkstore')
def fix():
    checkStore.exec()
    return {'done':'True'}
