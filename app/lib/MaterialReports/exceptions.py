def corrections(transactions):
    transacts = transactions.loc[ transactions['Код товара']!='00nan'].copy() 



    ### 1. Это ОС ##############################################################################################
    #CofE
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([15589,20309,
                                                                       20232,
                                                                       22884,23146,23147,23148,23149,23150,23152,
                                                                       24187,
                                                                       ])) ]
    #RMPD
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([16946,
                                                                       17501,17502,17503,17504,18755,20232])) ]
    ############################################################################################################




    ### 2. Единицы измерения ###################################################################################
    #Электроды кг -> тн
    transacts.loc[ transacts['Код товара']=='05140', 'Quantity' ] /= 1000
    transacts.loc[ transacts['Код товара']=='05140', 'Ед.изм.' ] = 'тн'
    ############################################################################################################




    ### 3. Переход Миржахона ###################################################################################
    #Часть материала была уже списана до меня
    transacts.loc[ transacts['Reservation Number'] == 5388, 'Quantity' ] = 162
    transacts.loc[ transacts['Reservation Number'] == 4450, 'Quantity' ] = 4794.598

    #Корректировка после перехода Миржахона
    transacts.loc[ (
                    (transacts['WO №'].isin([52090, 84634, 94411]))
                    )
                  & 
                  (
                    (transacts['Reserved By']=='Mirjakhon Toirov')
                    |
                    (transacts['Reserved By']=='Mirjahon Toirov Ilxom o`g`li')
                  ), 'Reserved By' ] = 'Mirjahon Toirov CofE'
    
    transacts.loc[ transacts['Reservation Number'].isin([6801,7605,7609,6802,6804,6805,6806,7237,7244,7604,7608,7238,7245,7611,7612,7650,7651,8477,8478,9088,9089,9092,7992,7993,8333,
                                                         8334,8851,9140,9157,9160,9158,9162,9159,9161,7752,8475 ]), 'Reserved By' ] = 'Mirjahon Toirov CofE'
   ############################################################################################################





    ### 4. Возвраты #############################################################################################
    #Листовые фильтры Мансур Хасанов, Тулкинакя
    transacts.loc[ transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]), 'Work Order Status Description' ] = 'Pending for return'
    transacts.loc[ (transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactYear' ] = 2026
    
    #Не списывать CofE 4 AP будут возвращать
    transacts.loc[ transacts['Reservation Number'].isin([17113,16761,17100]), 'Work Order Status Description' ] = 'Pending for return'
    
    #Взято со склада временное хранение. Учтено в файле Готовый отчёт
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([27599,])) ]
    ############################################################################################################

    
    

    ### 5. Технические ошибки ##################################################################################

    #Шохзод Юлдашев для SLU - он пока не в списке isRmpdPlaner
    transacts.loc[ transacts['Reservation Number'].isin([19189,19146,19193,19666,19724,20441,19660,19679,21116,
                                                         15560,19680,15145,20369,21117,
                                                         4731]), 'isRMPD_planner' ] = 'yes'
      
    #Ошибка со склада - 1 вместо 2. Номер накладной 1280
    transacts = transacts.loc[ ~(transacts['Catalogue Transaction ID'].isin([163811,])) ]

    #Временное хранение. Уктам Ильхомов. Блайнд. Должен был быть списан в сентябре, в последний момент изменили. В октябре
    transacts.loc[ transacts['Reservation Number'].isin([26964,]), 'closedMonth' ] = 10
    ############################################################################################################


    ### 6. AP ##################################################################################################   
    #Возврат бобура, прям перед закрытием августовского отчёта. УДалить еще в current вторую часть. Возврат по документам в сентябре
    transacts.loc[ transacts['Reservation Number'].isin([26767,]), 'Quantity' ] = 3
    transacts.loc[ transacts['Reservation Number'].isin([26767,]), 'closedMonth' ] = 9

    #Материалы из handover. Есть вторая часть в df transactions
    #transacts.loc[ transacts['Reservation Number'].isin([27583,27660,27465,27391,]), 'closedMonth' ] = 10
    ############################################################################################################

    return transacts


inactive_Reservations= [
### RMPD
771,848,937,938,939,1049,1050,1051,1114,1272,1320,1322,1452,1592,1609,3798,1871,1873,1874,1902,1922,1924,2356,2306,2355,2826,3806,3843,2859,2873,3088,3093,3927,3135,3242,3797,
3826,3983,3827,3845,3977,3978,3979,3980,4346,4347,4348,4349,4038,4039,4040,4041,4042,4043,4125,4126,4159,4178,4194,4182,4198,4251,4252,4324,4325,921,2357,3227,3257,1126,885,
1901,1921,1923,756,2045,2044, 465, 798, 799, 1067, 1273, 3215, 4570, 1441, 3216, 1097, 1077, 1069,6035,
15009,

### CofE
1538, 1756, 1847, 1946, 2695, 4554, 4555, 4556, 4557, 4684, 4685, 5244, 5311, 5418, 4014, 4116, 4117, 4155, 4245, 4394, 4396, 4463, 4620, 1350, 2886, 4015, 4761, 4763, 4765, 5362, 
2887, 4826, 4782, 4483, 3032, 3033, 3412, 3414, 3416, 3418, 3423, 3465, 3471, 3485, 3489, 3507, 3515, 3596, 3766, 4095, 3396, 3397, 3398, 3399, 3400, 3405, 3408, 3409, 3410, 3411, 
3413, 3420, 3422, 3424, 3428, 3434, 3455, 3457, 3460, 3470, 3472, 3475, 3479, 3482, 3483, 3486, 3490, 3513, 3516, 3519, 3521, 3524, 3552, 3591, 3597, 3767, 4480, 3545, 4119, 4623, 
4754, 5310, 5374, 5416, 4481, 4552, 1774, 4244, 1222, 1442, 1755, 1776, 1948, 2646, 4385, 4756, 5246, 5415, 1777, 2647, 4053, 4154, 4196, 4246, 4386, 4398, 4462, 4619, 4707, 4747, 
4755, 5417, 1791, 2323, 4749, 2916, 3020, 3097, 3180, 3184, 3544, 3624, 4047, 3910, 4401, 4037, 4081, 4115, 5430, 4118, 4140, 4397, 4402, 5248, 5249, 4403, 4465, 4404, 4461, 4621, 
4705, 5247, 5312, 5375, 4406, 4464, 4706, 4822, 4823, 4824, 4825, 5250, 5373, 5548, 1402, 2885, 4760, 4762, 4764, 4360, 3031, 8729, 8728, 9184,

### TAR
2478,2481,2483,2485,2565,2566,3730,2564,14743,14745,14748,14752,14755,14761,14764,14768,14784,14787,14782,
7519,7520,7521,7522,7523,7758,
2473,2475,2477,2479,2482,2484,2486,2567,3725,7502,7504,14740,14744,14747,14750,14754,14760,14763,14767,14781,14785,
14742,14746,14749,14753,14756,14762,14765,14770,14783,14786,17034,17035,17036,17037,17039,17041,17042,17043,17044,17045,
19732,19733,19734,19735,19736,19489,19488,19490,
22054,22055,22057,22058,22061,22064,22066,22068,22069,22081,

]


inactive_Master_Reservations  = [
### CofE
787,788,846,851,857,904,905,908,935,954,986,1009,1129,1311,1312,1313,1314,1341,1342,1343,1424,1426,1439,1443,1551,1560,1593,1594,1598,1599,1603,1629,1631,1697,1698,1710,1848,
1849,1852,2278,2307,2335,2648,2649,2679,2816,2908,2955,2956,2957,2959,3146,3147,3148,3203,3204,5527,5528,5536,782,6161,6162,7657,
6744,6766,6773,6828,6917,6985,7104,7299,7300,7301,7554,
8580,
### RMPD
2823,12369,12370,12371,12373,12377,13012,16535,16536,16787,16827,16829,16830,17141,17148,17149,17150,17155,18700,
18703,18896,18897,18907,18958,19103,19226,19295,19296,19297,19298,19308,19320,19333,19336,19398,19399,19409,19410,
19445,19492,19512,19513,19613,19861,20146,20207,20208,20210,20251,20340,20342,20347,20360,23112,
"""
#52090:
5388, 5877,6964,
#84634:
7910, 7912, 7913, 7915, 7916, 7918, 7919, 7920, 7921, 7922, 7923, 7963, 7694, 7965, 8068, 8140, 8141, 8228, 9083, 9318, 9511, 
#94411:
10138, 10340, 10341,
"""


]


extra = {
    #{'Код товара':'0','Reservation Number':-,'WO №':-,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"",'Ед.изм.':'','Quantity':0,'Отдел':'','Reserved By':"",'Asset Description':'undefined', 'Объект':'undefined'},
    # Current Return Qty со знаком "-"/Reservation number should be the same as original position!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    'rmpd':{
        'begin':[
            #Met
            {'Код товара':'12814','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Алюминий",'Ед.изм.':'кг','Quantity':5.3,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'12813','Reservation Number':-2,'WO №':-2,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Мис",'Ед.изм.':'кг','Quantity':7.87,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'12815','Reservation Number':-3,'WO №':-3,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Нержавекеющая сталь",'Ед.изм.':'кг','Quantity':0.84,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},

            #Extra Канцтовары
            #{'Код товара':'07139', 'Reservation Number':-4,'WO №':-4,'closedMonth':12,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Спец.обувь мужские для рабочих,ГОСТ 28507-99', 'Ед.изм.':'пара', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'RMPD','Asset Description':'Xasanov M, Shopulatov J', 'Объект':'Xasanov M, Shopulatov J'},
            #{'Код товара':'06899', 'Reservation Number':-5,'WO №':-5,'closedMonth':12,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Куртка мужская с логотипом', 'Ед.изм.':'комплект', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'RMPD','Asset Description':'Timur Isxakov', 'Объект':'Cost Controller'},
        
        ],
        'currentMonth':[
            #Бумага
            {'Код товара':'06944','Reservation Number':-4,'WO №':-4,'closedMonth':9,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':8,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            #{'Код товара':'31158','Reservation Number':-5,'WO №':-5,'closedMonth':5,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Бумага для офисной техники белая А3",'Ед.изм.':'пачка','Quantity':1,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            
            
            #Met
            #Алюминий 13
            #{'Код товара':'29422','Reservation Number':-6,'WO №':-6,'closedMonth':4,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Алюмин 13",'Ед.изм.':'т','Quantity':1.0006,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Никель 13
            #{'Код товара':'11064','Reservation Number':-7,'WO №':-7,'closedMonth':4,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Никель 13",'Ед.изм.':'т','Quantity':0.555,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Медь 13
            #{'Код товара':'21883','Reservation Number':-8,'WO №':-8,'closedMonth':4,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Медь 13",'Ед.изм.':'т','Quantity':0.7226,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Свинец 13
            #{'Код товара':'16797','Reservation Number':-6,'WO №':-6,'closedMonth':2,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Свинец 13",'Ед.изм.':'т','Quantity':0.527,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
        ],
        'currentReturn':[]
    },
    'cofe':{
        'begin':[
            #Корректировка кислород
            {'Код товара':'13688','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Кислород газообразный",'Ед.изм.':'м³','Quantity':0.12,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Корректировка Кислород', 'Объект':'Корректировка Кислород'},
            
            #Diesel
            #{'Код товара':'06933','Reservation Number':-2,'WO №':-2,'closedMonth':2,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':166,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            {'Код товара':'06933','Reservation Number':-3,'WO №':-3,'closedMonth':0,'closedYear':2025,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':20,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            #{'Код товара':'09683','Reservation Number':-4,'WO №':-4,'closedMonth':4,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':0.0199,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},

        ],
        'currentMonth':[
            #Бумага
            #{'Код товара':'06944','Reservation Number':-5,'WO №':-5,'closedMonth':7,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Бумага', 'Объект':'Бумага'},
            
            #Diesel
            {'Код товара':'06933','Reservation Number':-6,'WO №':-6,'closedMonth':9,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':200,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            #{'Код товара':'06933','Reservation Number':-8,'WO №':-8,'closedMonth':0,'closedYear':2025,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':20,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            {'Код товара':'09683','Reservation Number':-9,'WO №':-9,'closedMonth':9,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':28.804,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
        
            
            #Аргонбаллон
            #{'Код товара':'01874','Reservation Number':-9,'WO №':-9,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Аргон баллон 50л",'Ед.изм.':'шт','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Аргон баллон', 'Объект':'Аргон баллон'},
            
            #Половая тряпка
            #{'Код товара':'00094','Reservation Number':-10,'WO №':-10,'closedMonth':2,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Половая тряпка",'Ед.изм.':'м','Quantity':100,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Половая тряпка', 'Объект':'Половая тряпка'},
            
            ],
        'currentReturn':[
            #Половая тряпка
            #{'Код товара':'21165','Reservation Number':26767,'WO №':-999999,'closedMonth':9,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Возврат 21165",'Ед.изм.':'м','Quantity':-3,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'возврат', 'Объект':'возврат'},
            ]
    },
}
