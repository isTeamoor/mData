import pandas as pd

contracts = pd.read_excel('Список.xls')

contracts['Дата документа'] = pd.to_datetime(contracts['Дата документа'], format="%d.%m.%Y %H:%M:%S")
contracts['raisedYear']  = contracts['Дата документа'].dt.year
contracts['raisedMonth'] = contracts['Дата документа'].dt.month

contracts['Номер'] = contracts['Номер'].astype(int)

contracts['Requisition'] = 'n/a'

contracts['isMaintenance'] = 'no'

contracts['isMaintenance'].fillna('undefined', inplace=True)
contracts['№ договора'].fillna('undefined', inplace=True)

contracts = contracts.sort_values(by='Дата документа')

contracts = contracts[['Номер','Дата документа','№ договора','Requisition','isMaintenance','Инициатор','Сумма','Валюта','Контрагент']]

reqLib = [
    {1978:1101}
]

for i in reqLib:
    for key, value in i.items():
        contracts.loc[ contracts['Номер'] == key, 'Requisition' ] = value
        
contracts.to_excel('contracts.xlsx', index=False)



