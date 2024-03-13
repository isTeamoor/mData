import pandas as pd
from ...database.DF__spares import spares
from ...database.DF__assets import unitChildren
from ..gen import filterDF
from . import exceptions, reference




def matReport(repMonth, repYear, department, transactions):
  
  ### 1. Подготовка DF Transactions
  transactions = exceptions.corrections(transactions)
  
  transactions  = transactions.loc[ ((transactions['Catalogue Transaction Action Name'] == 'Issue') | (transactions['Catalogue Transaction Action Name'] == 'Return to Stock'))
                                  & (~transactions['Reservation Number'].isin(exceptions.inactive_Reservations))
                                  ].copy()
  
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


  begin        .rename(columns={'Quantity':'Кол-во начало'}, inplace=True)
  current      .rename(columns={'Quantity':'Кол-во приход'}, inplace=True)
  currentReturn.rename(columns={'Quantity':'Кол-во возврат'}, inplace=True)

  begin                 = begin.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  current             = current.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  currentReturn = currentReturn.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','closedYear','Отдел', 'Reserved By','WO №','Asset Description', 'Объект',]).sum()
  begin        .reset_index(drop=False, inplace=True)
  current      .reset_index(drop=False, inplace=True)
  currentReturn.reset_index(drop=False, inplace=True)
  




  ### 5. Объединение "на начало" и "приход" и "возврат"
  rep = begin.merge(current,     how='outer', on=['Код товара','Материал','Ед.изм.','Reservation Number','Work Order Status Description','closedYear','closedMonth','Отдел','Reserved By','WO №','Asset Description','Объект',])
  rep = rep.merge(currentReturn, how='outer', on=['Код товара','Материал','Ед.изм.','Reservation Number','Work Order Status Description','closedYear','closedMonth','Отдел','Reserved By','WO №','Asset Description','Объект',])

  rep = rep.merge(reference.OneC(), on = 'Код товара', how = 'outer')  #OneC.columns = ['Account', 'Код товара', 'Цена']
  rep.fillna({'Кол-во начало':0,'Кол-во приход':0,'Кол-во возврат':0,'Цена':0}, inplace=True)

  rep['is014'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in reference.is_014 else '')





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








  ### 10. Завершение подготовки базового DF
  rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
              'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
              'closedMonth','Отдел','Reserved By','is014','WO №','reservYear','reservMonth','Asset Description', 'Объект', 'Кол-во возврат']]




  ### 11. Базовый файл с детализацией по Reservations
  check = rep.copy()




  ### 12. Подготовка итогового материального отчёта
  rep = rep.loc[~rep['Account'].isna()]
  rep.fillna({'Код товара':'undefined','Account':'undefined','Материал':'undefined',
              'Ед.изм.':'undefined','Цена':-1 }, inplace=True)

  matRep = rep.groupby(['Код товара','Account','Материал','Ед.изм.','Цена']).sum()
  matRep.reset_index(drop=False, inplace=True)
  matRep = matRep[['Account','Код товара','Материал','Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход','Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец',]]
  
  #############Exception due to additional costs set by 1c
  if department == 'rmpd':
    matRep.loc[matRep['Код товара']=='12207', 'Сумма начало'] = 1868409.06
    matRep.loc[matRep['Код товара']=='12207', 'Сумма приход'] = 2839603.92

    matRep.loc[matRep['Код товара']=='12208', 'Сумма начало'] = 1868409.06
    matRep.loc[matRep['Код товара']=='12208', 'Сумма приход'] = 2839603.92

    matRep.loc[matRep['Код товара']=='12209', 'Сумма начало'] = 1868409.06
    matRep.loc[matRep['Код товара']=='12209', 'Сумма приход'] = 2839603.92

    matRep.loc[matRep['Код товара']=='12210', 'Сумма начало'] = 1868409.06
    matRep.loc[matRep['Код товара']=='12210', 'Сумма приход'] = 2839603.92
  ####################################################################

  ### Cуммирующие строки
  for acc in matRep['Account'].unique():
      matRep.loc[len(matRep)] = matRep.loc[ matRep['Account']==acc ].sum(numeric_only=True)
      matRep.loc[len(matRep)-1, 'Account'] = acc
  matRep.loc[len(matRep)] = matRep.loc[ matRep['Материал'].isna() ].sum(numeric_only=True)
  matRep.loc[len(matRep)-1, 'Материал'] = 'Жами'




  ### 13. Подготовка Акта ввода в эксплуатацию (внутренний)
  dalolat = rep.loc[ rep['Кол-во расход']>0 ].copy()
  dalolat['Кол-во расход'] = dalolat['Кол-во расход'] - dalolat['Кол-во возврат']
  dalolat = dalolat.loc [ dalolat['Кол-во расход'] !=0 ]
  
  dalolat['Кол-во всего'] = dalolat['Код товара'].copy().map(  lambda x: dalolat.loc[dalolat['Код товара'] == x, 'Кол-во расход'].sum() )
  
  dalolat = dalolat[['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By','Цена', 'Сумма расход']]
  dalolat = dalolat.groupby(['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By',]).sum()

  




  ### 14. Представление 014 для е-doc
  view_014 = rep.loc[ rep['Кол-во 014']>0 ].copy()
  view_014.insert(1,'Примечание', 'Reserved by '+view_014['Reserved By']+' WO № '+view_014['WO №'].astype(str)+' Reservation № '+view_014['Reservation Number'].astype(str))
  view_014 = view_014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014','Примечание']]

  view_014_G = view_014.copy()
  view_014_G['Объект'] = ''
  view_014_G = view_014_G.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  view_014_G.reset_index(drop=False, inplace=True)
  view_014_G = view_014_G[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014','Примечание']]





  ### 14. Представление списание для е-doc
  raw_wOff = dalolat.copy()
  raw_wOff.reset_index(drop=False, inplace=True)
  view_wOff_notSGU = raw_wOff.loc[raw_wOff['Отдел']!='4AP'].copy()
  view_wOff_SGU = raw_wOff.loc[raw_wOff['Отдел']=='4AP'].copy()
  view_wOff_notSGU = view_wOff_notSGU.loc [ view_wOff_notSGU['Кол-во расход'] !=0 ] [['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]   
  view_wOff_SGU = view_wOff_SGU.loc [ view_wOff_SGU['Кол-во расход'] !=0 ] [['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]  


  view_wOff_SGU_G = view_wOff_SGU.copy()
  view_wOff_notSGU_G = view_wOff_notSGU.copy()
  view_wOff_SGU_G['Объект'] = ''
  view_wOff_notSGU_G['Объект'] = ''
  view_wOff_SGU_G = view_wOff_SGU_G.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  view_wOff_notSGU_G = view_wOff_notSGU_G.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  view_wOff_SGU_G.reset_index(drop=False, inplace=True)
  view_wOff_notSGU_G.reset_index(drop=False, inplace=True)
  view_wOff_SGU_G = view_wOff_SGU_G[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]
  view_wOff_notSGU_G = view_wOff_notSGU_G[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]




  check.to_excel('2. check.xlsx')
  matRep.to_excel('3. matRep.xlsx')
  dalolat.to_excel('4. dalolat.xlsx')
  view_014.to_excel('4. view_014.xlsx')
  view_014_G.to_excel('4. view_014_G.xlsx')
  view_wOff_SGU.to_excel('4. view_wOff_SGU.xlsx')
  view_wOff_notSGU.to_excel('4. view_wOff_notSGU.xlsx')
  view_wOff_SGU_G.to_excel('4. view_wOff_SGU_G.xlsx')
  view_wOff_notSGU_G.to_excel('4. view_wOff_notSGU_G.xlsx')
  reference.OneCW()
  
    