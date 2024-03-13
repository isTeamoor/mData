from . import calc
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__trades import trades
from ...database.DF__budget import budget_cofe_mod

dataLib = {
    #################################################
    ###-                CofE Report              -###
    #################################################
    'WO_raised_number_total':{
        'f':calc.fieldTotal_by_year_month, 'args':[wo.loc[ wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique()) ], 'raisedYear', 'raisedMonth','Work Order ID', 'count']},
    'WO_raised_number_by_Status':{
        'f':calc.coupleFields_by_year_month, 'args':[wo.loc[ wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique()) ], 'raisedYear', 'raisedMonth', 'Work Order Status Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_JobTypes':{
        'f':calc.coupleFields_by_year_month, 'args':[wo.loc[ wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique()) ], 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count']},
    'WO_closed_number_by_JobTypes':{
        'f':calc.coupleFields_by_year_month, 'args':[wo.loc[ (wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique())) & (wo['Work Order Status Description']=='Closed') ], 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_Priority':{
        'f':calc.coupleFields_by_year_month, 'args':[wo.loc[ wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique()) ], 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count']},
    'WO_closed_number_by_Priority':{
        'f':calc.coupleFields_by_year_month, 'args':[wo.loc[ (wo['Work Order Number'].isin( trades.loc[trades['isCofETrade']=='yes', 'Work Order Number'].unique())) & (wo['Work Order Status Description']=='Closed') ], 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count']},
    'Trades_used':{
        'f':calc.coupleFields_by_year_month, 'args':[trades, 'raisedYear', 'raisedMonth', 'Trade Code Description', 'Actual Duration Hours', 'sum', gen.filters['CofE_trades']]},
    'Planed_cost_CofE':{
        'f':calc.fieldTotal_by_year_month, 'args':[budget_cofe_mod, 'year','month', 'value', 'sum']},
    'Actual_cost_labour_CofE':{
        'f':calc.fieldTotal_by_year_month, 'args':[trades, 'raisedYear', 'raisedMonth', 'Actual Cost', 'sum', gen.filters['CofE_trades']]},
    'Actual_cost_material_CofE':{
        'f':calc.fieldTotal_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Actual Cost', 'sum', gen.filters['CofE_spares']]},
}



def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    #print('Data befor serialisation:\n',data)
    return data

'''
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
    '''