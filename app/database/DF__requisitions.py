import pandas as pd
from .impo import requisitions, requisitionItems, contactID, approvalPath, uom
from .impo import assetIDcatalogID, catalogueInfo



requisitions = requisitions.merge(contactID[['Contact ID','Requisitioned By']], how='left', left_on='Requisitioned By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(contactID[['Contact ID','Created By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(approvalPath, how='left', on='Approval Path ID')


requisitionItems = requisitionItems.merge(uom, how='left', on='UOMID')
requisitionItems = requisitionItems.merge(contactID[['Contact ID','Requisition line By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitionItems = requisitionItems.merge(assetIDcatalogID, how='left', on='Asset ID')
requisitionItems = requisitionItems.merge(catalogueInfo[['Catalogue ID','Catalogue Number']],    how='left', on='Catalogue ID')

requisitions = requisitionItems.merge(requisitions, how='outer', on='Requisition ID')
requisitions['Total Expected Price'] = requisitions['Requisitioned Quantity'] * requisitions['Expected Purchase Price']




requisitions = requisitions.loc [ requisitions['Cancelled Date Time'].isna() ]
requisitions.fillna({'Approval Path Name':'undefined'}, inplace=True)


### Exception old unused TAR requisitions. Must be cancelled in CMMS by Ulugbek Hamroyev
requisitions = requisitions.loc[ ~(requisitions['Requisition Number'].isin([763,839,842,845,1267,1326])) ]
###########################################################################################################




requisitions['Raised Date Time'] = pd.to_datetime(requisitions['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['raisedYear']  = requisitions['Raised Date Time'].dt.year
requisitions['raisedMonth'] = requisitions['Raised Date Time'].dt.month

requisitions['Required By Date Time'] = pd.to_datetime(requisitions['Required By Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['requiredYear']  = requisitions['Required By Date Time'].dt.year
requisitions['requiredMonth'] = requisitions['Required By Date Time'].dt.month




maintenance_ApprovalPath = ['SLU Default', 'PWU Default', 'Maintenance','CofE department','Routine Maintenance Department',
    'CofE', 'Material Control Department', 'Turnaround','Contract Services Deparment', 'CofE (Insul/Scaff)']
requisitions = requisitions.loc [ requisitions['Approval Path Name'].isin(maintenance_ApprovalPath)]



requisitions['mergeNumber'] = ''
for RequisitionNumber, group in requisitions.groupby('Requisition Number'):
    counter = 0
    for i, row in group.iterrows():
        requisitions.loc[ i, 'mergeNumber'] = str(RequisitionNumber) + "-" + str(counter)
        counter += 1


requisitions = requisitions.sort_values(by=['Requisition Number', 'mergeNumber'], ascending=[True, True])

requisitions = requisitions.loc[ ~(requisitions['Requisition Line Description'].isna()) ]
requisitions = requisitions.loc[ requisitions['Requisition Line Description'] != '/' ]

requisitions.fillna({'Requisition Description':'undefined',
                     'UOMDescription':'undefined',}, inplace=True)


# Производим замену управляющих символов в каждом значении столбца с помощью регулярного выражения
requisitions['Requisition Line Description'] = requisitions['Requisition Line Description'].replace({'\x02': ' '}, regex=True)


requisitions = requisitions[['Requisition Line Description','Requisition Description','Approval Path Name','Created By',
 'Requisitioned Quantity', 'UOMDescription', 'Expected Purchase Price','Total Expected Price',
 'Requisition Number', 'requiredYear', 'requiredMonth', 'raisedYear', 'raisedMonth', 'Catalogue Number']] #'mergeNumber','Completed Date Time',
