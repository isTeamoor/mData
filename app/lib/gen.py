import pandas as pd
import numpy as np




def filterDF(df,  filters = 'all' ):
    if (filters == 'all') or (not filters):
        return df
    print(filters)
    
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



def getFields(df):
    df = df.fillna(0)
    output = {}
    for column in df.columns:
        output[column] = []
        for item in df[column].unique():
            if type(item) not in [str, float, pd.Timestamp, int]:
                item = item.item()
            if type(item) == str:
                if ' ' in item:
                    item = f'"{item}"'
            output[column].append(item)
    return output