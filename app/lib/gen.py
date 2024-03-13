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


filters = {
    'maintenance':[
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
    ],
    'CofE_trades':[
        {"field":'Trade Code Description', "operator":"in", "value":"['WELDER','INSULATE','Scaffolder','PIPING JUNIOR','Metrology Engineer','HVAC ENG','JET TECH','SUPV PSV','Fire and Gas engineer','WELD ENG','Field instrumentation Junior technician','Valve technician','Workshop machinist junior','F&G Supervisor','HVAC Supervisor','Piping Engineer','Work Shop machinist']"},
    ], 
    'CofE_spares':[
        {"field":'Reserved By', "operator":"==", "value":"'Mirjakhon Toirov'"},
    ], 
}

