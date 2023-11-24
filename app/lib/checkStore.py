import pandas as pd

['Catalogue Transaction ID', 'Catalogue Asset ID',
       'Catalogue Transaction Action Name', 'Catalogue Transaction Date Time',
       'Quantity', 'Unit Cost', 'Work Order Spare ID', 'Asset ID',
       'Catalogue Number', 'Catalogue Description', 'Material Code',
       'UOMDescription', 'Total Quantity Reserved', 'Stock On Hand',
       'transactYear', 'transactMonth', 'transactDay', 'reservYear',
       'reservMonth', 'Reservation Number', 'Work Order Number',
       'Work Order Status Description', 'Short Department Name', 'isRMPD',
       'isMaintenance', 'Asset Description', 'Asset Number', 'Reserved By',
       'closedYear', 'closedMonth', 'Actual Quantity', 'Estimated Unit Cost',
       'Estimated Quantity', 'Group WO number', 'Is Group Work Order',
       'Spares Comment']

def exec(transactions, repMonth, repYear):
    transactions['Quantity'] = transactions['Quantity'].map(lambda x: -x)
    transactions = transactions[['Material Code', 'Catalogue Description', 'Catalogue Transaction Action Name', 'Quantity','transactYear', 'transactMonth',]]

    begin = transactions.loc [ ((transactions['transactYear']==repYear) & (transactions['transactMonth']<repMonth))
                             | (transactions['transactYear']<repYear)  ].copy()
    begin.rename(columns={'Quantity':'Begin Quantity'}, inplace=True)
    begin = begin.groupby(['Material Code', 'Catalogue Description']).sum()
    begin.reset_index(drop=False, inplace = True)

        
    current = transactions.loc [ (transactions['transactYear']==repYear) & (transactions['transactMonth']==repMonth) ].copy()
    current.rename(columns={'Quantity':'Current Quantity'}, inplace=True) 
    current = current.groupby(['Material Code', 'Catalogue Description']).sum()
    current.reset_index(drop=False, inplace = True)


    rep = begin.merge(current, on = ['Material Code', 'Catalogue Description'], how = 'outer')[['Material Code', 'Catalogue Description','Begin Quantity','Current Quantity']]
    rep[['Begin Quantity','Current Quantity']] = rep[['Begin Quantity','Current Quantity']].fillna(0)
    rep = rep.loc[ ~((rep['Begin Quantity']==0) & (rep['Current Quantity']==0)) ]
    rep['Balance'] = rep['Begin Quantity'] + rep['Current Quantity']

    wh = pd.read_excel('wh.xlsx', sheet_name='10. Материаллар').iloc[12:]
    wh = wh.loc[ ~wh['Unnamed: 1'].isna() ]
    wh = wh[['Unnamed: 0','Unnamed: 1','Unnamed: 4', 'Unnamed: 6','Unnamed: 8', 'Unnamed: 12']]
    wh['Unnamed: 0'] = wh['Unnamed: 0'].astype(str).map(lambda x: x.strip()[-4:])
    wh.rename(columns={'Unnamed: 0':'Wh Code', 'Unnamed: 1': 'Wh Material','Unnamed: 4': 'Wh begin','Unnamed: 6':'Wh kirim','Unnamed: 8':'Wh chiqim','Unnamed: 12':'Wh balance'  }, inplace=True)

    rep = rep.merge(wh, left_on = 'Material Code', right_on = 'Wh Code', how = 'outer')
    rep[['Begin Quantity', 'Current Quantity', 'Balance', 'Wh begin','Wh kirim','Wh chiqim','Wh balance']] = rep[['Begin Quantity', 'Current Quantity', 'Balance', 'Wh begin','Wh kirim','Wh chiqim','Wh balance']].fillna(0)
    rep['Difference'] = rep['Balance'] - rep['Wh balance']
    rep = rep[['Material Code', 'Wh Code', 'Catalogue Description', 'Wh Material','Difference','Begin Quantity', 'Current Quantity', 'Balance', 'Wh begin','Wh kirim','Wh chiqim','Wh balance']]

    rep.to_excel('rep.xlsx')
