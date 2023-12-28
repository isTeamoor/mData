from . import calc
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__spares import spares

dataLib = {
    #################################################
    ###-              CC Report for D            -###
    #################################################
    'materialCost_total':{
        'f':calc.fieldTotal_by_year_month, 'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_Priority':{
        'f':calc.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_JobType':{
        'f':calc.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_Discipline':{
        'f':calc.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Department Name', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'WO_raised_number_by_Priority':{
        'f':calc.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count', gen.filters['maintenance']]},
    'WO_raised_number_by_JobType':{
        'f':calc.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count', gen.filters['maintenance']]},
    'WO_raised_number_by_Assets':{
        'f':calc.fieldTotal_by_Assets_year, 'args':[wo, 'raisedYear', 'Work Order ID', 'count', gen.filters['maintenance']]},
    'materialCost_by_Assets':{
        'f':calc.fieldTotal_by_Assets_year, 'args':[spares, 'reservYear', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    
}



def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    #print('Data befor serialisation:\n',data)
    return data