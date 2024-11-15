def corrections(transactions):
    ### 1.Постоянные исключения для материальных отчётов
    transacts = transactions.loc[ transactions['Код товара']!='00nan'].copy() 
    #Электроды кг -> тн
    transacts.loc[ transacts['Код товара']=='05140', 'Quantity' ] /= 1000
    transacts.loc[ transacts['Код товара']=='05140', 'Ед.изм.' ] == 'тн'

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
    transacts.loc[ transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]), 'closedMonth' ] = 11
    transacts.loc[ (transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactMonth' ] = 11
    
    #Это ОС
    transacts = transacts.loc[ transacts['Reservation Number'] != 15589 ]



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
14742,14746,14749,14753,14756,14762,14765,14770,14783,14786,

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
            {'Код товара':'06944','Reservation Number':-5,'WO №':-5,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':10,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            {'Код товара':'29422','Reservation Number':-6,'WO №':-6,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Алюмин 14",'Ед.изм.':'т','Quantity':1.9202,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'11064','Reservation Number':-7,'WO №':-7,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Никель",'Ед.изм.':'т','Quantity':1.1104,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'21883','Reservation Number':-8,'WO №':-8,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Медь 13",'Ед.изм.':'т','Quantity':0.1639,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
        
        ],
        'currentReturn':[]
    },
    'cofe':{
        'begin':[
            {'Код товара':'13688','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Кислород газообразный",'Ед.изм.':'м³','Quantity':0.12,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Корректировка Кислород', 'Объект':'Корректировка Кислород'},
            {'Код товара':'09683','Reservation Number':-2,'WO №':-2,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':0.036,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
        ],
        'currentMonth':[
            {'Код товара':'29764','Reservation Number':-3,'WO №':-3,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Argon ballon (40 litr)",'Ед.изм.':'шт','Quantity':2,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29763','Reservation Number':-4,'WO №':-4,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Argon ballon (46,7 litr)",'Ед.изм.':'шт','Quantity':6,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29762','Reservation Number':-5,'WO №':-5,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Argon ballon (50 litr)",'Ед.изм.':'шт','Quantity':19,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29767','Reservation Number':-6,'WO №':-6,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (39,4 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29768','Reservation Number':-7,'WO №':-7,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40 litr)",'Ед.изм.':'шт','Quantity':6,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29769','Reservation Number':-8,'WO №':-8,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,2 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29770','Reservation Number':-9,'WO №':-9,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,3 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29771','Reservation Number':-10,'WO №':-10,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,5 litr)",'Ед.изм.':'шт','Quantity':4,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29772','Reservation Number':-11,'WO №':-11,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,6 litr)",'Ед.изм.':'шт','Quantity':3,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29773','Reservation Number':-12,'WO №':-12,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,7 litr)",'Ед.изм.':'шт','Quantity':2,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29774','Reservation Number':-13,'WO №':-13,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (40,8 litr)",'Ед.изм.':'шт','Quantity':3,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29775','Reservation Number':-14,'WO №':-14,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (41 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29776','Reservation Number':-15,'WO №':-15,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (41,1 litr)",'Ед.изм.':'шт','Quantity':2,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29777','Reservation Number':-16,'WO №':-16,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (41,4 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29778','Reservation Number':-17,'WO №':-17,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (42 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29779','Reservation Number':-18,'WO №':-18,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (46,7 litr)",'Ед.изм.':'шт','Quantity':17,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29780','Reservation Number':-19,'WO №':-19,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Azot ballon (50 litr)",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            
            {'Код товара':'06944','Reservation Number':-20,'WO №':-20,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':4,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Бумага', 'Объект':'Бумага'},
            
            {'Код товара':'29765','Reservation Number':-21,'WO №':-21,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Kislarod ballon 40 litr",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29766','Reservation Number':-22,'WO №':-22,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Propan ballon 50 litr",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29760','Reservation Number':-23,'WO №':-23,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Динамометрические ключи с реверсивным храповиком - Модель-QLE 1400 N2",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29759','Reservation Number':-24,'WO №':-24,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Динамометрические ключи с реверсивным храповиком - Модель-QLE 2100 N2",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29757','Reservation Number':-25,'WO №':-25,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Загибочный станок",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29755','Reservation Number':-26,'WO №':-26,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Зх вальковый станок",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29756','Reservation Number':-27,'WO №':-27,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Зх вальковый станок TAEYANGENG",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29739','Reservation Number':-28,'WO №':-28,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Комплект для испытания предохранительных клапанов ТPU3100-LP. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29740','Reservation Number':-29,'WO №':-29,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Компрессор воздушный трехпоршневой 5,5 КВТ 380 В",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29741','Reservation Number':-30,'WO №':-30,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Компрессор воздушный трехпоршневой 5,5 КВТ 380 В",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29742','Reservation Number':-31,'WO №':-31,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр образцовый МО-11202 0…1 Мпа",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29743','Reservation Number':-32,'WO №':-32,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр образцовый МО-11203 0.1…10 Мпа",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29744','Reservation Number':-33,'WO №':-33,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр образцовый МО-11203 0.1…60 Мпа",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29745','Reservation Number':-34,'WO №':-34,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА  150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29746','Reservation Number':-35,'WO №':-35,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА 150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29747','Reservation Number':-36,'WO №':-36,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА 150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29748','Reservation Number':-37,'WO №':-37,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА 150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29749','Reservation Number':-38,'WO №':-38,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА 150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29750','Reservation Number':-39,'WO №':-39,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Манометр ТМ-610Р.00 0-4МПА 150ММ 1.5 М20х1.5",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29761','Reservation Number':-40,'WO №':-40,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Однобалочный мостовой кран YH 10-6",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29733','Reservation Number':-41,'WO №':-41,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Пресс гидравлический П 6320 Б. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29751','Reservation Number':-42,'WO №':-42,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Сверлиный станок",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29752','Reservation Number':-43,'WO №':-43,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Сверлиный станок",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29753','Reservation Number':-44,'WO №':-44,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Сверлиный станок",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29758','Reservation Number':-45,'WO №':-45,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Станок для вальцовки металла",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29738','Reservation Number':-46,'WO №':-46,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Станок супертроник '4S АУТО' для нарезки резьбы 1/2-4 BSPT 56465 ROTHENBERG. Б/У ",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29731','Reservation Number':-47,'WO №':-47,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Станок токарно-винтроезный - Модель: 16К20. Б/У ",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29732','Reservation Number':-48,'WO №':-48,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Станок токарный - Модель: НL-720. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29737','Reservation Number':-49,'WO №':-49,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Точильно корея. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29734','Reservation Number':-50,'WO №':-50,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Точильно-шлифовальный станок ТШ-3 Абразивный камень д400. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29735','Reservation Number':-51,'WO №':-51,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Точильно-шлифовальный станок ТШ-3 Абразивный камень д400. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29736','Reservation Number':-52,'WO №':-52,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Точильно-шлифовальный станок ТШ-3 Абразивный камень д400. Б/У",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            {'Код товара':'29754','Reservation Number':-53,'WO №':-53,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Электрическая гильотина по металлу",'Ед.изм.':'комплект','Quantity':1,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'new', 'Объект':'new'},
            
            {'Код товара':'09683','Reservation Number':-54,'WO №':-54,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':21.624,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
            
            {'Код товара':'06933','Reservation Number':-55,'WO №':-55,'closedMonth':10,'closedYear':2024,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':160,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            {'Код товара':'06933','Reservation Number':-56,'WO №':-56,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':40,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
        
            ],
        'currentReturn':[]
    },
}
