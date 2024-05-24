import pandas as pd
from pathlib import Path
import os

### Получение пути к папке reqs, которая находится выше скрипта
script_path = Path(__file__).resolve()
folder = script_path.parent.parent.parent.parent / 'reqs'
  



def divide_source(df):
    src = df.copy()

    src.rename(columns={
            'Requisition Line Description':'Item',
            'requiredYear':'Required Year',
            'requiredMonth':'Required Month',
            'UOMDescription':'uom',
            'Expected Purchase Price':'Expected Price per unit, usd',
            'Total Expected Price':'Summary Expected Cost, usd'
            }, inplace=True )
    src[['Contract №', 'Contract date', 'Currency (usd/uzs/eur/rub)', 'Actual price per unit', 'Actual quantity']] = ''

    src = src[['Requisition Number','Item','Requisitioned Quantity','uom','Contract №','Contract date','Currency (usd/uzs/eur/rub)','Actual price per unit',
                'Actual quantity','Approval Path Name','Created By','Required Year','Required Month','Requisition Description','Expected Price per unit, usd',
                'Summary Expected Cost, usd','raisedYear','raisedMonth', 'Catalogue Number']]




    svod = pd.DataFrame()
    

    for reqN, group in src.groupby('Requisition Number'):
        group.reset_index(inplace=True, drop=False)
        group.drop(columns=['index'], inplace=True)

        if f'{reqN}.xlsx' not in os.listdir(folder):
            print(f'new reqNumber: {reqN}')
            group.to_excel(f'reqs/{reqN}.xlsx', index=False)
            svod = pd.concat([svod, group], ignore_index=True)
            

            
        else:
            orig = pd.read_excel(f'{folder}/{reqN}.xlsx')

            for i, row in group.iterrows():
                check = orig.loc[ 
                    (orig['Catalogue Number'] == row['Catalogue Number']) &
                    (orig['Requisitioned Quantity'] == row['Requisitioned Quantity']) &
                    (orig['Expected Price per unit, usd'] == row['Expected Price per unit, usd'])
                 ]
                if check.size == 0:
                    newItem = {}

                    for field in row.index:
                        newItem[field] = row[field]

                    print(f'new  item in req #{reqN}: \n', newItem)
                    newItem = pd.DataFrame(newItem, index=[0])
                    orig = pd.concat([orig, newItem]).reset_index(drop=True)
                    orig.to_excel(f'reqs/{reqN}.xlsx', index=False)
            
            svod = pd.concat([svod, orig], ignore_index=True)
    svod.to_excel('svod.xlsx', index=False)


    
