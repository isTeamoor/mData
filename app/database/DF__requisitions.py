import pandas as pd
from .impo import requisitions, requisitionItems, contactID, approvalPath, uom



requisitions = requisitions.merge(contactID[['Contact ID','Requisitioned By']], how='left', left_on='Requisitioned By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(contactID[['Contact ID','Created By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(approvalPath, how='left', on='Approval Path ID')

requisitionItems = requisitionItems.merge(uom, how='left', on='UOMID')
requisitionItems = requisitionItems.merge(contactID[['Contact ID','Requisition line By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))

requisitions = requisitionItems.merge(requisitions, how='outer', on='Requisition ID')
requisitions['Total Expected Price'] = requisitions['Requisitioned Quantity'] * requisitions['Expected Purchase Price']




requisitions = requisitions.loc [ requisitions['Cancelled Date Time'].isna() ]




requisitions['Raised Date Time'] = pd.to_datetime(requisitions['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['raisedYear']  = requisitions['Raised Date Time'].dt.year
requisitions['raisedMonth'] = requisitions['Raised Date Time'].dt.month

requisitions['Required By Date Time'] = pd.to_datetime(requisitions['Required By Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['requiredYear']  = requisitions['Required By Date Time'].dt.year
requisitions['requiredMonth'] = requisitions['Required By Date Time'].dt.month



requisitions = requisitions.loc [ requisitions['raisedYear']==2023]
requisitions = requisitions.loc [ requisitions['requiredYear']==2023]


maintenanceApprovalPath = ['SLU Default', 'PWU Default', 'Maintenance', 'CofE department', 'Routine Maintenance Department', 'CofE', 'Civil Department', 
                           'Material Control Department', 'Turnaround', 'Contract Services Deparment', 'CofE Default','Civil']
requisitions = requisitions.loc [ requisitions['Approval Path Name'].isin(maintenanceApprovalPath)]


requisitions['mergeNumber'] = ''
for RequisitionNumber, group in requisitions.groupby('Requisition Number'):
    counter = 0
    for i, row in group.iterrows():
        requisitions.loc[ i, 'mergeNumber'] = str(RequisitionNumber) + "-" + str(counter)
        counter += 1


requisitions = requisitions[['Requisition Line Description','Requisition Description','Approval Path Name',
 'Requisition line By','Requisitioned By','Created By',
 'Requisitioned Quantity', 'UOMDescription', 'Expected Purchase Price','Total Expected Price',
 'Requisition Number','mergeNumber', 'requiredYear', 'requiredMonth', 'raisedYear', 'raisedMonth', 'Completed Date Time',]]