import pandas as pd
from . import impo
from .DF__spares import spares

spares = spares[['Work Order Spare ID','Work Order Number', 'Work Order Status Description', 'Priority Description', 'Department Name', 'Department Description', 'Asset Description', 'Asset Number', 'Account Code', 'Account Code Description',]]
spares = spares.rename(columns={'Account Code Description':'Account Code Description (from WO)', 'Account Code': 'Account Code (from WO)',})


requisitions = impo.requisitions
items        = impo.requisitItems
uom          = impo.uom
contactID    = impo.contactID[['Contact ID', 'Requisitioned By', 'Completed By','Cancelled By','Created By']]
accountCodes = impo.accountCodes
approvalPath = impo.approvalPath
assets       = impo.assets


reqItems = items.merge(requisitions, on='Requisition ID', how='outer' )
reqItems = reqItems.merge(spares,           on='Work Order Spare ID',           how='left')
reqItems = reqItems.merge(approvalPath,  on='Approval Path ID', how='left')
reqItems = reqItems.merge(accountCodes, on='Account Code ID',         how='left')
reqItems = reqItems.merge(contactID[['Contact ID', 'Requisitioned By']],     left_on='Requisitioned By Contact ID', right_on='Contact ID',how='left')
reqItems = reqItems.merge(contactID[['Contact ID', 'Completed By']],     left_on='Completed By Contact ID', right_on='Contact ID',how='left', suffixes=['','_delete'])
reqItems = reqItems.merge(contactID[['Contact ID', 'Cancelled By']],     left_on='Cancelled By Contact ID', right_on='Contact ID',how='left', suffixes=['','_delete'])
reqItems = reqItems.merge(contactID[['Contact ID', 'Created By']],     left_on='Created By Contact ID', right_on='Contact ID',how='left', suffixes=['','_delete'])
reqItems = reqItems.merge(uom, on='UOMID',    how='left')


reqItems['Required By Date Time'] = pd.to_datetime(reqItems['Required By Date Time'], format="%d/%m/%Y %H:%M:%S %p")
reqItems['requiredYear']  = reqItems['Required By Date Time'].dt.year
reqItems['requiredMonth'] = reqItems['Required By Date Time'].dt.month

reqItems['Raised Date Time'] = pd.to_datetime(reqItems['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
reqItems['raisedYear']  = reqItems['Raised Date Time'].dt.year
reqItems['raisedMonth'] = reqItems['Raised Date Time'].dt.month




reqItems = reqItems[['Requisition Number','Requisition Description','Approval Path Name','Created By',	'Requisitioned By',	'Requisition Line Description',	'Requisitioned Quantity','UOMDescription',
 	                'Expected Purchase Price',	'raisedYear','raisedMonth',	'requiredYear', 'requiredMonth',	'Completed Date Time',	'Completed By',	'Cancelled Date Time',	'Cancelled By',
                    'Account Code Name', 'Account Code Description',	'Comment','User Defined Text Box','Work Order Number','Work Order Status Description','Priority Description',
                    'Department Name',	'Department Description', 'Asset Description',	'Asset Number',	'Account Code (from WO)',	'Account Code Description (from WO)']]

