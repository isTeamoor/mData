from fastapi import APIRouter
from .. import models
from ..database.DF__wo import wo
from ..database.DF__spares import spares
from ..database.DF__trades import trades
from ..database.DF_assets import byAssets
from ..lib import stat
from ..database.DF_assets import checkRelationships

router = APIRouter(
    prefix="/utils",
    tags=['Utils']
)



@router.get('/WO_total_number')
def WO_total_number():
    return wo['Work Order Number'].count().item()

@router.get('/WO_raised_years')
def WO_raised_years():
    return list(  map( lambda item: int(item), wo['raisedYear'].unique() )  )

@router.get('/WO_raised_byYears')
def WO_raised_byYears():
    output = {}
    for raisedYear in wo['raisedYear'].unique():
        val = wo.loc[ wo['raisedYear'] == raisedYear, 'Work Order Number' ].count().item()
        output[int(raisedYear)] = int(val)
    return output

@router.get('/WO_departments_List')
def WO_departments_List():
    return list(wo['Short Department Name'].unique())

@router.get('/WO_raised_byDepartments')
def WO_raised_byDepartments():
    output = {}
    for department in wo['Short Department Name'].unique():
        output[department] = {}
        output[department]['total'] = int(wo.loc[ wo['Short Department Name'] == department, 'Work Order Number' ].count().item())
        for raisedYear in wo['raisedYear'].unique():
            val = wo.loc[ (wo['raisedYear'] == raisedYear) & (wo['Short Department Name'] == department), 'Work Order Number' ].count().item()
            output[department][int(raisedYear)] = int(val)
    return output

@router.get('/WO_priority_List')
def WO_priority_List():
    return list(wo['Priority Description'].unique())

@router.get('/WO_raised_byPriority')
def WO_raised_byPriority():
    output = {}
    for priority in wo['Priority Description'].unique():
        output[priority] = {}
        output[priority]['total'] = int(wo.loc[ wo['Priority Description'] == priority, 'Work Order Number' ].count().item())
        for raisedYear in wo['raisedYear'].unique():
            val = wo.loc[ (wo['raisedYear'] == raisedYear) & (wo['Priority Description'] == priority), 'Work Order Number' ].count().item()
            output[priority][int(raisedYear)] = int(val)
    return output

@router.get('/WO_jobType_List')
def WO_jobType_List():
    return list(wo['Job Type Description'].unique())

@router.get('/WO_raised_byJobTypes')
def WO_raised_byJobTypes():
    output = {}
    for jobType in wo['Job Type Description'].unique():
        output[jobType] = {}
        output[jobType]['total'] = int(wo.loc[ wo['Job Type Description'] == jobType, 'Work Order Number' ].count().item())
        for raisedYear in wo['raisedYear'].unique():
            val = wo.loc[ (wo['raisedYear'] == raisedYear) & (wo['Job Type Description'] == jobType), 'Work Order Number' ].count().item()
            output[jobType][int(raisedYear)] = int(val)
    return output

@router.get('/WO_status_List')
def WO_status_List():
    return list(wo['Work Order Status Description'].unique())

@router.get('/WO_raised_status')
def WO_raised_status():
    output = {}
    for status in wo['Work Order Status Description'].unique():
        output[status] = {}
        output[status]['total'] = int(wo.loc[ wo['Work Order Status Description'] == status, 'Work Order Number' ].count().item())
        for raisedYear in wo['raisedYear'].unique():
            val = wo.loc[ (wo['raisedYear'] == raisedYear) & (wo['Work Order Status Description'] == status), 'Work Order Number' ].count().item()
            output[status][int(raisedYear)] = int(val)
    return output

@router.get('/WO_raised_byAssets')
def WO_raised_byAssets():
    return byAssets(wo.loc[wo['raisedYear']==2023, ['Asset ID', 'Work Order Number']].groupby('Asset ID').count(), 'raised number')



