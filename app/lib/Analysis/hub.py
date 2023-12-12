from . import WO
from ...lib import gen
from ...database.DF__wo import wo

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
    'WO_notClosed_number_Overall'         :{'f':WO.fieldTotal, 'args':[wo, 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_year'         :{'f':WO.fieldTotal_by_year, 'args':[wo, 'raisedYear','Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_year_month'   :{'f':WO.fieldTotal_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Assets'       :{'f':WO.fieldTotal_by_Assets_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Work Order Number', 'count', gen.filters['notClosedWO']]},

    'WO_notClosed_number_by_Priority_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Priority Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_JobType_by_year'    :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Job Type Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Division_by_year'   :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Department Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Department_by_year' :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Short Department Name', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Planer_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','Created By', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_isRMPD_by_year'     :{'f':WO.coupleFields_by_year, 'args':[wo, 'raisedYear','isRMPD', 'Work Order ID', 'count', gen.filters['notClosedWO']]},

    'WO_notClosed_number_by_Priority_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Priority Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_JobType_by_year_month'    :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Job Type Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Division_by_year_month'   :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Department Description', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Department_by_year_month' :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Short Department Name', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_Planer_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'Created By', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
    'WO_notClosed_number_by_isRMPD_by_year_month'     :{'f':WO.coupleFields_by_year_month, 'args':[wo, 'raisedYear', 'raisedMonth', 'isRMPD', 'Work Order ID', 'count', gen.filters['notClosedWO']]},
}




def getVal(sectionName):
    data = dataLib[sectionName]['f'](  *dataLib[sectionName]['args']  )
    print('Data befor serialisation:\n',data)
    return data