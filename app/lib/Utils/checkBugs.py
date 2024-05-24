from datetime import datetime

from ...database.DF__spares import spares
from ...database.DF__wo import wo
from ...database.DF__transactions import transactions

def check():
    ### No Account Code
    noAcc = spares.loc[
        (spares['Account Code']=='undefined')
        & (spares['raisedYear']>2022)
        & (~(  (spares['Reservation Number']==0) & (spares['Spares Comment'].isna()) ))
        ]
    
    noAcc = noAcc[[
        'Work Order Number','Work Order Status Description','Reservation Number','Reserved By',
        'Work Order Spare Description','Actual Quantity',
        'Account Code','Department Name','Department Description','Spares Comment']]
    


    ### Not Closed WO
    openWO = wo.loc[
        (wo['raisedYear']>2022)
        & (~wo['Work Order Status Description'].isin(['Cancelled','Closed']) )
    ]

    openWO['Lag'] = datetime.now() - openWO['Raised Date Time']

    openWO = openWO[['Created By','Lag','Work Order Number', 'Work Order Status Description',
                     'raisedYear', 'raisedMonth',
                     'Priority Description','Department Name','Short Department Name','Department Description','isMaintenance'
                     ]]



    ### Actual 0, but Reservation issued
    reservBug = transactions.loc[ (transactions['Catalogue Transaction Action Name'] == 'Issue') 
                                | (transactions['Catalogue Transaction Action Name'] == 'Return to Stock')
                                | (transactions['Catalogue Transaction Action Name'] == 'Reverse Over Issue - Over Issue Correction')
                                ]
    reservBug = reservBug[[
    'Quantity', 'Материал','Reservation Number', 'WO №', 'Work Order Status Description'
    ]]
    reservBug = reservBug.groupby(['WO №','Reservation Number','Work Order Status Description','Материал']).sum()
    reservBug.reset_index(drop=False, inplace=True)

    #Reservation = 0, quantity >0
    reservBug1 = reservBug.loc[(reservBug['Reservation Number']==0) & (reservBug['Quantity']!=0)]

    #
    reservBug = reservBug.merge(spares[['Reservation Number','Actual Quantity']], how='left', on='Reservation Number')
    reservBug = reservBug.loc[reservBug['Reservation Number']!=0]
    reservBug['Dif'] = reservBug['Quantity'] - reservBug['Actual Quantity']
    reservBug = reservBug.loc[reservBug['Dif']!=0]


    ###Print
    reservBug.to_excel('reservBug.xlsx', index=False)
    reservBug1.to_excel('reservBug1.xlsx', index=False)
    openWO.to_excel('openWO.xlsx', index=False)
    noAcc.to_excel('fix.xlsx', index=False)