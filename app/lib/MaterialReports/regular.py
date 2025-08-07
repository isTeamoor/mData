import pandas as pd
from ...database.DF__spares import spares
from ...database.DF__wo import wo
from ..gen import filterDF
from . import exceptions, reference, yaroqsiz




def matReport(repMonth, repYear, department, transacts):
  ### 1. Подготовка DF Transactions
  transactions = exceptions.corrections(transacts)
  
  transactions  = transactions.loc[ transactions['Catalogue Transaction Action Name'].isin(['Issue', 'Return to Stock']) ]
  
  transactions  = transactions.loc[ ~(transactions['Reservation Number'].isin(exceptions.inactive_Reservations)) ]

  transactions = filterDF(transactions, reference.department_Filters[department])

  transactions = reference.spread(transactions, spares, exceptions.inactive_Master_Reservations, repMonth, repYear)
  
  ### Отчёт по временному хранению
  transactions['TempSave'] = transactions.apply(lambda x: 'yes' if x['Reservation Number'] in reference.tempSave[department] else x['Reservation Number'], axis=1)
  transactions.loc[ transactions['TempSave']=='yes'].to_excel('TempSave_report.xlsx')
  
  ### Exception
  # CofE 1 Blind
  transactions.loc[ (transactions['WO №']==84795) & (transactions['Код товара']=='31335'), 'closedMonth'] = 3
  
  
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

  rep['is014'] = rep['Код товара'].map(lambda x: 'yes' if x in reference.is_014 else '')
  
  rep['iswOff'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in reference.is_wOff else '')

  ### Перевод на временное хранение
  #По номеру Reservation
  rep['is014'] = rep.apply(lambda x: 'yes' if x['Reservation Number'] in reference.tempSave[department] else x['is014'], axis=1)
  #По коду и WO№ в случае если reservation number отрицательный из-за лимитов
  rep['is014'] = rep.apply(lambda x: 'yes' if 
                           x['Код товара'] in reference.tempSaveLimits[department].keys()
                           and 
                           x['WO №'] == reference.tempSaveLimits[department][x['Код товара']]['wo'] else x['is014'], axis=1)

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
      #Аргон 11062
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 58035.71426728586     if x['Код товара']=='11062' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 58035.71432160804  if x['Код товара']=='11062' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 58035.71421709894  if x['Код товара']=='11062' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 58035.71430051813  if x['Код товара']=='11062' else x['Сумма конец'], axis=1)
      #Кислород 05733
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 10000   if x['Код товара']=='05733' else x['Сумма начало'], axis=1)
      #rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 10000  if x['Код товара']=='05733' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 10000  if x['Код товара']=='05733' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 10000  if x['Код товара']=='05733' else x['Сумма конец'], axis=1)
      #Азот 27158 !
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 150894.645  if x['Код товара']=='27158' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 150894.64  if x['Код товара']=='27158' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 150894.64   if x['Код товара']=='27158' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 150894.64   if x['Код товара']=='27158' else x['Сумма конец'], axis=1)
      #Свинцовая пломба 06801 !
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 28114.99736842105   if x['Код товара']=='06801' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 28114.99736842105  if x['Код товара']=='06801' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 28114.99736842105  if x['Код товара']=='06801' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 28114.99736842105  if x['Код товара']=='06801' else x['Сумма конец'], axis=1)
      #Кислород газообразный 13688
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 7652.536929993577   if x['Код товара']=='13688' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 7500  if x['Код товара']=='13688' else x['Сумма приход'], axis=1)
      rep['Сумма расход'] = rep.apply(lambda x: x['Кол-во расход'] * 7520.639610671765  if x['Код товара']=='13688' else x['Сумма расход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 7500  if x['Код товара']=='13688' else x['Сумма конец'], axis=1)
      
  if department == 'rmpd':
      a=1
      ##########################################################


  



  ### 10. Завершение подготовки базового DF

  rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
              'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
              'closedMonth','Отдел','Reserved By','is014','iswOff','WO №','Asset Description', 'Объект', 'Кол-во возврат']]
  

  ### !!! Exception steel angle 003 & 1040 accounts
  
  row1 = {'Account':'003.1 (Материалы на складе)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':1,
          'Кол-во начало':1000,'Сумма начало':1000,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':0,'Сумма расход':0,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':1000,'Сумма конец':1000, 
          'Reservation Number':22838,
          'Work Order Status Description':'Started','closedMonth':0,
          'Отдел':'Cofe-Jet Wash','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':137433,'Asset Description':'Washing buy area ', 'Объект':'WBA', 'Кол-во возврат':0}
  row2 = {'Account':'1040 (Запасные части)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':74323.4350833333,
          'Кол-во начало':120,'Сумма начало':8918812.21,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':0,'Сумма расход':0,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':120,'Сумма конец':8918812.21, 
          'Reservation Number':23322,
          'Work Order Status Description':'Started','closedMonth':0,
          'Отдел':'Cofe-Jet Wash','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':137433,'Asset Description':'Washing buy area ', 'Объект':'WBA', 'Кол-во возврат':0}
  row3 = {'Account':'1040 (Запасные части)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':74323.4350833333,
          'Кол-во начало':5,'Сумма начало':371617.18,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':5,'Сумма расход':371617.18,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':19432,
          'Work Order Status Description':'Closed','closedMonth':2,
          'Отдел':'Turnaround','Reserved By':'Kamoljon Ismoilov Yashinovich',
          'is014':'','iswOff':'','WO №':133264,'Asset Description':'Fired Steam Superheater', 'Объект':'172-XP-007', 'Кол-во возврат':0}
  row4 = {'Account':'1040 (Запасные части)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':74323.4350833333,
          'Кол-во начало':5,'Сумма начало':371617.18,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':5,'Сумма расход':371617.18,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':20231,
          'Work Order Status Description':'Closed','closedMonth':2,
          'Отдел':'Turnaround','Reserved By':'Kamoljon Ismoilov Yashinovich',
          'is014':'','iswOff':'','WO №':133264,'Asset Description':'Fired Steam Superheater', 'Объект':'172-XP-007', 'Кол-во возврат':0}
  row5 = {'Account':'003.1 (Материалы на складе)',
          'Код товара':'30405',
          'Материал':'0,6/1KV MGT/XLPE/LSZH  2C X 2,5sqmm+2,5sqmm / Кабель с изоляцией из слюдяной ленты, сшитого полиэтилена, с малодымной оболочкой и нулевым содержанием галогенов',
          'Ед.изм.':'м',
          'Цена':1,
          'Кол-во начало':0,'Сумма начало':0,
          'Кол-во приход':30,'Сумма приход':30,
          'Кол-во расход':30,'Сумма расход':30,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':25411,
          'Work Order Status Description':'Closed','closedMonth':6,
          'Отдел':'Cofe-Electrical','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':139844,'Asset Description':'Warehouse', 'Объект':'WIM', 'Кол-во возврат':0}
  row6 = {'Account':'1090 (Прочие материалы)',
          'Код товара':'30405',
          'Материал':'0,6/1KV MGT/XLPE/LSZH  2C X 2,5sqmm+2,5sqmm / Кабель с изоляцией из слюдяной ленты, сшитого полиэтилена, с малодымной оболочкой и нулевым содержанием галогенов',
          'Ед.изм.':'м',
          'Цена':15597.66338028169,
          'Кол-во начало':0,'Сумма начало':0,
          'Кол-во приход':71,'Сумма приход':1107434.1,
          'Кол-во расход':71,'Сумма расход':1107434.1,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':25412,
          'Work Order Status Description':'Closed','closedMonth':6,
          'Отдел':'Cofe-Electrical','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':139844,'Asset Description':'Warehouse', 'Объект':'WIM', 'Кол-во возврат':0}
  if department=='cofe':
    rep = rep.loc[ rep['Код товара']!='29137']
    rep = pd.concat([rep, pd.DataFrame(row1, index=[0])]).reset_index(drop=True)
    rep = pd.concat([rep, pd.DataFrame(row2, index=[0])]).reset_index(drop=True)
    #rep = rep.loc[ rep['Код товара']!='30405']
    #rep = pd.concat([rep, pd.DataFrame(row5, index=[0])]).reset_index(drop=True)
    #rep = pd.concat([rep, pd.DataFrame(row6, index=[0])]).reset_index(drop=True)
  """if department=='rmpd':
    rep = pd.concat([rep, pd.DataFrame(row3, index=[0])]).reset_index(drop=True)
    rep = pd.concat([rep, pd.DataFrame(row4, index=[0])]).reset_index(drop=True)"""



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

  ####################################################################################################
  wOff_Mn['Comment'] = ''
  if department == 'rmpd':
    
    wOff_Mn['Comment'] = "Zaxira qism/material. Eskirgan/yaroqsizlangan o'rniga o'rnatilgan. Sarflangan dalolatnoma asosida foydalanilgan. Ushbu aktga ilova №1.Eskirgan/yaroqsizlangan qismining holati va undan metallolom chiqimi ilova №3 da keltirilgan" 

    wOff_Mn['Comment'] = wOff_Mn.apply(lambda x: "Bir martalik foydalanish uchun. Topshirish qaydnomasi asosida foydalanilgan. Ushbu aktga ilova №2" 
                                      if x['Код товара'] in reference.is_wOff else x['Comment'], axis=1)
    
    wOff_Mn['Comment'] = wOff_Mn.apply(lambda x: "Sarflanadigan buyumlar. Sarflangan dalolatnoma asosida foydalanilgan. Ushbu aktga ilova №1" 
                                      if x['Код товара'] in yaroqsiz.notMet and x['Код товара'] not in reference.is_wOff else x['Comment'], axis=1)
    
    wOff_Mn['Comment'] = wOff_Mn.apply(lambda x: "Zaxira qism/material. Birinchi marta o'rnatilgan. Sarflangan dalolatnoma asosida foydalanilgan.Ushbu aktga ilova №1" 
                                      if x['Код товара'] in yaroqsiz.moc_DF['Код товара'].unique() else x['Comment'], axis=1)
  ####################################################################################################
  
  ### Exception
  """if department == 'cofe':
    #Аргон 11062
    wOff_Mn.loc[ wOff_Mn['Код товара']=='11062', 'Цена' ] = 53571.43
    wOff_Mn.loc[ wOff_Mn['Код товара']=='05733', 'Цена' ] = 9943.122014018023"""

  wOff_Mn['Сумма расход'] = wOff_Mn['Цена'] * wOff_Mn['Кол-во расход']
      
  wOff_Ap = wOff_Ap[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]
  wOff_Mn = wOff_Mn[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход','Comment']]





  ### 14. Раздача
  handover = rep.loc[ (rep['Кол-во 014']>0)
                      |
                      (
                         (rep['Кол-во расход']>0) & (rep['iswOff']=='yes')
                      ) 
                     ].copy()
  handover = handover.loc[ ~(handover['Reservation Number'].isin(reference.tempSave[department])) ]
  handover.insert(1,'Примечание', 'Reserved by '+handover['Reserved By']+' WO № '+handover['WO №'].astype(str)+' Reservation № '+handover['Reservation Number'].astype(str))
  handover = handover[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014','Кол-во расход', 'Примечание']]

  #TempSave handover
  tempSaveHO = rep.loc[ (rep['Кол-во 014']>0)
                      |
                      (
                         (rep['Кол-во расход']>0) & (rep['iswOff']=='yes')
                      ) 
                     ].copy()
  tempSaveHO = tempSaveHO.loc[ tempSaveHO['Reservation Number'].isin(reference.tempSave[department]) ]
  tempSaveHO.insert(1,'Примечание', 'Reserved by '+tempSaveHO['Reserved By']+' WO № '+tempSaveHO['WO №'].astype(str)+' Reservation № '+tempSaveHO['Reservation Number'].astype(str))
  tempSaveHO = tempSaveHO[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014','Кол-во расход', 'Примечание']]




  ### 14. Ввод в эксплуатацию
  to014 = rep.loc[ rep['Кол-во 014']>0 ].copy()
  to014 = to014.loc[ ~(to014['Reservation Number'].isin(reference.tempSave[department])) ]
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]
  to014['Объект'] = ''
  to014 = to014.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  to014.reset_index(drop=False, inplace=True)
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]

  #TempSave
  tempSave = rep.loc[ rep['Кол-во 014']>0 ].copy()
  tempSave = tempSave.loc[ tempSave['Reservation Number'].isin(reference.tempSave[department]) ] 
  tempSave = tempSave[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]
  tempSave['Объект'] = ''
  tempSave = tempSave.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  tempSave.reset_index(drop=False, inplace=True)
  tempSave = tempSave[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]


  cheQ.to_excel('cheQ.xlsx', index=False)
  check.to_excel('2. check.xlsx', index=False)
  matRep.to_excel('3. matRep.xlsx', index=False)
  dalolat.to_excel('4. dalolat.xlsx')
  handover.to_excel('4. handover.xlsx', index=False)
  tempSaveHO.to_excel('4. tempSaveHO.xlsx', index=False)
  to014.to_excel('4. 014.xlsx', index=False)
  tempSave.to_excel('4. tempSave.xlsx', index=False)
  wOff_Ap.to_excel('4. wOff_AP.xlsx', index=False)
  wOff_Mn.to_excel('4. wOff_Mn.xlsx', index=False)
  reference.OneCW()
    
  
  ### 15. Yaroqsiz to Metall
  met = dalolat.copy()
  met.reset_index(drop = False, inplace = True)
  


  # Без AP
  met = met.loc[ (met['Отдел']!='4AP') & (met['Отдел']!='4AP_free') ]

  # Добавляем WO Description
  met = met.merge(wo[['Work Order Number','Work Order Description']], how = 'left', left_on='WO №', right_on='Work Order Number' )
  
  # Добавляем Info
  met.insert(2, 'info', met['Кол-во расход'].astype(str) + ' ' + met['Ед.изм.'] + ' [ ' + met['Объект'] + ' ] WO-' + met['WO №'].astype(str) + ' by: ' + met['Reserved By'] + "\n")


  # Файл без группировки. Каждый Reservation отдельно
  met2 = met[['Код товара','Материал','Ед.изм.',
              'Кол-во всего','Кол-во расход',
              'Asset Description','Объект',
              'Reserved By','Reservation Number','Work Order Number','Work Order Description']].copy()


  # Файл с группировкой. Суммирует расход для каждого кода
  met = met.groupby(['Код товара','Материал'])[['info', 'Кол-во расход']].sum()
  met.reset_index(drop = False, inplace = True)
  


  if department == 'rmpd':
      yaroq = yaroqsiz.execute(transacts)
      yaroq = yaroq.merge(yaroqsiz.moc_DF, how='outer', on=['Код товара','Количество (из акта)','Номер документа','Номер файла','№','Материал (из акта)'])
      
      yaroq = yaroq.merge(met, how='outer', on='Код товара')
      yaroq = yaroqsiz.metLib(yaroq)

      yaroq = yaroq[['Номер файла','Номер документа','Код товара','Количество (из акта)','Кол-во расход','info','Материал (из акта)','Материал',	
                     'На уничтожение','В повторное использование','На металл','Алюминий, кг','Медь, кг','Нержавейка, кг','Черный металл, кг','Драг. металл, кг',]]
      

      
      yaroq_report = yaroq.copy()
      yaroq_report = yaroq_report.loc[ ~(yaroq_report['info'].isna()) ]
      yaroq_report = yaroq_report.fillna('')
      yaroq_report['checksum'] = yaroq_report.apply(lambda x: yaroq_report.loc[ yaroq_report['Код товара']==x['Код товара'],
                                                                                'Количество (из акта)' ].sum(), axis=1)
      yaroq_report = yaroq_report.groupby(['Код товара','Материал','info',
                                           'На уничтожение','В повторное использование','На металл',
                                           'Кол-во расход','checksum',
                                           'Номер документа','Номер файла','Материал (из акта)',]).sum()

      yaroq.to_excel('5. yaroq.xlsx', index=False)
      yaroq_report.to_excel('5. yaroq_report.xlsx')


      ### Extra
      yar = yaroq.loc[ ~(yaroq['Кол-во расход'].isna()) ]
      yar = yar[['Код товара','Номер документа','Количество (из акта)']]
      yar = yar.fillna({'Номер документа': "", 'Количество (из акта)': 0})
      
      yar = yar.groupby('Код товара', as_index=False).agg({
      'Количество (из акта)': 'sum',  # Суммируем числа
      'Номер документа': lambda x: ',\n'.join(x)  # Объединяем строки с переносом
      })
      yar.reset_index(drop = False, inplace = True)
      

      yar = yar.merge(met2, how='left', on='Код товара')
      yar['Catalogue Number'] = yar['Код товара'].copy().apply(lambda x: ( transactions.loc[ transactions['Код товара']==x, 'Catalogue Number' ].unique() )[0]     if x in  transactions['Код товара'].unique() else "")
      
      
      yar['test'] = yar['Кол-во всего'] - yar['Количество (из акта)']
      yar_stat = yar.copy()

      yar_full = yar.loc[yar['test']<=0]
      yar_full = yar_full.groupby(['Код товара','Catalogue Number','Материал','Ед.изм.','Количество (из акта)','Номер документа',
                         'Кол-во всего','Reservation Number','Кол-во расход','Asset Description','Объект','Reserved By','Work Order Number',
                         'Work Order Description']).sum()
      yar_full.to_excel('yar_full.xlsx')

      yar = yar.loc[yar['test']>0]
      yar = yar.groupby(['Код товара','Catalogue Number','Материал','Ед.изм.','Количество (из акта)','Номер документа',
                         'Кол-во всего','Reservation Number','Кол-во расход','Asset Description','Объект','Reserved By','Work Order Number',
                         'Work Order Description']).sum()
      yar.to_excel('yar.xlsx')

      yar_stat = yar_stat.groupby(['Код товара','Catalogue Number','Материал','Ед.изм.','Количество (из акта)','Кол-во всего',])[['Asset Description','Объект',]].sum()
      yar_stat.reset_index(drop = False, inplace = True)
      yar_stat['%']=yar_stat['Количество (из акта)']/yar_stat['Кол-во всего']

      finished_acts = {
         '14.03-16.03':['ORD-048/270-2025','ORD-048/76-2025','ORD-048/2340-2024','ORD-048/504-2025',],



      }
      for key, value in finished_acts.items():
         yar_stat[key] = 0
         for act in value:
            print(act)
            added = yaroq.loc[ yaroq['Номер документа'] == act ].copy()
            print(added)
            added = added.groupby('Код товара')[['Количество (из акта)','Материал']].sum()
            added.reset_index(drop = False, inplace = True)
            for index, row in added.iterrows():
               yar_stat.loc[ yar_stat['Код товара']==row['Код товара'], key ] += row['Количество (из акта)']

      yar_stat.to_excel('yar_stat.xlsx', index=False)



      
