import pandas as pd
import os
from .DF__spares import spares
from .impo import transactions, assetIDcatalogID, stockOnHand, stockReserved, catalogueInfo, uom



### Переходник: transactions['Catalogue Asset ID'] -> assetIDcatalogID['Asset ID', 'Catalogue ID'] ->... 
transactions = transactions.merge(assetIDcatalogID, how='left', left_on='Catalogue Asset ID', right_on='Asset ID')
transactions = transactions.merge(catalogueInfo,    how='left', on='Catalogue ID')
transactions = transactions.merge(stockOnHand,      how='left', on='Asset ID')
transactions = transactions.merge(stockReserved,    how='left', on='Asset ID')
transactions = transactions.merge(uom,              how='left', on='UOMID')




transactions['Catalogue Transaction Date Time'] = pd.to_datetime(transactions['Catalogue Transaction Date Time'], format="%d/%m/%Y %H:%M:%S %p")
transactions['transactYear']  = transactions['Catalogue Transaction Date Time'].dt.year
transactions['transactMonth'] = transactions['Catalogue Transaction Date Time'].dt.month



transactions['Quantity'] = transactions['Quantity'].map(lambda x: -x) #Issue становятся "положительными", Return to stock "Отрицательными"





transactions.rename(columns={'User Defined Text Box1': 'Material Code'}, inplace=True)

transactions['Material Code'] = transactions['Material Code'].astype(str)


transactions  = transactions.loc [ (transactions['Material Code'].str.len() != 5) ]  # пятизначными обозначаются Initial spare parts

transactions['Material Code'] = transactions['Material Code'].map(lambda x: x.strip()) # удаление пробелов и табуляции

transactions['Material Code'] = transactions['Material Code'].map(lambda x: '0000'+ x if len(x)==1 else '000'+ x if len(x)==2 else '00'+ x if len(x)==3 else '0' + x if len(x)==4 else x[-5:] )



spares = spares[[
'Work Order Spare ID', 'Reservation Number', 'reservYear', 'reservMonth', 'Reserved By', 'isRMPD_planner',
'Work Order Number','Work Order Status Description','raisedYear', 'raisedMonth',
'closedYear', 'closedMonth', 'Short Department Name', 'isRMPD','Created By',
'Is Master Work Order', 'Is Group Work Order', 'Group WO number','Spares Comment','Employee WOSpares', 'Asset Description','Asset Number','Estimated Cost',
]]
transactions = transactions.merge(spares, how='left', on='Work Order Spare ID')





transactions.rename(columns={'Material Code':'Код товара',
                                'Catalogue Description':'Материал',
                                'UOMDescription':'Ед.изм.',
                                'Asset Number':'Объект', 
                                'Short Department Name':'Отдел',
                                'Work Order Number':'WO №'}, inplace=True)
transactions = transactions[[
'Catalogue Transaction ID', 'Catalogue Transaction Action Name','transactYear', 'transactMonth',
'Quantity', 'Catalogue Number', 'Код товара', 'Материал','Ед.изм.', 
'Reservation Number', 'reservYear', 'reservMonth', 'Reserved By','isRMPD_planner','Asset Description','Объект',
'WO №', 'Work Order Status Description', 'raisedYear', 'raisedMonth',
'closedYear', 'closedMonth', 'Отдел', 'isRMPD', 'Created By',
'Is Master Work Order', 'Is Group Work Order', 'Group WO number',
'Spares Comment', 'Employee WOSpares', 'Stock On Hand','Total Quantity Reserved',
'Estimated Cost',
]]




