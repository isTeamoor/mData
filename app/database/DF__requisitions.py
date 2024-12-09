import pandas as pd
from .impo import requisitions, requisitionItems, approvalPath, contactID, uom
from .impo import assetIDcatalogID, catalogueInfo


### 1. Merge reqlines & requisitions
requisitions = requisitions.merge(approvalPath, how='left', on='Approval Path ID')

requisitionItems = requisitionItems.merge(uom, how='left', on='UOMID')
requisitionItems = requisitionItems.merge(assetIDcatalogID, how='left', on='Asset ID')
requisitionItems = requisitionItems.merge(catalogueInfo[['Catalogue ID','Catalogue Number']], how='left', on='Catalogue ID')
requisitionItems = requisitionItems.merge(contactID[['Contact ID','Created By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))

requisitions = requisitionItems.merge(requisitions, how='outer', on='Requisition ID')




### 2. Prepare dataFrame
requisitions = requisitions.loc [ requisitions['Cancelled Date Time'].isna() ]

requisitions = requisitions.loc[ ~(requisitions['Requisition Line Description'].isna()) ]
requisitions = requisitions.loc[ requisitions['Requisition Line Description'] != '/' ]

requisitions.fillna({'Approval Path Name':'undefined',
                     'Requisition Description':'undefined',
                     'UOMDescription':'undefined'}, inplace=True)

requisitions = requisitions.sort_values(by='Requisition Number', ascending=True)


requisitions['Raised Date Time'] = pd.to_datetime(requisitions['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['raisedYear']  = requisitions['Raised Date Time'].dt.year
requisitions['raisedMonth'] = requisitions['Raised Date Time'].dt.month

requisitions['Required By Date Time'] = pd.to_datetime(requisitions['Required By Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['requiredYear']  = requisitions['Required By Date Time'].dt.year
requisitions['Required Month'] = requisitions['Required By Date Time'].dt.month


requisitions['Total Expected Price'] = requisitions['Requisitioned Quantity'] * requisitions['Expected Purchase Price']




### 3. Фильтр на maintenance
maintenance_ApprovalPath = ['Maintenance','Routine Maintenance Department',
                            'SLU Default','PWU Default', 
                            'CofE department','CofE','CofE (Insul/Scaff)',
                            'Contract Services Deparment',
                            'Material Control Department',
                            'Turnaround'] #Localization
requisitions = requisitions.loc [ requisitions['Approval Path Name'].isin(maintenance_ApprovalPath)]

requisitions = requisitions.loc[ ~(requisitions['Requisition Number'].isin([763,839,842,845,1267,1326])) ] #old unused TAR requisitions


### 4. Производим замену управляющих символов в каждом значении столбца с помощью регулярного выражения
requisitions['Requisition Line Description'] = requisitions['Requisition Line Description'].replace({'\x02': ' '}, regex=True)




### 5. Ready dataFrame
requisitions.rename(columns={
            'Requisition Line Description':'Item',
            'requiredYear':'Required Year',
            'Required Month':'Required Month',
            'UOMDescription':'uom',
            'Expected Purchase Price':'Expected Price per unit, usd',
            'Total Expected Price':'Summary Expected Cost, usd'
            }, inplace=True )

requisitions = requisitions[['Item','Requisition Description','Approval Path Name','Created By',
 'Requisitioned Quantity', 'uom', 'Expected Price per unit, usd','Summary Expected Cost, usd',
 'Requisition Number', 'Required Year', 'Required Month', 'raisedYear', 'raisedMonth', 'Catalogue Number']]


