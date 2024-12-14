def corrections(transactions):
    ### 1.Постоянные исключения для материальных отчётов
    transacts = transactions.loc[ transactions['Код товара']!='00nan'].copy() 
    #Электроды кг -> тн
    transacts.loc[ transacts['Код товара']=='05140', 'Quantity' ] /= 1000
    transacts.loc[ transacts['Код товара']=='05140', 'Ед.изм.' ] = 'тн'

    #До перехода Миржахона, часть материала была уже списана
    transacts.loc[ transacts['Reservation Number'] == 5388, 'Quantity' ] = 162
    transacts.loc[ transacts['Reservation Number'] == 4450, 'Quantity' ] = 4794.598

    #Корректировка после перехода Миржахона
    transacts.loc[ (transacts['WO №'].isin([52090, 84634, 94411])) & (transacts['Reserved By']=='Mirjakhon Toirov'), 'Reserved By' ] = 'Mirjahon Toirov CofE'
    transacts.loc[ transacts['Reservation Number'].isin([6801,7605,7609,6802,6804,6805,6806,7237,7244,7604,7608,7238,7245,7611,7612,7650,7651,8477,8478,9088,9089,9092,7992,7993,8333,
                                                         8334,8851,9140,9157,9160,9158,9162,9159,9161,7752,8475 ]), 'Reserved By' ] = 'Mirjahon Toirov CofE'

    #Корректировка рулон цинковый 0.002 разница
    transacts.loc[ transacts['Reservation Number'] == 11217, 'Quantity'  ] = 0
    


    ### 2.Временные исключения для материальных отчётов
    
    #Тулкинакя, будет возврат на склад
    transacts.loc[ transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]), 'Work Order Status Description' ] = 'Pending for return'
    transacts.loc[ (transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactYear' ] = 2026
    
    #Это ОС
    transacts = transacts.loc[ transacts['Reservation Number'] != 15589 ]
    transacts = transacts.loc[ transacts['Reservation Number'] != 16946 ]

    #Не списывать CofE 4 AP
    transacts.loc[ transacts['Reservation Number'].isin([17113,16761,17100]), 'closedMonth' ] = 12

    #Забыл, списать в декабре
    transacts.loc[ transacts['Reservation Number'].isin([17048,]), 'closedMonth' ] = 12

    #Возврат 2 гаскета Мансур хасанов
    transacts.loc[ (transacts['Reservation Number'].isin([15594,]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactMonth' ] = 11
    #Возврат 8 и 4 гаскета Мансур хасанов Жду письмо
    transacts.loc[ transacts['Reservation Number'].isin([15581,15582,]), 'closedMonth' ] = 12
    transacts.loc[ (transacts['Reservation Number'].isin([15581,15582,]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactMonth' ] = 12


    #Ошибка в данных CMMS
    transacts.loc[ transacts['Reservation Number'].isin([13244,13245]), 'closedYear' ] = 2024
    transacts.loc[ transacts['Reservation Number'].isin([13244,13245]), 'closedMonth' ] = 11
    #трубы с измененной ед.изм
    transacts.loc[ transacts['Reservation Number'].isin([15545,]), 'Quantity' ] *= -1
    #транзакции почему то позже отчётного месяца
    transacts.loc[ transacts['Reservation Number'].isin([17445,17444,17446,17179,17447]), 'transactMonth' ] = 11
    



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


]


inactive_Master_Reservations  = [
### CofE
787,788,846,851,857,904,905,908,935,954,986,1009,1129,1311,1312,1313,1314,1341,1342,1343,1424,1426,1439,1443,1551,1560,1593,1594,1598,1599,1603,1629,1631,1697,1698,1710,1848,
1849,1852,2278,2307,2335,2648,2649,2679,2816,2908,2955,2956,2957,2959,3146,3147,3148,3203,3204,5527,5528,5536,782,6161,6162,7657,
6744,6766,6773,6828,6917,6985,7104,7299,7300,7301,7554,
8580,
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
            {'Код товара':'12814','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Алюминий",'Ед.изм.':'кг','Quantity':5.3,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'12813','Reservation Number':-2,'WO №':-2,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Мис",'Ед.изм.':'кг','Quantity':7.87,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'12815','Reservation Number':-3,'WO №':-3,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Нержавекеющая сталь",'Ед.изм.':'кг','Quantity':0.84,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
        ],
        'currentMonth':[
            #Бумага а4
            {'Код товара':'06944','Reservation Number':-4,'WO №':-4,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':4,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            #Алюминий 14{'Код товара':'29422','Reservation Number':-6,'WO №':-6,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Алюмин 14",'Ед.изм.':'т','Quantity':1.9202,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Никель{'Код товара':'11064','Reservation Number':-7,'WO №':-7,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Никель",'Ед.изм.':'т','Quantity':1.1104,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Медь 13{'Код товара':'21883','Reservation Number':-8,'WO №':-8,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Медь 13",'Ед.изм.':'т','Quantity':0.1639,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
        
            #Новые инструменты после инвентаризации
            {'Код товара':'30741', 'Reservation Number':-5,'WO №':-5,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 3', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30742', 'Reservation Number':-6,'WO №':-6,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 15/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30743', 'Reservation Number':-7,'WO №':-7,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 13/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30744', 'Reservation Number':-8,'WO №':-8,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 11/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30745', 'Reservation Number':-9,'WO №':-9,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 9/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30746', 'Reservation Number':-10,'WO №':-10,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 7/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30747', 'Reservation Number':-11,'WO №':-11,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 5/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30748', 'Reservation Number':-12,'WO №':-12,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 5/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30749', 'Reservation Number':-13,'WO №':-13,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 3/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30750', 'Reservation Number':-14,'WO №':-14,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 3/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30751', 'Reservation Number':-15,'WO №':-15,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 3/4', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30752', 'Reservation Number':-16,'WO №':-16,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 1/4', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30753', 'Reservation Number':-17,'WO №':-17,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 1/2', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30754', 'Reservation Number':-18,'WO №':-18,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 1/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30755', 'Reservation Number':-19,'WO №':-19,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 1/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30756', 'Reservation Number':-20,'WO №':-20,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30757', 'Reservation Number':-21,'WO №':-21,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 15/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30758', 'Reservation Number':-22,'WO №':-22,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 13/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30759', 'Reservation Number':-23,'WO №':-23,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 11/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30760', 'Reservation Number':-24,'WO №':-24,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 9/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30761', 'Reservation Number':-25,'WO №':-25,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 7/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30762', 'Reservation Number':-26,'WO №':-26,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 7/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30763', 'Reservation Number':-27,'WO №':-27,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 5/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30764', 'Reservation Number':-28,'WO №':-28,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 5/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30765', 'Reservation Number':-29,'WO №':-29,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 3/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30766', 'Reservation Number':-30,'WO №':-30,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 3/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30767', 'Reservation Number':-31,'WO №':-31,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 3/4', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30768', 'Reservation Number':-32,'WO №':-32,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30769', 'Reservation Number':-33,'WO №':-33,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/16', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30770', 'Reservation Number':-34,'WO №':-34,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30771', 'Reservation Number':-35,'WO №':-35,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/4', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30772', 'Reservation Number':-36,'WO №':-36,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/2', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30773', 'Reservation Number':-37,'WO №':-37,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 9/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30774', 'Reservation Number':-38,'WO №':-38,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 5/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30775', 'Reservation Number':-39,'WO №':-39,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 7/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30776', 'Reservation Number':-40,'WO №':-40,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/2', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30777', 'Reservation Number':-41,'WO №':-41,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 3/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30778', 'Reservation Number':-42,'WO №':-42,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 3/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30779', 'Reservation Number':-43,'WO №':-43,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 3/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30780', 'Reservation Number':-44,'WO №':-44,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 5/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30781', 'Reservation Number':-45,'WO №':-45,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/4', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30782', 'Reservation Number':-46,'WO №':-46,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/8', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30783', 'Reservation Number':-47,'WO №':-47,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 15/16', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30784', 'Reservation Number':-48,'WO №':-48,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30785', 'Reservation Number':-49,'WO №':-49,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 3/4', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30786', 'Reservation Number':-50,'WO №':-50,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 7/8', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30787', 'Reservation Number':-51,'WO №':-51,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1 1/16', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30788', 'Reservation Number':-52,'WO №':-52,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1/31', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30789', 'Reservation Number':-53,'WO №':-53,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 1/13', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30790', 'Reservation Number':-54,'WO №':-54,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Насос для масла', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30791', 'Reservation Number':-55,'WO №':-55,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Микрометр 0-25 мм', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30792', 'Reservation Number':-56,'WO №':-56,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Штангенциркуль 0-300 мм', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30793', 'Reservation Number':-57,'WO №':-57,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Разводной ключ 300x36', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30794', 'Reservation Number':-58,'WO №':-58,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 2 7/8', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30795', 'Reservation Number':-59,'WO №':-59,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Головка 60', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30796', 'Reservation Number':-60,'WO №':-60,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Цепной ключ большой', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30797', 'Reservation Number':-61,'WO №':-61,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 60', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30798', 'Reservation Number':-62,'WO №':-62,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Верёвочная лесенка 6мм', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30799', 'Reservation Number':-63,'WO №':-63,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ динамометрический 300/1500', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30800', 'Reservation Number':-64,'WO №':-64,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 46', 'Ед.изм.':'шт', 'Quantity':4, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30801', 'Reservation Number':-65,'WO №':-65,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 41', 'Ед.изм.':'шт', 'Quantity':13, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30802', 'Reservation Number':-66,'WO №':-66,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 60', 'Ед.изм.':'шт', 'Quantity':10, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30803', 'Reservation Number':-67,'WO №':-67,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 55', 'Ед.изм.':'шт', 'Quantity':4, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30804', 'Reservation Number':-68,'WO №':-68,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 50', 'Ед.изм.':'шт', 'Quantity':14, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30805', 'Reservation Number':-69,'WO №':-69,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 80', 'Ед.изм.':'шт', 'Quantity':14, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30806', 'Reservation Number':-70,'WO №':-70,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 75', 'Ед.изм.':'шт', 'Quantity':10, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30807', 'Reservation Number':-71,'WO №':-71,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 60', 'Ед.изм.':'шт', 'Quantity':13, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30808', 'Reservation Number':-72,'WO №':-72,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 65', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30809', 'Reservation Number':-73,'WO №':-73,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 55', 'Ед.изм.':'шт', 'Quantity':10, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30810', 'Reservation Number':-74,'WO №':-74,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Рожковый под молоток 50', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30811', 'Reservation Number':-75,'WO №':-75,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 41', 'Ед.изм.':'шт', 'Quantity':8, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30812', 'Reservation Number':-76,'WO №':-76,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной набор 6/7-36/41', 'Ед.изм.':'шт', 'Quantity':9, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30813', 'Reservation Number':-77,'WO №':-77,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 36/41', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30814', 'Reservation Number':-78,'WO №':-78,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 36/32', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30815', 'Reservation Number':-79,'WO №':-79,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 22/24', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30816', 'Reservation Number':-80,'WO №':-80,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 22/19', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30817', 'Reservation Number':-81,'WO №':-81,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ30/32', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30818', 'Reservation Number':-82,'WO №':-82,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной гаечный ключ 17/16', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30819', 'Reservation Number':-83,'WO №':-83,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной ключ 36', 'Ед.изм.':'шт', 'Quantity':4, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30820', 'Reservation Number':-84,'WO №':-84,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной ключ 32', 'Ед.изм.':'шт', 'Quantity':15, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30821', 'Reservation Number':-85,'WO №':-85,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной ключ 27', 'Ед.изм.':'шт', 'Quantity':7, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30822', 'Reservation Number':-86,'WO №':-86,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной ключ 22', 'Ед.изм.':'шт', 'Quantity':7, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30823', 'Reservation Number':-87,'WO №':-87,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Накидной под молоток 110', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30824', 'Reservation Number':-88,'WO №':-88,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Съёмник 300', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30825', 'Reservation Number':-89,'WO №':-89,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Распорка большая', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30826', 'Reservation Number':-90,'WO №':-90,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Распорка маленькая', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30827', 'Reservation Number':-91,'WO №':-91,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Лампа 220', 'Ед.изм.':'шт', 'Quantity':12, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30828', 'Reservation Number':-92,'WO №':-92,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Мегаомметр', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30829', 'Reservation Number':-93,'WO №':-93,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Вентилятор пушка', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30830', 'Reservation Number':-94,'WO №':-94,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Цепной ключ маленький', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30831', 'Reservation Number':-95,'WO №':-95,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Фланцевый уровень большой', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30832', 'Reservation Number':-96,'WO №':-96,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Фланцевый уровень маленький', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30833', 'Reservation Number':-97,'WO №':-97,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ 24', 'Ед.изм.':'шт', 'Quantity':6, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30834', 'Reservation Number':-98,'WO №':-98,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ 27', 'Ед.изм.':'шт', 'Quantity':8, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30835', 'Reservation Number':-99,'WO №':-99,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ 17', 'Ед.изм.':'шт', 'Quantity':8, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30836', 'Reservation Number':-100,'WO №':-100,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ 32', 'Ед.изм.':'шт', 'Quantity':5, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30837', 'Reservation Number':-101,'WO №':-101,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Ключ 19', 'Ед.изм.':'шт', 'Quantity':9, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30838', 'Reservation Number':-102,'WO №':-102,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Шестигранник 17', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30839', 'Reservation Number':-103,'WO №':-103,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Кувалда 5 кг', 'Ед.изм.':'шт', 'Quantity':3, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30840', 'Reservation Number':-104,'WO №':-104,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Кувалда 3 кг', 'Ед.изм.':'шт', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},
            {'Код товара':'30841', 'Reservation Number':-105,'WO №':-105,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Таль 20', 'Ед.изм.':'шт', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'Инвентаризация','Asset Description':'Новые инструменты', 'Объект':'Новые инструменты'},

            {'Код товара':'07139', 'Reservation Number':-106,'WO №':-106,'closedMonth':12,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Спец.обувь мужские для рабочих,ГОСТ 28507-99', 'Ед.изм.':'пара', 'Quantity':2, 'Отдел':'RMPD','Reserved By':'RMPD','Asset Description':'Xasanov M, Shopulatov J', 'Объект':'Xasanov M, Shopulatov J'},
            {'Код товара':'06899', 'Reservation Number':-107,'WO №':-107,'closedMonth':12,'closedYear':2024,'Work Order Status Description':'Closed','Материал':'Куртка мужская с логотипом', 'Ед.изм.':'комплект', 'Quantity':1, 'Отдел':'RMPD','Reserved By':'RMPD','Asset Description':'Timur Isxakov', 'Объект':'Cost Controller'},
        ],
        'currentReturn':[]
    },
    'cofe':{
        'begin':[
            #Корректировка кислород
            {'Код товара':'13688','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Кислород газообразный",'Ед.изм.':'м³','Quantity':0.12,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Корректировка Кислород', 'Объект':'Корректировка Кислород'},
            
            #Diesel
            {'Код товара':'06933','Reservation Number':-2,'WO №':-2,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':40,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            #{'Код товара':'09683','Reservation Number':-2,'WO №':-2,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':0.036,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
            
        ],
        'currentMonth':[
            #Бумага
            {'Код товара':'06944','Reservation Number':-3,'WO №':-3,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':4,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Бумага', 'Объект':'Бумага'},
            
            #Diesel
            {'Код товара':'06933','Reservation Number':-4,'WO №':-4,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':678.53,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            {'Код товара':'06933','Reservation Number':-5,'WO №':-5,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':301.47,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            {'Код товара':'09683','Reservation Number':-6,'WO №':-6,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':24.244,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
        
            #Аргонбаллон
            {'Код товара':'01874','Reservation Number':-7,'WO №':-7,'closedMonth':11,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Аргон баллон 50л",'Ед.изм.':'шт','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Аргон баллон', 'Объект':'Аргон баллон'},
            ],
        'currentReturn':[]
    },
}
