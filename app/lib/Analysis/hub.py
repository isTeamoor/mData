from . import calc
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__spares import spares
from ...database.DF__trades import trades
from ...database.DF__requisitions import requisitions


filter_lib ={
    'maintenance':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
    ],
    'maintenance_reserv_in_2024':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'reservYear', "operator":"==", "value":"2024"}
    ],
    'maintenance_reserv_in_2023':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'reservYear', "operator":"==", "value":"2023"}
    ],
    'maintenance_raised_in_2024':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'raisedYear', "operator":"==", "value":"2024"}
    ],
    'maintenance_raised_in_2023':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'raisedYear', "operator":"==", "value":"2023"}
    ],
    'maintenance_closed_WO':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
    ],
    'maintenance_open_WO':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"!=", "value":"'Closed'"},
        "&",
        {"field":'Work Order Status Description', "operator":"!=", "value":"'Cancelled'"},
    ],
    'CofE_trades':[
        {"field":'Trade Code Description', "operator":"in", "value":"['WELDER','INSULATE','Scaffolder','PIPING JUNIOR','Metrology Engineer','HVAC ENG','JET TECH','SUPV PSV','Fire and Gas engineer','WELD ENG','Field instrumentation Junior technician','Valve technician','Workshop machinist junior','F&G Supervisor','HVAC Supervisor','Piping Engineer','Work Shop machinist']"},
    ], 
    'CofE_spares':[
        {"field":'Reserved By', "operator":"==", "value":"'Mirjakhon Toirov'"},
    ], 
}


dataLib = {
    #################################################
    ###-          Requisitions Analysis          -###
    #################################################
    'rq_raised_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[requisitions, 'raisedYear', 'Total Expected Price', 'sum']},
    'rq_raised_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[requisitions, 'raisedYear','raisedMonth', 'Total Expected Price', 'sum']},
    'rq_required_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[requisitions, 'requiredYear', 'Total Expected Price', 'sum']},
    'rq_required_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[requisitions, 'requiredYear','requiredMonth', 'Total Expected Price', 'sum']},
    'rq_raised_Departments_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[requisitions, 'raisedYear','Approval Path Name', 'Total Expected Price', 'sum']},
    'rq_required_Departments_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[requisitions, 'requiredYear','Approval Path Name', 'Total Expected Price', 'sum']},
    'rq_raised_Departments_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[requisitions, 'raisedYear','raisedMonth','Approval Path Name', 'Total Expected Price', 'sum']},
    'rq_required_Departments_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[requisitions, 'requiredYear','requiredMonth','Approval Path Name', 'Total Expected Price', 'sum']},

    #################################################
    ###-              Spares Analysis            -###
    #################################################
    'sp_reserved_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[spares, 'reservYear', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_monthly':{
        'f':calc.fieldTotal_monthly, 
        'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Priority Description', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Job Type Description', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Department Name', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Department Name', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[spares, 'reservYear', 'Short Department Name', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[spares, 'reservYear', 'reservMonth', 'Short Department Name', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[spares, 'reservYear', 'Actual Cost', 'sum', filter_lib['maintenance']]},
    'sp_reserved_Assets_sorted_2023':{
        'f':calc.sorted_matcost_assets, 
        'args':[spares, filter_lib['maintenance_reserv_in_2023']]},
    'sp_reserved_Assets_sorted_2024':{
        'f':calc.sorted_matcost_assets, 
        'args':[spares, filter_lib['maintenance_reserv_in_2024']]},
    #################################################
    ###-            Work Orders Analysis         -###
    #################################################
    'wo_raised_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_closed_yearly':{
        'f':calc.fieldTotal_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', filter_lib['maintenance_closed_WO']]},
    
    'wo_raised_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Priority Description', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Priority_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Priority Description', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    'wo_raised_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Priority_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},

    'wo_raised_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Job Type Description', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_JobType_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Job Type Description', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    'wo_raised_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_JobType_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    
    'wo_raised_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Department Name', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Discipline_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Department Name', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    'wo_raised_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Department Name', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Discipline_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Department Name', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},

    'wo_raised_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Short Department Name', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Department_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Short Department Name', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    'wo_raised_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Department_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},

    'wo_raised_Planer_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Created By', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Planer_yearly':{
        'f':calc.coupleFields_yearly, 
        'args':[wo, 'raisedYear', 'Created By', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},
    'wo_raised_Planer_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order Number', 'count', filter_lib['maintenance']]},
    'wo_open_Planer_monthly':{
        'f':calc.coupleFields_monthly, 
        'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]},

    'wo_raised_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', filter_lib['maintenance']]},    
    'wo_open_Assets_yearly':{
        'f':calc.fieldTotal_Assets_yearly, 
        'args':[wo, 'raisedYear', 'Work Order Number', 'count', filter_lib['maintenance_open_WO']]}, 
    
    'wo_raised_Assets_sorted_2023':{
        'f':calc.sorted_woRaised_assets, 
        'args':[wo, filter_lib['maintenance_raised_in_2023']]},
    'wo_raised_Assets_sorted_2024':{
        'f':calc.sorted_woRaised_assets, 
        'args':[wo, filter_lib['maintenance_raised_in_2024']]},
}




def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    #print('Data befor serialisation:\n',data)
    return data