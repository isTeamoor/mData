import pandas as pd
import re
from ..database.DF__requisitions import requisitions



purchs = pd.read_excel('озл.xlsx')

purchs.rename(columns={
    'РЕЕСТР КОНТРАКТОВ':'Contract', 
    'Unnamed: 1':'Date', 
    'Unnamed: 2':'Items', 
    'Unnamed: 3':'Price',
    'Unnamed: 4':'Сurrency', 
    'Unnamed: 5':'Document', 
    'Unnamed: 6':'Initiator', 
    'Unnamed: 7':'Type', 
    'Unnamed: 8':'Origin'}, inplace=True)

purchs = purchs.iloc[1:]




purchs['Document'] = purchs['Document'].fillna('undef')
purchs['Document'] = purchs['Document'].astype(str)

def regexps(row):
    if re.search('Requ', row['Document']) or re.search('PR', row['Document']) or re.search('RP', row['Document']) or re.search('RR', row['Document']):
        for match in re.findall("\d*", row['Document']):
            if match:
                return match
    else:
        if re.findall("^\d\d{,5}\d$", row['Document']):
            return re.findall("^\d\d{,5}\d$", row['Document'])[0]
        
purchs['Requisition Number'] = purchs.apply(regexps, axis=1)


purchs = purchs.loc[ (purchs['Document'].str.contains('ORD') == False)
                   & (purchs['Document'].str.contains('undef') == False)
                   & (purchs['Document'] != '-') ]

purchs['Requisition Number'].fillna(0, inplace=True)
purchs = purchs.loc [ purchs['Requisition Number']!=0 ]
purchs['Requisition Number'] = purchs['Requisition Number'].astype(int)




purchs['RawPrice'] = purchs['Price'].copy()
purchs.loc[ purchs['Price']=='-', 'Price' ] = 0
purchs['Price'] = purchs['Price'].fillna(0)
purchs['Price'] = purchs['Price'].map(lambda x: ''.join(x.split(' ')) if ' ' in str(x) else x)
purchs['Price'] = purchs['Price'].map(lambda x: x.replace(',', '') if '.' in str(x) and ',' in str(x) else x)
purchs['Price'] = purchs['Price'].map(lambda x: x.replace(',', '') if str(x).count(',')>1  else x)
purchs['Price'] = purchs['Price'].astype(float)

purchs.loc [ purchs['Сurrency'] == 'сум','Price' ] = purchs['Price']/12000
purchs.loc [ purchs['Сurrency'] == 'EUR','Price' ] = purchs['Price']*1.08
purchs.loc [ purchs['Сurrency'] == 'RUB','Price' ] = purchs['Price']/90



purchs['Date'] = purchs['Date'].fillna(0)
purchs['Date'] = pd.to_datetime(purchs['Date'])
purchs['contractYear']  = purchs['Date'].dt.year
purchs['contractMonth'] = purchs['Date'].dt.month



purchs['mergeNumber'] = ''
for RequisitionNumber, group in purchs.groupby('Requisition Number'):
    counter = 0
    for i, row in group.iterrows():
        purchs.loc[ i, 'mergeNumber'] = str(RequisitionNumber) + "-" + str(counter)
        counter += 1


purchs = purchs.loc [ purchs['Requisition Number'].isin(requisitions['Requisition Number'].unique()) ]
purchs = purchs[['Contract', 'Items', 'Price', 'Requisition Number', 'mergeNumber',	'contractYear', 'contractMonth']]

budgetContracted = purchs.groupby('contractMonth')['Price'].sum()
budgetPlaned = requisitions.groupby('raisedMonth')['Total Expected Price'].sum()
budgetRequired = requisitions.groupby('requiredMonth')['Total Expected Price'].sum()

purchCompare = purchs.merge(requisitions, how='outer', on=['Requisition Number','mergeNumber' ])

budgetContracted.to_excel('budgetContracted.xlsx')
budgetPlaned.to_excel('budgetPlaned.xlsx')
budgetRequired.to_excel('budgetRequired.xlsx')
purchs.to_excel('purchs.xlsx')
purchCompare.to_excel('purchCompare.xlsx')