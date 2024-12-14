from . import calc
from ...lib.gen import flt
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__trades import trades
from ...database.DF__requisitions import requisitions


dataLib = {
    ### Requisitions Analysis
    #1. Raised requisitions
    'rq_raised_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[requisitions, 'raisedYear', 'Summary Expected Cost, usd', 'sum']},
    'rq_raised_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[requisitions, 'raisedYear','raisedMonth', 'Summary Expected Cost, usd', 'sum']},
    'rq_raised_Departments_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[requisitions, 'raisedYear','Approval Path Name', 'Summary Expected Cost, usd', 'sum']},
    'rq_raised_Departments_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[requisitions, 'raisedYear','raisedMonth','Approval Path Name', 'Summary Expected Cost, usd', 'sum']},
    'rq_raised_Planer_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[requisitions, 'raisedYear','Created By', 'Summary Expected Cost, usd', 'sum']},
    #2. Required requisitions
    'rq_required_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[requisitions, 'Required Year', 'Summary Expected Cost, usd', 'sum']},
    'rq_required_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[requisitions, 'Required Year','Required Month', 'Summary Expected Cost, usd', 'sum']},
    'rq_required_Departments_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[requisitions, 'Required Year','Approval Path Name', 'Summary Expected Cost, usd', 'sum']},
    'rq_required_Departments_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[requisitions, 'Required Year','Required Month','Approval Path Name', 'Summary Expected Cost, usd', 'sum']},



    ### Spares Analysis
    #1. Spares cost total
    'sp_reserved_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[spares, 'reservYear', 'Actual Cost', 'sum', [flt['maintenance']] ]},
    'sp_reserved_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', [flt['maintenance']]]},
    
    'sp_reserved_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Priority Description', 'Actual Cost', 'sum', [flt['maintenance']]]},
    'sp_reserved_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', [flt['maintenance']]]},
    
    'sp_reserved_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Job Type Description', 'Actual Cost', 'sum', [flt['maintenance']]]},
    'sp_reserved_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', [flt['maintenance']]]},
    
    'sp_reserved_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Department Name', 'Actual Cost', 'sum', [flt['maintenance']]]},
    'sp_reserved_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Department Name', 'Actual Cost', 'sum', [flt['maintenance']]]},
    
    'sp_reserved_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Short Department Name', 'Actual Cost', 'sum', [flt['maintenance']]]},
    'sp_reserved_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Short Department Name', 'Actual Cost', 'sum', [flt['maintenance']]]},
    
    #2. Spares cost by assets
    'sp_reserved_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[spares, 'reservYear', 'Actual Cost', 'sum', [flt['maintenance']]]},
    'sp_reserved_Assets_sorted_2024':{
        'f':calc.sorted_matcost_assets, 
        'args':[spares, [ flt['maintenance'],"&",flt['reserved_2024'] ]  ]},



    ### Work Orders Analysis

    #1. Raised WO
    'wo_raised_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Priority Description', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Job Type Description', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Department Name', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Department Name', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Short Department Name', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Planer_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Created By', 'Work Order Number', 'count', [flt['maintenance']]]},
    'wo_raised_Planer_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order Number', 'count', [flt['maintenance']]]},

    #2. Not Closed WO
    'wo_open_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ] ]},
    'wo_open_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Priority Description', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Job Type Description', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Department Name', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Department Name', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Short Department Name', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Planer_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Created By', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},
    'wo_open_Planer_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]},

    #3. WO by assets
    'wo_raised_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', [flt['maintenance']]]},    
    'wo_open_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', [ flt['maintenance'],"&",flt['notclosed'],"&",flt['notcancelled'] ]]}, 
    
    'wo_raised_Assets_sorted_2024':{
        'f':calc.sorted_woRaised_assets, 
        'args':[wo, [ flt['maintenance'],"&",flt['raised_2024'] ] ]},
}




def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    #print('Data befor serialisation:\n',data)
    return data