import pandas as pd
from . import DF__spares
from . import impo



transactions = impo.transactions.merge(impo.catalogInfo, left_on='Catalogue Asset ID', right_on='Asset ID', how='left')




transactions['Catalogue Transaction Date Time'] = pd.to_datetime(transactions['Catalogue Transaction Date Time'], format="%d/%m/%Y %H:%M:%S %p")
transactions['transactYear']  = transactions['Catalogue Transaction Date Time'].dt.year
transactions['transactMonth'] = transactions['Catalogue Transaction Date Time'].dt.month
transactions['transactDay']   = transactions['Catalogue Transaction Date Time'].dt.day




transactions['Quantity'] = transactions['Quantity'].map(lambda x: -x)

transactions['Material Code'] = transactions['Material Code'].astype(str)
transactions  = transactions.loc [ (transactions['Material Code'].str.len() != 5) ]
transactions['Material Code'] = transactions['Material Code'].map(lambda x: x.strip()[-4:])




spares = DF__spares.spares[['reservYear','reservMonth', 'Reservation Number','Work Order Number', 'Work Order Status Description', 'Short Department Name', 'isRMPD', 'isMaintenance',
                            'Asset Description', 'Asset Number','Reserved By', 'closedYear', 'closedMonth','Actual Quantity', 'Estimated Unit Cost', 'Estimated Quantity','Work Order Spare ID']]
transactions = transactions.merge(spares, how='left', on='Work Order Spare ID')



