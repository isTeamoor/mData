from ...database.DF__spares import spares

def check():
    noAcc = spares.loc[
        (spares['Account Code']=='undefined')
        & (spares['raisedYear']>2022)
        & (~(  (spares['Reservation Number']==0) & (spares['Spares Comment'].isna()) ))
        ]
    noAcc = noAcc[[
        'Work Order Number','Work Order Status Description','Reservation Number','Reserved By',
        'Work Order Spare Description','Actual Quantity',
        'Account Code','Department Name','Department Description','Spares Comment']]
    noAcc.to_excel('fix.xlsx', index=False)