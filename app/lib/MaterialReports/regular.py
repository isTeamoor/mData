import pandas as pd
import numpy as np
from ...lib.gen import filterDF
from ...database.DF__spares import spares
from . import exceptions
from . import reference
from . import groupped



def matReport(repMonth, repYear, department, transactions):

  transactions = exceptions.corrections(transactions)

  
  ### 1. Подготовка DF Transactions
  transactions  = transactions.loc[ ((transactions['Catalogue Transaction Action Name'] == 'Issue') | (transactions['Catalogue Transaction Action Name'] == 'Return to Stock'))
                                  & (transactions['transactYear'] == repYear)
                                  & (~transactions['Reservation Number'].isin(reference.inactive_Reservations))
                                  ]
  transactions = filterDF(transactions, reference.department_Filters[department])
  
  transactions = transactions[['Material Code','Catalogue Description','UOMDescription','Quantity','Reservation Number','Work Order Status Description','closedMonth','transactMonth',
                               'Short Department Name','Reserved By','Work Order Number','reservYear','reservMonth','Asset Description', 'Asset Number','closedYear','Estimated Quantity',
                               'Group WO number', 'Is Group Work Order','Spares Comment',]]

  transactions.rename(columns={'Material Code':'Код товара',
                                'Catalogue Description':'Материал',
                                'UOMDescription':'Ед.изм.',
                                'Asset Number':'Объект', 
                                'Short Department Name':'Отдел',
                                'Work Order Number':'WO №'}, inplace=True)
  
  transactions = groupped.spread(transactions, spares, reference.inactive_Master_Reservations)



  ### 2. Выборка транзакций на начало месяца и в течении месяца
  begin = transactions.loc[ (transactions['transactMonth'] < repMonth)
                          & ( 
                              (transactions['Work Order Status Description'] != 'Closed') 
                              | ((transactions['Work Order Status Description'] == 'Closed') & (transactions['closedMonth'] >= repMonth))
                            )
                          ]
  current = transactions.loc[transactions['transactMonth'] == repMonth]

  for row in exceptions.extra[department]['begin']:
      newRow = pd.DataFrame(row, index=[0])
      begin = pd.concat([begin, newRow]).reset_index(drop=True)
  for row in exceptions.extra[department]['currentMonth']:
      newRow = pd.DataFrame(row, index=[0])
      current = pd.concat([current, newRow]).reset_index(drop=True)





  ### 4. Получение суммы по количеству для каждой reservation
  begin   = begin.groupby(  ['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','Отдел','Reserved By','WO №','reservYear','reservMonth','Asset Description', 'Объект',]).sum()
  current = current.groupby(['Reservation Number','Код товара','Материал','Ед.изм.','Work Order Status Description','closedMonth','Отдел','Reserved By','WO №','reservYear','reservMonth','Asset Description', 'Объект',]).sum()

  begin.reset_index(drop=False, inplace=True)
  current.reset_index(drop=False, inplace=True)





  ### 5. Объединение "на начало" и "приход", 
  begin.rename(columns={'Quantity':'Кол-во начало'}, inplace=True)
  current.rename(columns={'Quantity':'Кол-во приход'}, inplace=True)
  
  rep = begin.merge(current, how='outer', on=['Код товара','Материал','Ед.изм.','Reservation Number','Work Order Status Description','closedMonth','Отдел','Reserved By','WO №','reservYear','reservMonth','Asset Description', 'Объект',])

  



  ### 6. Добавление цен и групп из 1с. Вычисление сумм на начало и Приход
  rep = rep.merge(reference.OneC(), on = 'Код товара', how = 'outer')  #OneC.columns = ['Account', 'Код товара', 'Цена']
  rep['is014'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in reference.is_014 else '')
  rep[['Кол-во начало','Кол-во приход','Цена']] = rep[['Кол-во начало','Кол-во приход','Цена']].fillna(0)

  rep['Сумма начало'] = rep['Кол-во начало'] * rep['Цена']
  rep['Сумма приход'] = rep['Кол-во приход'] * rep['Цена']




  ### 7. Подготовка полей Расход
  rep['Кол-во расход'] = rep['Кол-во начало'] + rep['Кол-во приход']
  rep['Сумма расход']  = rep['Сумма начало'] + rep['Сумма приход']

  rep.loc[  (rep['is014'] == 'yes')
          | (
            (rep['Work Order Status Description'] != 'Closed') | ((rep['Work Order Status Description'] == 'Closed') & (rep['closedMonth'] > repMonth))
            ), ['Кол-во расход','Сумма расход'] ] = 0





  ### 8. Подготовка полей 014
  rep['Кол-во 014'] = rep['Кол-во начало'] + rep['Кол-во приход']
  rep['Сумма 014']  = rep['Сумма начало'] + rep['Сумма приход']

  rep.loc[  ~(rep['is014'] == 'yes')
          | (
            (rep['Work Order Status Description'] != 'Closed') | ((rep['Work Order Status Description'] == 'Closed') & (rep['closedMonth'] > repMonth))
            ), ['Кол-во 014','Сумма 014'] ] = 0





  ### 9. Подготовка полей Конец
  rep['Кол-во конец'] = rep['Кол-во начало'] + rep['Кол-во приход']
  rep['Сумма конец']  = rep['Сумма начало'] + rep['Сумма приход']

  rep.loc[ (rep['Work Order Status Description'] == 'Closed')
          & (rep['closedMonth'] <= repMonth), ['Кол-во конец','Сумма конец'] ] = 0




  ### 10. Завершение подготовки базового DF
  rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
              'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
              'closedMonth','Отдел','Reserved By','is014','WO №','reservYear','reservMonth','Asset Description', 'Объект',]]




  ### 11. Базовый файл с детализацией по Reservations
  check = rep




  ### 12. Подготовка итогового материального отчёта
  rep[['Код товара','Account','Материал','Ед.изм.']] = rep[['Код товара','Account','Материал','Ед.изм.']].fillna('undefined')
  rep[['Цена']] = rep[['Цена']].fillna(9999999999999)
  matRep = rep.groupby(['Код товара','Account','Материал','Ед.изм.','Цена']).sum()
  matRep.reset_index(drop=False, inplace=True)
  matRep = matRep[['Account','Код товара','Материал','Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход','Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец',]]

  ### 12.1 Cуммирующие строки
  for acc in matRep['Account'].unique():
      matRep.loc[len(matRep)] = matRep.loc[ matRep['Account']==acc ].sum(numeric_only=True)
      matRep.loc[len(matRep)-1, 'Account'] = acc
  matRep.loc[len(matRep)] = matRep.loc[ matRep['Материал'].isna() ].sum(numeric_only=True)
  matRep.loc[len(matRep)-1, 'Материал'] = 'Жами'





  ### 13. Подготовка Акта ввода в эксплуатацию (внутренний)
  dalolat = rep.loc[ rep['Кол-во расход']>0 ].copy()
  
  dalolat['Кол-во всего'] = dalolat['Код товара'].copy().map(  lambda x: dalolat.loc[dalolat['Код товара'] == x, 'Кол-во расход'].sum() )

  dalolat = dalolat[['Код товара', 'Материал', "Ед.изм.",'Кол-во всего',"Отдел", 'WO №','Reservation Number', 'Кол-во расход','Asset Description', 'Объект', 'Reserved By','Цена']]
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
  view_wOff = rep.loc[rep['Кол-во расход']>0] [['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]   




  ### 15. Представление для накладной
  waybill = reference.OneCW()



  
  check.to_excel('2. check.xlsx')
  matRep.to_excel('3. matRep.xlsx')
  dalolat.to_excel('4. dalolat.xlsx')
  view_014.to_excel('4. view_014.xlsx')
  view_014_G.to_excel('4. view_014_G.xlsx')
  view_wOff.to_excel('4. view_wOff.xlsx')
  waybill.to_excel('4. waybill.xlsx')
    