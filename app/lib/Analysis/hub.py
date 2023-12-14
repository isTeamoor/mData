from . import WO
from ...lib import gen
from ...database.DF__wo import wo
from ...database.DF__spares import spares

dataLib = {
    #################################################
    ###-   Total Raised Work Orders Statistics   -###
    #################################################
    'WO_raised_number_Overall'         :{'f':WO.fieldTotal, 'args':[wo, 'Work Order ID', 'count']},
    'WO_raised_number_by_year'         :{'f':WO.fieldTotal_by_year, 'args':[wo, 'raisedYear','Work Order ID', 'count']},
    'WO_raised_number_by_year_month'   :{'f':WO.fieldTotal_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order ID', 'count']},
    'WO_raised_number_by_Assets'       :{'f':WO.fieldTotal_by_Assets_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order Number', 'count']},

    'WO_raised_number_by_Priority_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Priority Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_JobType_by_year'    :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Job Type Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_Division_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Department Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_Department_by_year' :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Short Department Name', 'Work Order ID', 'count']},
    'WO_raised_number_by_Planer_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Created By', 'Work Order ID', 'count']},
    'WO_raised_number_by_isRMPD_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','isRMPD', 'Work Order ID', 'count']},
    'WO_raised_number_by_Status_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Work Order Status Description', 'Work Order ID', 'count']},

    'WO_raised_number_by_Priority_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_JobType_by_year_month'    :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_Division_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Department Description', 'Work Order ID', 'count']},
    'WO_raised_number_by_Department_by_year_month' :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order ID', 'count']},
    'WO_raised_number_by_Planer_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order ID', 'count']},
    'WO_raised_number_by_isRMPD_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'isRMPD', 'Work Order ID', 'count']},
    'WO_raised_number_by_Status_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order Status Description', 'Work Order ID', 'count']},
    
    ###############################################
    ###-   Not Closed Work Orders Statistics   -###
    ###############################################
    #'WO_notClosed_number_Overall'         :{'f':WO.fieldTotal, 'args':[wo, 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_year'         :{'f':WO.fieldTotal_by_year, 'args':[wo, 'raisedYear','Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_year_month'   :{'f':WO.fieldTotal_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Assets'       :{'f':WO.fieldTotal_by_Assets_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order Number', 'count', gen.filters['notClosedWO']]},

    #'WO_notClosed_number_by_Priority_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Priority Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_JobType_by_year'    :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Job Type Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Division_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Department Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Department_by_year' :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Short Department Name', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Planer_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Created By', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_isRMPD_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','isRMPD', 'Work Order ID', 'count', gen.filters['notClosedWO']]},

    #'WO_notClosed_number_by_Priority_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_JobType_by_year_month'    :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Division_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Department Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Department_by_year_month' :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_Planer_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    #'WO_notClosed_number_by_isRMPD_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'isRMPD', 'Work Order ID', 'count', gen.filters['notClosedWO']]},

    ###############################################
    ###-           Spares Statistics           -###
    ###############################################
    #'Spares_maintenance_raised_by_year'                     :{'f':WO.fieldTotal_by_year, 'args':[spares, 'reservYear','Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_year_month'               :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_Priority_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_JobType_by_year_month'    :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_Division_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Department Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_Department_by_year_month' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_Planer_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    #'Spares_maintenance_raised_by_Assets'                   :{'f':WO.fieldTotal_by_Assets_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Actual Cost', 'sum', gen.filters['maintenance']]},

    #'Spares_maintenance_actual_by_year'                     :{'f':WO.fieldTotal_by_year, 'args':[spares, 'closedYear','Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_year_month'               :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'closedYear', 'closedMonth','Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_Priority_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_JobType_by_year_month'    :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_Division_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Department Description', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_Department_by_year_month' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_Planer_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},
    #'Spares_maintenance_actual_by_Assets'                   :{'f':WO.fieldTotal_by_Assets_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Actual Cost', 'sum', gen.filters['maintenance_spares_actual']]},

    ###############################################
    ###-               СС Report               -###
    ###############################################
    'materialCost_total'   :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total(a)':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'reservYear', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total(a)_planer':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'reservYear', 'Actual Cost', 'sum', gen.filters['maintenance-planerExample']]},
    'materialCost_total(a)_priority':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'reservYear', 'Actual Cost', 'sum', gen.filters['maintenance-PriorityExample']]},
    'materialCost_total_by_Planers' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_JobType' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_Priority' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_Department' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance']]},
    'materialCost_total_by_AccountCodes' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Account Code Description', 'Actual Cost', 'sum', gen.filters['maintenance']]},

    'materialCost_closed'   :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'closedYear', 'closedMonth','Actual Cost', 'sum', gen.filters['maintenance_closed']]},
    'materialCost_closed(a)':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'closedYear', 'Actual Cost', 'sum', gen.filters['maintenance_closed']]},
    'materialCost_closed(a)_planer':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'closedYear', 'Actual Cost', 'sum', gen.filters['maintenance-planerExample_closed']]},
    'materialCost_closed(a)_priority':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'closedYear', 'Actual Cost', 'sum', gen.filters['maintenance-PriorityExample_closed']]},
    'materialCost_closed_by_Planers' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance_closed']]},
    'materialCost_closed_by_JobType' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance_closed']]},
    'materialCost_closed_by_Priority' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance_closed']]},
    'materialCost_closed_by_Department' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance_closed']]},



    'f-emerg_materialCost_total'   :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'reservYear', 'reservMonth','Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total(a)':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'reservYear', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total_by_Planers' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total_by_JobType' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total_by_Priority' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total_by_Department' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},
    'f-emerg_materialCost_total_by_AccountCodes' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'reservYear', 'reservMonth', 'Account Code Description', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority']]},

    'f-emerg_materialCost_closed'   :{'f':WO.fieldTotal_by_year_month, 'args':[spares, 'closedYear', 'closedMonth','Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
    'f-emerg_materialCost_closed(a)':{'f':WO.fieldTotal_by_Assets_year, 'args':[spares, 'closedYear', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
    'f-emerg_materialCost_closed_by_Planers' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Created By', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
    'f-emerg_materialCost_closed_by_JobType' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Job Type Description', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
    'f-emerg_materialCost_closed_by_Priority' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Priority Description', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
    'f-emerg_materialCost_closed_by_Department' :{'f':WO.coupleFields_by_year_month, 'args':[spares, 'closedYear', 'closedMonth', 'Short Department Name', 'Actual Cost', 'sum', gen.filters['maintenance-1planer-1priority_closed']]},
}




def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    #print('Data befor serialisation:\n',data)
    return data