import pandas as pd
from ...database.DF__spares import spares
from ..gen import filterDF
from . import exceptions, reference, yaroqsiz




def matReport(repMonth, repYear, department, transacts):
  ### 1. Подготовка DF Transactions
  transactions = exceptions.corrections(transacts)
  

  transactions  = transactions.loc[ transactions['Catalogue Transaction Action Name'].isin(['Issue', 'Return to Stock']) ]
  
  transactions  = transactions.loc[ ~(transactions['Reservation Number'].isin(exceptions.inactive_Reservations)) ]

  transactions = filterDF(transactions, reference.department_Filters[department])

  transactions = reference.spread(transactions, spares, exceptions.inactive_Master_Reservations, repMonth, repYear)

  
  ### 2. Выборка транзакций на начало отчётного периода
  begin = transactions.loc[ 
    (
      ((transactions['transactYear'] == repYear) & (transactions['transactMonth'] < repMonth)) 
      | (transactions['transactYear'] < repYear)
    )
    & 
    ( 
      (transactions['Work Order Status Description'] != 'Closed') 
      | 
      (
        (transactions['Work Order Status Description'] == 'Closed') 
        & 
        (
          (transactions['closedYear'] == repYear) & (transactions['closedMonth'] >= repMonth)
          | 
          (transactions['closedYear'] > repYear)
        )
      )
    )
  ].copy()
  



  ### 3. Выборка транзакций за отчётный период
  current = transactions.loc[ (transactions['transactMonth'] == repMonth) & (transactions['transactYear'] == repYear) 
                             & (transactions['Catalogue Transaction Action Name']=='Issue') ].copy()



  ### 4. Возвраты за отчётный период
  currentReturn = transactions.loc[ (transactions['transactMonth'] == repMonth) & (transactions['transactYear'] == repYear)
                                   & (transactions['Catalogue Transaction Action Name']=='Return to Stock') ].copy()
  



  for row in exceptions.extra[department]['begin']:
      newRow = pd.DataFrame(row, index=[0])
      begin = pd.concat([begin, newRow]).reset_index(drop=True)
  for row in exceptions.extra[department]['currentMonth']:
      newRow = pd.DataFrame(row, index=[0])
      current = pd.concat([current, newRow]).reset_index(drop=True)
  for row in exceptions.extra[department]['currentReturn']:
      newRow = pd.DataFrame(row, index=[0])
      currentReturn = pd.concat([currentReturn, newRow]).reset_index(drop=True)




  currentReturn['Quantity'] = currentReturn['Quantity'].map(lambda x: -x) ### Qty "положительные"



  ### Скорее всего группировка нужна только для begin, чтобы уменьшить на количество возврата в предыдущие периоды
  begin        .rename(columns={'Quantity':'Кол-во начало'}, inplace=True)
  current      .rename(columns={'Quantity':'Кол-во приход'}, inplace=True)
  currentReturn.rename(columns={'Quantity':'Кол-во возврат'}, inplace=True)

  begin                 = begin.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  current             = current.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  currentReturn = currentReturn.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  begin        .reset_index(drop=False, inplace=True)
  current      .reset_index(drop=False, inplace=True)
  currentReturn.reset_index(drop=False, inplace=True)



  ### Если в одном месяце взяли и сразу вернули
  for i,row in current.iterrows():
      if row['Reservation Number'] in currentReturn['Reservation Number'].unique():
          current.loc[ current['Reservation Number']==row['Reservation Number'], 'Кол-во приход' ] = row['Кол-во приход'] - currentReturn.loc[ currentReturn['Reservation Number']==row['Reservation Number'], 'Кол-во возврат' ].item()
          currentReturn = currentReturn.loc[ currentReturn['Reservation Number']!=row['Reservation Number'] ]
  


  ### 5. Объединение "на начало" и "приход" и "возврат"
  rep = begin.merge(current,     how='outer', on=['Код товара','Материал','Ед.изм.','Reservation Number','Work Order Status Description','closedYear','closedMonth','Отдел','Reserved By','WO №','Asset Description','Объект',])
  rep = rep.merge(currentReturn, how='outer', on=['Код товара','Материал','Ед.изм.','Reservation Number','Work Order Status Description','closedYear','closedMonth','Отдел','Reserved By','WO №','Asset Description','Объект',])

  rep = rep.merge(reference.OneC(), on = 'Код товара', how = 'outer')  #OneC.columns = ['Account', 'Код товара', 'Цена']
  rep.fillna({'Кол-во начало':0,'Кол-во приход':0,'Кол-во возврат':0,'Цена':0}, inplace=True)

  rep['is014'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in reference.is_014 else '')
  rep['iswOff'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in reference.is_wOff else '')



  ### Файл для проверки соответствия количества в rep и 1с
  cheQ = rep[['Код товара',	'Материал',	'Кол-во начало',	'Кол-во приход',	'Qty1',	'Qty2',	]].copy()
  cheQ = cheQ.groupby(['Код товара',	'Материал',	'Qty1',	'Qty2',	]).sum()
  cheQ.reset_index(inplace=True, drop=False)
  cheQ = cheQ[['Код товара',	'Материал',	'Кол-во начало','Qty1',	'Кол-во приход','Qty2']]
  cheQ.insert(6, 'Dif_начало', cheQ['Кол-во начало'] - cheQ['Qty1'])
  cheQ.insert(7, 'Dif_приход', cheQ['Кол-во приход'] - cheQ['Qty2'])
  cheQ.insert(8, 'Dif_all', cheQ['Dif_начало'] + cheQ['Dif_приход'])





  ### 6. Поле "Расход"
  rep['Кол-во расход'] =  rep['Кол-во начало'] + rep['Кол-во приход'] # Если списываются

  rep.loc[(rep['is014'] == 'yes')
          | 
          (
            (rep['Work Order Status Description'] != 'Closed') 
            | 
            (
              (rep['Work Order Status Description'] == 'Closed') 
              & 
              (
                ((rep['closedYear'] == repYear) & (rep['closedMonth'] > repMonth)) 
                | (rep['closedYear'] > repYear)
              )
            )
          ), 'Кол-во расход' ] = 0 + rep['Кол-во возврат']



  ### 7. Поле "014"
  rep['Кол-во 014'] = rep['Кол-во начало'] + rep['Кол-во приход'] - rep['Кол-во возврат'] # Если списываются

  rep.loc[(rep['is014'] != 'yes')
          | 
          (
            (rep['Work Order Status Description'] != 'Closed') 
            | 
            (
              (rep['Work Order Status Description'] == 'Closed') 
              & 
              (((rep['closedYear'] == repYear) & (rep['closedMonth'] > repMonth)) 
                | (rep['closedYear'] > repYear))
            )
          ), 'Кол-во 014' ] = 0




  ### 8. Поле "на Конец"
  rep['Кол-во конец'] = 0 # Если списываются
  rep.loc[(rep['Work Order Status Description'] != 'Closed') 
          | 
          (
            (rep['Work Order Status Description'] == 'Closed') 
            & 
            (((rep['closedYear'] == repYear) & (rep['closedMonth'] > repMonth)) 
              | (rep['closedYear'] > repYear))
          ), 'Кол-во конец' ] = rep['Кол-во начало'] + rep['Кол-во приход'] - rep['Кол-во возврат']




  ###Exception do not consider diesel's price
  rep.loc[rep['Код товара']=='06933', 'Цена'] = 0
  ##########################################################



  ### 9. Вычисление сумм
  rep['Сумма начало']  = rep['Кол-во начало']  * rep['Цена']
  rep['Сумма приход']  = rep['Кол-во приход']  * rep['Цена']
  rep['Сумма расход']  = rep['Кол-во расход']  * rep['Цена']
  rep['Сумма 014']     = rep['Кол-во 014']     * rep['Цена']
  rep['Сумма конец']   = rep['Кол-во конец']   * rep['Цена']



  
  ### Exception different prices in 1c
  if department == 'cofe':
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 53571.42853     if x['Код товара']=='11062' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 53348.3258   if x['Код товара']=='11062' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 53571.4285   if x['Код товара']=='11062' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 53357.91   if x['Код товара']=='11062' else x['Сумма конец'], axis=1)

      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 10580.357     if x['Код товара']=='05733' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 10336.74   if x['Код товара']=='05733' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 10580.357040   if x['Код товара']=='05733' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 10245.21   if x['Код товара']=='05733' else x['Сумма конец'], axis=1)

      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 1     if x['Код товара']=='12481' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 3043.63   if x['Код товара']=='12481' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 870.32   if x['Код товара']=='12481' else x['Сумма расход'], axis=1)
  
  if department == 'rmpd':
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 1     if x['Код товара']=='12478' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 1268.179   if x['Код товара']=='12478' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 1   if x['Код товара']=='12478' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 1106.5906   if x['Код товара']=='12478' else x['Сумма конец'], axis=1)

      #Труба (30394) из тн -> м 
      rep['Ед.изм.'] = rep.apply(lambda x: 'м' if x['Код товара']=='30394' else x['Ед.изм.'], axis=1)
      rep['Кол-во приход'] = rep.apply(lambda x: x['Кол-во приход'] * 142.5   if x['Код товара']=='30394' else x['Кол-во приход'], axis=1)
      rep['Кол-во конец'] = rep.apply(lambda x: x['Кол-во конец'] * 142.5   if x['Код товара']=='30394' else x['Кол-во конец'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 169319.6359649123   if x['Код товара']=='30394' else x['Сумма приход'], axis=1)
      rep['Сумма конец']  = rep.apply(lambda x: x['Кол-во конец'] * 169319.6359649123    if x['Код товара']=='30394' else x['Сумма конец'], axis=1)
  ##########################################################

  



  ### 10. Завершение подготовки базового DF
  rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
              'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
              'closedMonth','Отдел','Reserved By','is014','iswOff','WO №','Asset Description', 'Объект', 'Кол-во возврат']]




  ### 11. Базовый файл с детализацией по Reservations
  check = rep.copy()




  ### 12. Подготовка итогового материального отчёта
  rep = rep.loc[ ~rep['Account'].isna() ]
  rep.fillna({'Код товара':'undefined','Account':'undefined','Материал':'undefined',
              'Ед.изм.':'undefined','Цена':-1 }, inplace=True)
  matRep = rep.groupby(['Код товара','Account','Материал','Ед.изм.','Цена']).sum()
  matRep.reset_index(drop=False, inplace=True)
  matRep = matRep[['Account','Код товара','Материал','Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход','Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец',]]
  
  ### Cуммирующие строки
  for acc in matRep['Account'].unique():
      matRep.loc[ len(matRep)] = matRep.loc[ matRep['Account']==acc ].sum(numeric_only=True)
      matRep.loc[ len(matRep)-1, 'Account'] = acc
  matRep.loc[ len(matRep) ] = matRep.loc[ matRep['Материал'].isna() ].sum(numeric_only=True)
  matRep.loc[ len(matRep)-1, 'Материал'] = 'Жами'





  ### 13. Подготовка Акта ввода в эксплуатацию (внутренний)
  dalolat = rep.loc[ (rep['Кол-во расход']>0) & (rep['iswOff']!='yes') ].copy()
  dalolat['Кол-во расход'] = dalolat['Кол-во расход'] - dalolat['Кол-во возврат']
  dalolat = dalolat.loc [ dalolat['Кол-во расход'] !=0 ]
  
  dalolat['Кол-во всего'] = dalolat['Код товара'].copy().map(  lambda x: dalolat.loc[ dalolat['Код товара'] == x, 'Кол-во расход' ].sum() )
  
  dalolat = dalolat[['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By','Цена', 'Сумма расход']]
  dalolat = dalolat.groupby(['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By',]).sum()




  ### 14. Файл списание
  raw_wOff = rep.loc[ rep['Кол-во расход']>0 ].copy()
  raw_wOff['Кол-во расход'] = raw_wOff['Кол-во расход'] - raw_wOff['Кол-во возврат']
  raw_wOff = raw_wOff.loc [ raw_wOff['Кол-во расход'] !=0 ]
  
  raw_wOff = raw_wOff[['Код товара', 'Материал', "Ед.изм.",'Цена','Кол-во расход', 'Сумма расход',"Отдел"]]
  raw_wOff = raw_wOff.groupby(['Код товара', 'Материал',"Ед.изм.",'Цена', "Отдел"]).sum()
  raw_wOff.reset_index(drop=False, inplace=True)

  raw_wOff['Объект'] = ''

  wOff_Mn = raw_wOff.loc[ (raw_wOff['Отдел']!='4AP') & (raw_wOff['Отдел']!='4AP_free') ].copy()
  wOff_Ap = raw_wOff.loc[ (raw_wOff['Отдел']=='4AP') | (raw_wOff['Отдел']=='4AP_free') ].copy()
  

  wOff_Ap = wOff_Ap.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  wOff_Mn = wOff_Mn.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()

  wOff_Ap.reset_index(drop=False, inplace=True)
  wOff_Mn.reset_index(drop=False, inplace=True)

  wOff_Ap = wOff_Ap[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]
  wOff_Mn = wOff_Mn[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]




  ### 14. Раздача
  handover = rep.loc[ (rep['Кол-во 014']>0)
                      |
                      (
                         (rep['Кол-во расход']>0) & (rep['iswOff']=='yes')
                      ) 
                     ].copy()

  handover.insert(1,'Примечание', 'Reserved by '+handover['Reserved By']+' WO № '+handover['WO №'].astype(str)+' Reservation № '+handover['Reservation Number'].astype(str))
  handover = handover[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014','Кол-во расход', 'Примечание']]




  ### 14. Ввод в эксплуатацию
  to014 = rep.loc[ rep['Кол-во 014']>0 ].copy()
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]
  to014['Объект'] = ''
  to014 = to014.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  to014.reset_index(drop=False, inplace=True)
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]


  cheQ.to_excel('cheQ.xlsx', index=False)
  check.to_excel('2. check.xlsx', index=False)
  matRep.to_excel('3. matRep.xlsx', index=False)
  dalolat.to_excel('4. dalolat.xlsx')
  handover.to_excel('4. handover.xlsx', index=False)
  to014.to_excel('4. 014.xlsx', index=False)
  wOff_Ap.to_excel('4. wOff_AP.xlsx', index=False)
  wOff_Mn.to_excel('4. wOff_Mn.xlsx', index=False)
  reference.OneCW()
  
    

  ### 15. Yaroqsiz to Metall
  met = dalolat.copy()
  met.reset_index(drop = False, inplace = True)

  met = met.loc[ (met['Отдел']!='4AP') & (met['Отдел']!='4AP_free') ]

  met.insert(2, 'info', met['Кол-во расход'].astype(str) + ' ' + met['Ед.изм.'] + ' [ ' + met['Объект'] + ' ] WO-' + met['WO №'].astype(str) + ' by: ' + met['Reserved By'] + "\n")
  met = met.groupby(['Код товара', 'Материал'])[['info', 'Кол-во расход']].sum()
  met.reset_index(drop = False, inplace = True)


  if department == 'rmpd':
      yaroq = yaroqsiz.execute(transacts)
      
      yaroq = yaroq.merge(met, how='outer', on='Код товара')
      yaroq = yaroqsiz.metLib(yaroq)

      yaroq = yaroq[['Номер файла','Номер документа','Код товара','Количество (из акта)','Кол-во расход','info','Материал (из акта)','Материал',	
                     'На уничтожение','В повторное использование','На металл','Алюминий, кг','Медь, кг','Нержавейка, кг','Черный металл, кг','Драг. металл, кг']]
      
      yaroq.to_excel('5. yaroq.xlsx', index=False)

      
