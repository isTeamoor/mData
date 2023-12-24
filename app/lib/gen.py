import pandas as pd
import numpy as np


def filterDF(df,  filters = 'all' ):
    if (filters == 'all') or (not filters):
        return df
    
    def conditionString(filters):
        conditions = ''
        for item in filters:
            if type(item)==dict:
                conditions += f'(   `{ item["field"] }` {item["operator"]} {item["value"]}   )'
            if type(item)==str:
                conditions += f" {item} "
            if type(item)==list:
                conditions += f'( {conditionString(item)} )'
        return conditions
    
    print(conditionString(filters))
    return df.query(conditionString(filters))


name = "Mansur Xasanov Tulqin o'g'li"
filters = {
    'maintenance':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
    ],
    



    'notClosedWO':[{'field':'Work Order Status Description', 'operator':'not in', 'value':"['Closed', 'Cancelled']"}],
    'rmpd':[
        {"field":'isRMPD', "operator":"==", "value":"'yes'"}, 
        "&", 
        {"field":'Reserved By', "operator":"!=", "value":"'Mirjakhon Toirov'"}, 
        "&",
        {"field":'Reserved By', "operator":"!=", "value":"'Bobur Aralov'"}
    ],
    'cofe':[ 
        {"field":'Reserved By', "operator":"==", "value":"'Mirjakhon Toirov'"},
    ],
    
    'maintenance-planerExample':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Created By', "operator":"==", "value":f'"{str(name)}"'},
    ],
    'maintenance-PriorityExample':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Priority Description', "operator":"==", "value":"'EMERGENCY-24hr'"},
    ],
    'maintenance_closed':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
    ],
    'maintenance-planerExample_closed':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
        "&",
        {"field":'Created By', "operator":"==", "value":f'"{str(name)}"'},
    ],
    'maintenance-PriorityExample_closed':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
        "&",
        {"field":'Priority Description', "operator":"==", "value":"'EMERGENCY-24hr'"},
    ],
    'maintenance-PriorityExample_closed':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
        "&",
        {"field":'Priority Description', "operator":"==", "value":"'EMERGENCY-24hr'"},
    ],
    'maintenance-1planer-1priority':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Priority Description', "operator":"==", "value":"'EMERGENCY-24hr'"},
        "&",
        {"field":'Created By', "operator":"==", "value":f'"{str(name)}"'},
    ],
    'maintenance-1planer-1priority_closed':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
        "&",
        {"field":'Priority Description', "operator":"==", "value":"'EMERGENCY-24hr'"},
        "&",
        {"field":'Created By', "operator":"==", "value":f'"{str(name)}"'},
        "&",
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
    ],
}

