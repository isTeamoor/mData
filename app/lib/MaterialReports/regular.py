import pandas as pd
from ...database.DF__spares import spares
from ...database.DF__wo import wo
from ...database.DF__assets import unitChild
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
  transactions['TempSave'] = transactions.apply(lambda x: 'yes' if x['Reservation Number'] in reference.tempSave[department] else 'no', axis=1)
  transactions['TempSave'] = transactions.apply(lambda x: 'yes' if x['Код товара'] in reference.tempSaveLimits[department].keys() 
                                                               and x['WO №'] == reference.tempSaveLimits[department][x['Код товара']]['wo'] else x['TempSave'], axis=1)
  transactions.loc[ transactions['TempSave']=='yes'].to_excel('2. tempSave_report.xlsx')
  
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
      print(row)
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





  ### 9. Вычисление сумм
  #Исключения цена расхода
  if department == 'cofe':
    rep.loc[ rep['Код товара']=='06933', 'Цена' ] = 0

    rep.loc[ rep['Код товара']=='11062', 'Цена' ] = 55465.80738795397
    #rep.loc[ rep['Код товара']=='14457', 'Цена' ] = 88756.6174375 

  if department == 'rmpd':
    rep.loc[ rep['Код товара']=='12813', 'Цена' ] = 41768.6741713571
    rep.loc[ rep['Код товара']=='12814', 'Цена' ] = 7846.732666666667


  rep['Сумма начало']  = rep['Кол-во начало']  * rep['Цена']
  rep['Сумма приход']  = rep['Кол-во приход']  * rep['Цена']
  rep['Сумма расход']  = rep['Кол-во расход']  * rep['Цена']
  rep['Сумма 014']     = rep['Кол-во 014']     * rep['Цена']
  rep['Сумма конец']   = rep['Кол-во конец']   * rep['Цена']

  ### Exception different prices in 1c
  if department == 'cofe':
      #Аргон 11062
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 56147.14380812033     if x['Код товара']=='11062' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 54017.85712742981  if x['Код товара']=='11062' else x['Сумма приход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 56147.14380812033  if x['Код товара']=='11062' else x['Сумма конец'], axis=1)
      #Кислород газообразный 13688
      #rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 9367.529880478088   if x['Код товара']=='13688' else x['Сумма начало'], axis=1)
      #rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 9375  if x['Код товара']=='13688' else x['Сумма приход'], axis=1)
      #rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 8774.932003626473  if x['Код товара']=='13688' else x['Сумма конец'], axis=1)
      #Кислород газообразный 14457
      #rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 88982.6584962406   if x['Код товара']=='14457' else x['Сумма приход'], axis=1)
      #rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 89323.85254716981   if x['Код товара']=='14457' else x['Сумма конец'], axis=1)
      #Кислород баллон 01876
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 2688047.208     if x['Код товара']=='01876' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 1   if x['Код товара']=='01876' else x['Сумма приход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 1008018.328   if x['Код товара']=='01876' else x['Сумма конец'], axis=1)
  if department == 'rmpd':
      #Мис 12813
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 18500   if x['Код товара']=='12813' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 42000  if x['Код товара']=='12813' else x['Сумма приход'], axis=1)
      #Алюминий 12814
      rep['Сумма начало'] = rep.apply(lambda x: x['Кол-во начало'] * 5000   if x['Код товара']=='12814' else x['Сумма начало'], axis=1)
      rep['Сумма приход'] = rep.apply(lambda x: x['Кол-во приход'] * 8032.740767045455  if x['Код товара']=='12814' else x['Сумма приход'], axis=1)
      rep['Сумма конец'] = rep.apply(lambda x: x['Кол-во конец'] * 5000  if x['Код товара']=='12814' else x['Сумма конец'], axis=1)
      



  ### 10. Завершение подготовки базового DF

  rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
              'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
              'closedMonth','Отдел','Reserved By','is014','iswOff','WO №','Asset Description', 'Объект', 'Кол-во возврат']]
  
  """
  ### !!! Exception steel angle 003 & 1040 accounts
  row1 = {'Account':'003.1 (Материалы на складе)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':1,
          'Кол-во начало':1000,'Сумма начало':1000,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':1000,'Сумма расход':1000,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':22838,
          'Work Order Status Description':'Closed','closedMonth':10,
          'Отдел':'Cofe-Jet Wash','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':137433,'Asset Description':'Washing buy area ', 'Объект':'WBA', 'Кол-во возврат':0}
  row2 = {'Account':'1040 (Запасные части)',
          'Код товара':'29137',
          'Материал':'STEEL ANGLE - MATERIAL : HOT DIP GALVANIZED 50 x 50 x 6T (5000nmm)  / Уголок из стали - материал: горячеоцинкованная сталь 50 x 50 x 6T (5000 мм)',
          'Ед.изм.':'Meter',
          'Цена':74323.4350833333,
          'Кол-во начало':120,'Сумма начало':8918812.21,
          'Кол-во приход':0,'Сумма приход':0,
          'Кол-во расход':120,'Сумма расход':8918812.21,'Кол-во 014':0, 'Сумма 014':0,
          'Кол-во конец':0,'Сумма конец':0, 
          'Reservation Number':23322,
          'Work Order Status Description':'Closed','closedMonth':10,
          'Отдел':'Cofe-Jet Wash','Reserved By':'Boburjon Aralov Akbar o`g`li',
          'is014':'','iswOff':'','WO №':137433,'Asset Description':'Washing buy area ', 'Объект':'WBA', 'Кол-во возврат':0}
  if department=='cofe':
    rep = rep.loc[ rep['Код товара']!='29137']
    rep = pd.concat([rep, pd.DataFrame(row1, index=[0])]).reset_index(drop=True)
    rep = pd.concat([rep, pd.DataFrame(row2, index=[0])]).reset_index(drop=True)
  """

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

  ### C включением WO description
  dalolat_mod = rep.loc[ (rep['Кол-во расход']>0) & (rep['iswOff']!='yes') ].copy()
  dalolat_mod['Кол-во расход'] = dalolat_mod['Кол-во расход'] - dalolat_mod['Кол-во возврат']
  dalolat_mod = dalolat_mod.loc [ dalolat_mod['Кол-во расход'] !=0 ]
  
  dalolat_mod['Кол-во всего'] = dalolat_mod['Код товара'].copy().map(  lambda x: dalolat_mod.loc[ dalolat_mod['Код товара'] == x, 'Кол-во расход' ].sum() )
  
  dalolat_mod = dalolat_mod[['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By','Цена', 'Сумма расход']]
  # Добавляем WO Description
  dalolat_mod = dalolat_mod.merge(wo[['Work Order Number','Work Order Description']], how = 'left', left_on='WO №', right_on='Work Order Number' )
  dalolat_mod = dalolat_mod.fillna({'WO №':0, 'Work Order Description':'Custom'})
  # Проход по assets
  dalolat_mod['Facility'] = 'х'
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'SLU' if x['Объект'] in unitChild('SLU') else x['Facility'],axis=1)
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'U&O' if x['Объект'] in unitChild('U&O') else x['Facility'],axis=1)
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'PWU' if x['Объект'] in unitChild('PWU') else x['Facility'],axis=1)
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'Buildings' if x['Объект'] in unitChild('Buildings') else x['Facility'],axis=1)
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'Warehouse' if x['Объект'] in unitChild('Warehouse') else x['Facility'],axis=1)
  dalolat_mod['Facility'] = dalolat_mod.apply(lambda x: 'AUTOMATION' if x['Объект'] in unitChild('AUTOMATION') else x['Facility'],axis=1)
  dalolat_mod = dalolat_mod.groupby(['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект','Facility', 'Reserved By','Work Order Description']).sum()





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


  wOff_Mn['Сумма расход'] = wOff_Mn['Цена'] * wOff_Mn['Кол-во расход']
      
  wOff_Ap = wOff_Ap[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]
  wOff_Mn = wOff_Mn[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход','Comment']]





  ### 14. Раздача. Не связан с TempSave reference.tempSaveLimits, только reference.tempSave!
  handover = rep.loc[ (rep['Кол-во 014']>0)
                      |
                      (
                         (rep['Кол-во расход']>0) & (rep['iswOff']=='yes')
                      ) 
                     ].copy()
  handover = handover.loc[ ~(handover['Reservation Number'].isin(reference.tempSave[department])) ]
  handover.insert(1,'Примечание', 'Reserved by '+handover['Reserved By']+' WO № '+handover['WO №'].astype(str)+' Reservation № '+handover['Reservation Number'].astype(str))
  handover = handover[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014','Кол-во расход', 'Примечание']]

  """#TempSave handover
  tempSaveHO = rep.loc[ (rep['Кол-во 014']>0)
                      |
                      (
                         (rep['Кол-во расход']>0) & (rep['iswOff']=='yes')
                      ) 
                     ].copy()
  tempSaveHO = tempSaveHO.loc[ tempSaveHO['Reservation Number'].isin(reference.tempSave[department]) ]
  tempSaveHO.insert(1,'Примечание', 'Reserved by '+tempSaveHO['Reserved By']+' WO № '+tempSaveHO['WO №'].astype(str)+' Reservation № '+tempSaveHO['Reservation Number'].astype(str))
  tempSaveHO = tempSaveHO[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014','Кол-во расход', 'Примечание']]"""




  ### 14. Ввод в эксплуатацию. Не связан с TempSave reference.tempSaveLimits, только reference.tempSave!
  to014 = rep.loc[ rep['Кол-во 014']>0 ].copy()
  #to014 = to014.loc[ ~(to014['Reservation Number'].isin(reference.tempSave[department])) ]
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]
  to014['Объект'] = ''
  to014 = to014.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  to014.reset_index(drop=False, inplace=True)
  to014 = to014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]

  """#TempSave
  tempSave = rep.loc[ rep['Кол-во 014']>0 ].copy()
  tempSave = tempSave.loc[ tempSave['Reservation Number'].isin(reference.tempSave[department]) ] 
  tempSave = tempSave[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]
  tempSave['Объект'] = ''
  tempSave = tempSave.groupby(['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена']).sum()
  tempSave.reset_index(drop=False, inplace=True)
  tempSave = tempSave[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Кол-во 014', 'Цена', 'Сумма 014']]"""


  cheQ.to_excel('cheQ.xlsx', index=False)
  check.to_excel('2. check.xlsx', index=False)
  matRep.to_excel('3. matRep.xlsx', index=False)
  dalolat.to_excel('4. dalolat.xlsx')
  dalolat_mod.to_excel('4. dalolat_mod.xlsx')
  handover.to_excel('4. handover.xlsx', index=False)
  to014.to_excel('4. 014.xlsx', index=False)
  wOff_Ap.to_excel('4. wOff_AP.xlsx', index=False)
  wOff_Mn.to_excel('4. wOff_Mn.xlsx', index=False)
  reference.OneCW()
  """tempSaveHO.to_excel('4. tempSaveHO.xlsx', index=False)
  tempSave.to_excel('4. tempSave.xlsx', index=False)"""
  



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
      yaroq.to_excel('5. yaroq.xlsx', index=False)

      
      """yaroq_report = yaroq.copy()
      yaroq_report = yaroq_report.loc[ ~(yaroq_report['info'].isna()) ]
      yaroq_report = yaroq_report.fillna('')
      yaroq_report['checksum'] = yaroq_report.apply(lambda x: yaroq_report.loc[ yaroq_report['Код товара']==x['Код товара'],
                                                                                'Количество (из акта)' ].sum(), axis=1)
      yaroq_report = yaroq_report.groupby(['Код товара','Материал','info',
                                           'На уничтожение','В повторное использование','На металл',
                                           'Кол-во расход','checksum',
                                           'Номер документа','Номер файла','Материал (из акта)',]).sum()
      yaroq_report.to_excel('5. yaroq_report.xlsx')"""

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

      """yar_stat = yar_stat.groupby(['Код товара','Catalogue Number','Материал','Ед.изм.','Количество (из акта)','Кол-во всего',])[['Asset Description','Объект',]].sum()
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
"""


      
