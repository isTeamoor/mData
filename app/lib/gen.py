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

flt = {
    'maintenance':
        {"field":'isMaintenance', "operator":"==", "value":"'yes'"},
    'reserved_2023':
        {"field":'reservYear', "operator":"==", "value":"2023"},
    'reserved_2024':
        {"field":'reservYear', "operator":"==", "value":"2024"},
    'raised_2023':
        {"field":'raisedYear', "operator":"==", "value":"2023"},
    'raised_2024':
        {"field":'raisedYear', "operator":"==", "value":"2024"},

    'closed':
        {"field":'Work Order Status Description', "operator":"==", "value":"'Closed'"},
    'notclosed':
        {"field":'Work Order Status Description', "operator":"!=", "value":"'Closed'"},
    'cancelled':
        {"field":'Work Order Status Description', "operator":"==", "value":"'Cancelled'"},
    'notcancelled':
        {"field":'Work Order Status Description', "operator":"!=", "value":"'Cancelled'"},

    'U&O':
        {"field":'Short Department Name', "operator":"==", "value":"'U&O'"},

}