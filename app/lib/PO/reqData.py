import pandas as pd
from pathlib import Path
import os




### 1. Получение пути к папке reqs, которая находится выше скрипта
script_path = Path(__file__).resolve()
folder = script_path.parent.parent.parent.parent / 'reqs'
  



### 2. Использует папку reqs в каталоге /mData/
def divide_source(df):
    src = df.copy()
    svod = pd.DataFrame()


    ### Define template
    src[['Contract №', 'Contract date', 'Currency (usd/uzs/eur/rub)', 'Actual price per unit', 'Actual quantity']] = ''

    src = src[['Requisition Number','Item','Requisitioned Quantity','uom','Contract №','Contract date','Currency (usd/uzs/eur/rub)','Actual price per unit',
                'Actual quantity','Approval Path Name','Created By','Required Year','Required Month','Requisition Description','Expected Price per unit, usd',
                'Summary Expected Cost, usd','raisedYear','raisedMonth', 'Catalogue Number']]




    ### Разделение df Requisitions на группы по номеру requisition
    for reqN, group in src.groupby('Requisition Number'):

        group.reset_index(inplace=True, drop=False)
        group.drop(columns=['index'], inplace=True)


        ### 1. Если это новый reqN, то создает новый файл в папке reqs и добавляет инфу в svod
        if f'{reqN}.xlsx' not in os.listdir(folder):
            print(f'new reqNumber: {reqN}')
            group.to_excel(f'reqs/{reqN}.xlsx', index=False)
            svod = pd.concat([svod, group], ignore_index=True)
            
        ### 2. Если такой reqN уже существует:
        else:
            ### 2.1 Загружает этот файл xlsx
            orig = pd.read_excel(f'{folder}/{reqN}.xlsx')


            ### 2.2 Перебор всех строк в reqN группе
            for i, row in group.iterrows():

                # Проверка существует ли данный item в загруженном xlsx файле
                check = orig.loc[ 
                    (orig['Catalogue Number'] == row['Catalogue Number']) &
                    (orig['Requisitioned Quantity'] == row['Requisitioned Quantity']) &
                    (orig['Expected Price per unit, usd'] == row['Expected Price per unit, usd'])
                 ]
                
                # Если не найден, то добавляет в загруженный xlsx файл новый элемент и заново генерирует xlsx файл
                if check.size == 0:
                    newItem = {}

                    for field in row.index:
                        newItem[field] = row[field]

                    newItem = pd.DataFrame(newItem, index=[0])
                    orig = pd.concat([orig, newItem]).reset_index(drop=True)

                    print(f'new  item in req #{reqN}: \n', newItem)
                    orig.to_excel(f'reqs/{reqN}.xlsx', index=False) 
            
            ### 3. Заполнение инфы из модернизированного загруженного xlsx файла в svod
            svod = pd.concat([svod, orig], ignore_index=True)



    svod.to_excel('svod.xlsx', index=False)


    
