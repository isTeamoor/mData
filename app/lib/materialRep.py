import pandas as pd
import numpy as np

### Номера Reservations, материалы по которым уже списаны
inactive = [
771,848,937,938,939,1049,1050,1051,1114,1272,1320,1322,1452,1592,1609,3798,1871,1873,1874,1902,1922,1924,2356,2306,2355,2826,3806,3843,2859,2873,3088,3093,3927,3135,3242,3797,3826,3983,3827,
3845,3977,3978,3979,3980,4346,4347,4348,4349,4038,4039,4040,4041,4042,4043,4125,4126,4159,4178,4194,4182,4198,4251,4252,4324,4325,921,2357,3227,3257,1126,885,1901,1921,1923,756,
]

to_014 = ['6935','5841','7139','5230','4189','3494','2799','5749','1738','1308','1309','1310','1311','1312','1329','1330','1331','1333','1351','1354','1372','1374','1376','1377','1378','892','2204',
'4179','0158','0140','0134','0114','0915','1278','1276','1275','1277','1272','1279','3190','2995','2806','2812','2813','2814','2826','2827','2828','2830','2896','2897','1307','1353','1373', '3904',
'1375','2325','1393','3484','3017','2786','3019','4662','0899','3745','1367','2890','2891','2892','2893','2894','2452','2092','2451','2817','0155','0156','0526','0002','4188','2910','6597', '7277',
'1622','1625','1623','1626','1624','3222','1628','1630','1627','1632','0009','0001','4346','6860','1274','1273','1352','2854','2863','2885','3480','1349','3226','2824','2935','1344','6601', '6600',
'1337','1313','1315','1316','1317','1320','1321','1322','1323','1325','1326','1327','1568','1635','1570','1571','1588','1590','1591','1636','1603','1604','1621','2804','2807','2809','2815', '6598',
'2816','2818','2819','2820','2821','2822','2823','2831','2834','2840','2845','2846','2847','2848','2851','2856','2858','2860','2861','2864','2878','2880','2881','2882','2883','2884','2886', '6599',
'2887','2888','2899','2900','2901','2902','2903','2906','2936','3260','0809','0810','2453','0678','0157','0203','0113','0158','0159','6136','1575','1578','0154','6899','2450','5359','6799',
'3227','1379','1382','1314','1319','2879','1366','2857','2865','0007','0008','5942','4140','5752','6330','1189','1324','0865','1369','0863','1355','1387','0804','1587','1328',
'1332','2829','1406','0806','0805','1338','1342','1343','1339','1340','1341','2855','2852','3223','2862','1334','1335','1336','2850','2859','2853','1403','1574','1576','1577','1582','1360',
'1361','1364','1365','1429','1407','0691','0692','0693','0694','0695','0700','0703','0702','0705','0706','0707','0708','1350','1371','1380','1381','1383','1384','1385','1386','1394', '1395',
'1396','1398','1399','1589','1639','1606','1620','2835','0189','0745','0140','0230','0738','5232','5231','0899','0155','0114','0157','0526','0113','1201','1202','1203','1204','6340','2911',
'2912','2913','7481','7407','7473','7403','2802','3229','5305','6122','6332','6900','7497','7883','7882',
]






def matReport(repMonth, repYear, transactions):
    ### 0. Исключение (забыл добавить в далолатнома в августе)
    transactions.loc [ transactions['Reservation Number']==3269, 'closedMonth' ] = 9

    
    ### 1. Подготовка DF Transactions
    transactions  = transactions.loc [ ((transactions['Catalogue Transaction Action Name'] == 'Issue') | (transactions['Catalogue Transaction Action Name'] == 'Return to Stock'))
                                    & (transactions['transactYear'] == repYear)
                                    & (transactions['isRMPD'] == 'yes')
                                    & (transactions['Reserved By'] != 'Mirjakhon Toirov') & (transactions['Reserved By'] != 'Bobur Aralov')
                                    & (~transactions['Reservation Number'].isin(inactive))
                                    ]
    print(transactions.loc[ transactions['Reservation Number']==1591, 'Material Code' ])
    
    transactions  = transactions[['Material Code','Catalogue Description','UOMDescription','Quantity','Reservation Number','Work Order Status Description','closedMonth','transactMonth',
                                  'Short Department Name','Reserved By','Work Order Number','reservYear','reservMonth','Asset Description', 'Asset Number','Actual Quantity','closedYear']]
    
    transactions.rename(columns={'Material Code':'Код товара',
                                 'Catalogue Description':'Материал',
                                 'UOMDescription':'Ед.изм.',
                                 'Asset Number':'Объект', 
                                 'Short Department Name':'Отдел',
                                 'Work Order Number':'WO №', 
                                 'Actual Quantity': 'Кол-во'}, inplace=True)
    


    ### 2. Выборка транзакций на начало месяца и в течении месяца
    begin = transactions.loc[ (transactions['transactMonth'] < repMonth)
                            & ( 
                                (transactions['Work Order Status Description'] != 'Closed') 
                                | ( (transactions['Work Order Status Description'] == 'Closed') & ( (transactions['closedYear'] == repYear) & (transactions['closedMonth'] >= repMonth) ) )
                              )
                            ]
                        
    current = transactions.loc[(transactions['transactMonth'] == repMonth)]




    ### 3. Дополнительные транзакции, которые вводятся вручную как исключения
    begin_additional = [
    #{'Код товара':'','Материал':'','Ед.изм.':'','Quantity':0,'Reservation Number':0,'Work Order Status Description':'','closedMonth':0,'Отдел':'','Reserved By':'','WO №':0,'reservYear':2023,'reservMonth':0,'Asset Description':'', 'Объект':'',},
    {'Код товара':'4921','Материал':'Size: 1 1/2" (Size: 40mm) Gasket, 316L SS WND GRAPH FILL 316L SS I/R 316L SS O/R RF B16.20 CL600 4.5MM thickness (3.2MM RING) Spiral Wound','Ед.изм.':'шт','Quantity':2,'Reservation Number':431,'Work Order Status Description':'Closed','closedMonth':9,'Отдел':'SLU','Reserved By':'Ulugbek  Khamroev','WO №':2771,'reservYear':2023,'reservMonth':8,'Asset Description':'', 'Объект':'',},
    {'Код товара':'4973','Материал':'Size: 12" (Size: 300mm) Gasket, 316L SS WND GRAPH FILL CS I/R CS O/R RF B16.20 CL600 4.5MM thickness (3.2MM RING) Spiral Wound','Ед.изм.':'шт','Quantity':2,'Reservation Number':437,'Work Order Status Description':'Closed','closedMonth':9,'Отдел':'SLU','Reserved By':'Ulugbek  Khamroev','WO №':651,'reservYear':2023,'reservMonth':8,'Asset Description':'', 'Объект':'',},
    ]
    current_additional = [
    #{'Код товара':'','Материал':'','Ед.изм.':'','Quantity':0,'Reservation Number':0,'Work Order Status Description':'','closedMonth':0,'Отдел':'','Reserved By':'','WO №':0,'reservYear':2023,'reservMonth':0,'Asset Description':'', 'Объект':'',},
    ]

    for row in begin_additional:
        newRow = pd.DataFrame(row, index=[0])
        begin = pd.concat([begin, newRow]).reset_index(drop=True)
    for row in current_additional:
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
    rep = rep.merge(OneC(), on = 'Код товара', how = 'outer')
    rep[['Кол-во начало','Кол-во приход','Цена']] = rep[['Кол-во начало','Кол-во приход','Цена']].fillna(0)

    rep['Сумма начало'] = rep['Кол-во начало'] * rep['Цена']
    rep['Сумма приход'] = rep['Кол-во приход'] * rep['Цена']




    
    ### 7. Подготовка полей Расход
    rep['Кол-во расход'] = rep['Кол-во начало'] + rep['Кол-во приход']
    rep['Сумма расход']  = rep['Сумма начало'] + rep['Сумма приход']

    rep['is014'] = rep['Код товара'].copy().map(lambda x: 'yes' if x in to_014 else '')

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
           & (rep['closedMonth'] == repMonth), ['Кол-во конец','Сумма конец'] ] = 0




    ### 10. Завершение подготовки базового DF
    rep = rep[['Account','Код товара','Материал', 'Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход',
               'Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец', 'Reservation Number','Work Order Status Description',
                'closedMonth','Отдел','Reserved By','is014','WO №','reservYear','reservMonth','Asset Description', 'Объект',]]




    ### 11. Базовый файл с детализацией по Reservations
    check = rep




    ### 12. Подготовка итогового материального отчёта
    matRep = rep.groupby(['Код товара','Account','Материал','Ед.изм.','Цена']).sum()
    matRep.reset_index(drop=False, inplace=True)
    matRep = matRep[['Account','Код товара','Материал','Ед.изм.','Цена','Кол-во начало','Сумма начало','Кол-во приход','Сумма приход','Кол-во расход','Сумма расход','Кол-во 014', 'Сумма 014','Кол-во конец','Сумма конец',]]
    matRep['Account'].fillna('undef')

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
    view_014.insert(1,'Примечание', 'Reserved by '+view_014['Reserved By']+' WO № '+view_014['WO №'].astype(str)+' Reservation Number '+view_014['Reservation Number'].astype(str))
    view_014 = view_014[['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во 014', 'Сумма 014','Примечание']]





    ### 14. Представление списание для е-doc
    view_wOff = rep.loc[rep['Кол-во расход']>0] [['Код товара', 'Материал', 'Объект', "Ед.изм.", 'Цена', 'Кол-во расход', 'Сумма расход']]   



    
    check.to_excel('1. check.xlsx')
    matRep.to_excel('2. matRep.xlsx')
    dalolat.to_excel('4. dalolat.xlsx')
    view_014.to_excel('5. view_014.xlsx')
    view_wOff.to_excel('5. view_wOff.xlsx')
    





def OneC():
  prices = pd.read_excel("0. мунтазам.xlsx").rename(columns={'Unnamed: 1':'Kod', 'Unnamed: 2':'Name', 'Unnamed: 5':'Qty1', 'Unnamed: 6':'Sum1','Unnamed: 7':'Qty2', 'Unnamed: 8':'Sum2'}).iloc[16: ][['Kod', 'Name','Qty1','Sum1','Qty2','Sum2']]
  prices['Kod'] = prices['Kod'].astype(str)
  prices['Код товара'] = prices['Kod'].copy().map(lambda x: x[-4:])
  prices[['Sum1','Sum2','Qty1','Qty2']] = prices[['Sum1','Sum2','Qty1','Qty2']].fillna(0)
  prices['Цена'] = (prices['Sum1']+prices['Sum2'])/(prices['Qty1']+prices['Qty2'])

  prices['Account'] = prices['Kod']
  prices.loc[ ~prices['Name'].isna(), 'Account' ] = np.nan
  prices['Account'] = prices['Account'].ffill()

  prices = prices.loc[ ~prices['Name'].isna(), ['Account', 'Код товара', 'Цена'] ]
  return prices