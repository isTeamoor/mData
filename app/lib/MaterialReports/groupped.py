import pandas as pd



def spread(transactions, spares, inactive_Master_Reservations):

  transacts = transactions.copy()
  targetDF = transacts.loc[ (transacts['Is Master Work Order']=='yes') & (~(transacts['Reservation Number'].isin(inactive_Master_Reservations))) ]
  if targetDF.loc[ ~(targetDF['Catalogue Transaction Action Name']=='Issue') ].size != 0:
    print('there are master reservations with return to stock')
  else:
    print('there are NO master reservations with return to stock')

  

  MRs = targetDF.copy().groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth', 'Отдел','Reserved By','WO №','reservYear',
                                 'reservMonth','Asset Description', 'Объект','closedYear', 'Catalogue Transaction Action Name','transactMonth']).sum()
  MRs.reset_index(drop=False, inplace=True)



  childSpares = spares.loc[ (~(spares['Group WO number']=='undefined')) & (spares['Spares Comment'].str.isnumeric()) ].copy()
  childSpares['Spares Comment'] = childSpares['Spares Comment'].astype(float)







  Limits = pd.DataFrame()

  checkHasValues = False



  for i, MR in MRs.iterrows():

    if  childSpares.loc[ childSpares['Spares Comment'] == MR['Reservation Number'] ].size != 0:
      checkHasValues = True
      for i, childSpare in childSpares.loc[ childSpares['Spares Comment'] == MR['Reservation Number'] ].iterrows():
        record = pd.DataFrame({
          'master WO №':MR['WO №'],
          'master WO Status' : MR['Work Order Status Description'],
          'master Reservation Reserved By' : MR['Reserved By'],
          'master Reservation №' : MR['Reservation Number'],
          'master Reservation material' : MR['Материал'],
          'master Reservation Material Code' : MR['Код товара'],
          'master Reservation Qty' : MR['Quantity'],
          'master Reservation reservYear' : MR['reservYear'],
          'master Reservation reservMonth' : MR['reservMonth'],
          'master Reservation transactMonth':MR['transactMonth'], 
          'is new transaction':'yes'
        }, index=[0])
        for key in childSpare.index:
          record[key] = childSpare[key]

        Limits = pd.concat([Limits, record]).reset_index(drop=True)
    
    else:
        record = pd.DataFrame({
          'master WO №':MR['WO №'],
          'master WO Status' : MR['Work Order Status Description'],
          'master Reservation Reserved By' : MR['Reserved By'],
          'master Reservation №' : MR['Reservation Number'],
          'master Reservation material' : MR['Материал'],
          'master Reservation Material Code' : MR['Код товара'],
          'master Reservation Qty' : MR['Quantity'],
          'master Reservation reservYear' : MR['reservYear'],
          'master Reservation reservMonth' : MR['reservMonth'],
          'master Reservation transactMonth':MR['transactMonth'], 
          'is new transaction':'no'
        }, index=[0])

        Limits = pd.concat([Limits, record]).reset_index(drop=True)

  if checkHasValues == False:
    return transacts




  for i, MR in MRs.iterrows():
    usedQty = Limits.loc[ Limits['master Reservation №'] == MR['Reservation Number'], 'Estimated Quantity'].sum().item()
    Limits.loc[ Limits['master Reservation №'] == MR['Reservation Number'], 'Remain Qty' ] = Limits['master Reservation Qty'] - usedQty



  Limits2 = Limits.groupby(['master Reservation №','master WO №', 'master Reservation material', 'master Reservation Qty','Remain Qty'])['Actual Quantity'].count()
  Limits2 = Limits2.reset_index(drop=False)
  Limits2 = Limits2[['master WO №', 'master Reservation №', 'master Reservation material', 'master Reservation Qty',	'Remain Qty' ]]



  transacts=transacts.drop(targetDF.index)
  counter = -10000
  for i, childSpare in Limits.loc[ Limits['is new transaction']=='yes' ].iterrows():
    counter+=1
    pseudoTransaction = pd.DataFrame({
      'Код товара':childSpare['master Reservation Material Code'],
      'Материал':childSpare['master Reservation material'],
      'Ед.изм.':childSpare['UOMDescription'],
      'Quantity':childSpare['Estimated Quantity'],
      'Reservation Number':counter,
      'Work Order Status Description':childSpare['Work Order Status Description'],
      'closedMonth':childSpare['closedMonth'],
      'closedYear':childSpare['closedYear'],
      'transactMonth':childSpare['master Reservation transactMonth'],                               
      'Отдел':childSpare['Short Department Name'],
      'Reserved By':childSpare['master Reservation Reserved By'],
      'WO №':childSpare['Work Order Number'],
      'reservYear':childSpare['raisedYear'],
      'reservMonth':childSpare['raisedMonth'],
      'Asset Description':childSpare['Asset Description'], 
      'Объект':childSpare['Asset Number'],
      'Estimated Quantity':childSpare['Estimated Quantity'],                               
      'Group WO number':childSpare['master WO №'], 
      'Is Group Work Order':'no',
      'Spares Comment':childSpare['master Reservation №'],
      'Catalogue Transaction Action Name':'Issue'
    }, index=[0])
    transacts = pd.concat([transacts, pseudoTransaction]).reset_index(drop=True)
  


  for i, MR in MRs.iterrows():
    pseudoTransaction = {}
    for column in MR.index:
      pseudoTransaction[column] = MR[column]
    pseudoTransaction['Quantity'] = Limits2.loc[ Limits2['master Reservation №'] == MR['Reservation Number'] , 'Remain Qty'].item()
    pseudoTransaction = pd.DataFrame(pseudoTransaction, index=[0])
    transacts = pd.concat([transacts, pseudoTransaction]).reset_index(drop=True)


  Limits[['master Reservation Reserved By',	'master WO №',	'master WO Status',	'master Reservation №',	'master Reservation reservMonth',	'master Reservation Material Code',
          'master Reservation material',	'master Reservation Qty',	'Work Order Spare Description',	'Estimated Quantity',	'Work Order Number',	'Work Order Description',	
          'Work Order Status Description',	'Asset Description',	'Asset Number']].to_excel('limits.xlsx')
  Limits2.to_excel('limits2.xlsx')
  return transacts
