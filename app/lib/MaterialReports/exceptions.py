def corrections(transactions):
    transacts = transactions.copy()

    transacts.loc [ transacts['Catalogue Transaction ID'].isin([101733,101734]), 'transactMonth'] = 11 #Ulugbek Hamroyev LTFT Возврат труб был в ноябре письмо
    transacts.loc [ transacts['Catalogue Transaction ID'] == 103005, 'transactMonth'] = 12 #Мирсаид хайдаров в декабре возврат письмо

    transacts.loc[ transacts['Reservation Number'] == 5388, 'Quantity' ] = 162 # 9356 - Высокотемпературный силиконовый герметик "TYTAN"(часть уже списана до меня)
    transacts.loc[ transacts['Reservation Number'] == 4450, 'Quantity' ] = 4794.6 # 7633 - Рулон оцинкованный ГОСТ 14918-80 Ст08пс Zn120,  0,65x1250 БТ н/обр.(часть уже списана до меня)

    transacts.loc[ transacts['Reservation Number'] == 4415, 'closedMonth' ] = 11 #В связи с переходом на новый closed dates
    transacts.loc[ transacts['Reservation Number'] == 5188, 'closedMonth' ] = 11 #В связи с переходом на новый closed dates
    transacts.loc[ transacts['Reservation Number'] == 5528, 'closedMonth' ] = 11 #В связи с переходом на новый closed dates
    transacts.loc[ transacts['Reservation Number'] == 5527, 'closedMonth' ] = 11 #В связи с переходом на новый closed dates

    transacts.loc[ transacts['Reservation Number'] == 3768, 'isRMPD' ] = 'yes' #Проблемный WO, его должны перезакрыть в следюущем месяце

    transacts.loc[ transacts['Код товара'] == "06811", 'Ед.изм.' ] = 'шт' #Почему то не показывает ед.изм
    
    return transacts



inactive_Reservations= [
### RMPD
771,848,937,938,939,1049,1050,1051,1114,1272,1320,1322,1452,1592,1609,3798,1871,1873,1874,1902,1922,1924,2356,2306,2355,2826,3806,3843,2859,2873,3088,3093,3927,3135,3242,3797,
3826,3983,3827,3845,3977,3978,3979,3980,4346,4347,4348,4349,4038,4039,4040,4041,4042,4043,4125,4126,4159,4178,4194,4182,4198,4251,4252,4324,4325,921,2357,3227,3257,1126,885,
1901,1921,1923,756,2045,2044, 465, 798, 799,
### CofE
1538, 1756, 1847, 1946, 2695, 4554, 4555, 4556, 4557, 4684, 4685, 5244, 5311, 5418, 4014, 4116, 4117, 4155, 4245, 4394, 4396, 4463, 4620, 1350, 2886, 4015, 4761, 4763, 4765, 5362, 
2887, 4826, 4782, 4483, 3032, 3033, 3412, 3414, 3416, 3418, 3423, 3465, 3471, 3485, 3489, 3507, 3515, 3596, 3766, 4095, 3396, 3397, 3398, 3399, 3400, 3405, 3408, 3409, 3410, 3411, 
3413, 3420, 3422, 3424, 3428, 3434, 3455, 3457, 3460, 3470, 3472, 3475, 3479, 3482, 3483, 3486, 3490, 3513, 3516, 3519, 3521, 3524, 3552, 3591, 3597, 3767, 4480, 3545, 4119, 4623, 
4754, 5310, 5374, 5416, 4481, 4552, 1774, 4244, 1222, 1442, 1755, 1776, 1948, 2646, 4385, 4756, 5246, 5415, 1777, 2647, 4053, 4154, 4196, 4246, 4386, 4398, 4462, 4619, 4707, 4747, 
4755, 5417, 1791, 2323, 4749, 2916, 3020, 3097, 3180, 3184, 3544, 3624, 4047, 3910, 4401, 4037, 4081, 4115, 5430, 4118, 4140, 4397, 4402, 5248, 5249, 4403, 4465, 4404, 4461, 4621, 
4705, 5247, 5312, 5375, 4406, 4464, 4706, 4822, 4823, 4824, 4825, 5250, 5373, 5548, 1402, 2885, 4760, 4762, 4764
]


inactive_Master_Reservations  = [
### CofE
782,787,788,846,851,857,904,905,908,935,954,986,1009,1129,1311,1312,1313,1314,1341,1342,1343,1424,1426,1439,1443,1551,1560,1593,1594,1599,1603,1629,1631,1697,1698,1710,1848,
1849,1852,2278,2307,2335,2648,2649,2679,2816,2908,2955,2956,2957,2959,3146,3147,3148,3203,3204,5527,5528,5536,
]


extra = {
    #{'Код товара':'0','Reservation Number':-,'WO №':-,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"",'Ед.изм.':'','Quantity':0,'Отдел':'','Reserved By':"",'Asset Description':'undefined', 'Объект':'undefined'},
        
    'rmpd':{
        'begin':[],
        'currentMonth':[
            {'Код товара':'05275','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':'Наждачная бумага от 40 мм до 60 мм','Ед.изм.':'м2','Quantity':1,'Отдел':'RMPD','Reserved By':"Mirsaid Xaydorov Baxtiyor o'g'li",'Asset Description':'undefined', 'Объект':'undefined'},
        ],
        'currentReturn':[
            ### !!! Qty со знаком "-"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ]
    },
    'cofe':{
        'begin':[
            #Постоянно на балансе 3 балона газа
            {'Код товара':'05943','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':0,'Work Order Status Description':'OnHand','Материал':'Газ сжиженный ПБФ','Ед.изм.':'бал','Quantity':3,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            # По результатам инвентаризации - "LPG"
            {'Код товара':'05287','Reservation Number':-2,'WO №':-2,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"Nipoflange 3'' X 1'' ND, Cl300, BWxRF, CS A105 BE MSS-SP-97 MR0103 / Фланцевая бобышка",'Ед.изм.':'шт','Quantity':2,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05286','Reservation Number':-3,'WO №':-3,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"ELBOW 90 LR, 1/2', SCH 40, CS A105 SWE, B16.11 CL600 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':1,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05239','Reservation Number':-4,'WO №':-4,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"ELBOW 90 LR, 3', SCH 40, CS A234- WPB, SMLS, ASME B16.9 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':12,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05237','Reservation Number':-5,'WO №':-5,'closedMonth':0,'closedYear':0,'Work Order Status Description':'OnHand','Материал':"PIPE 1/2', SCH 160, A106- B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':0.9,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05236','Reservation Number':-6,'WO №':-6,'closedMonth':0,'closedYear':0,'Work Order Status Description':'OnHand','Материал':"PIPE 1-1/2', SCH 160, A106- B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':0.8,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05234','Reservation Number':-7,'WO №':-7,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"PIPE 3', SCH STD, A106-B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':98.08,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
        ],
        'currentMonth':[
            {'Код товара':'06933','Reservation Number':-8,'WO №':-8,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"Дизельное топливо",'Ед.изм.':'л','Quantity':100,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'06933','Reservation Number':-9,'WO №':-9,'closedMonth':0,'closedYear':0,'Work Order Status Description':'OnHand','Материал':"Дизельное топливо",'Ед.изм.':'л','Quantity':100,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'09683','Reservation Number':-10,'WO №':-10,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':15.561,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'01875','Reservation Number':-11,'WO №':-11,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"Азот баллон 50л ",'Ед.изм.':'шт','Quantity':3,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
        ],
        'currentReturn':[
            ### !!! Qty со знаком "-"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Возврат на склад материалов с "LPG"
            {'Код товара':'05234','Reservation Number':-7,'WO №':-7,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"PIPE 3', SCH STD, A106-B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':-98.08,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05239','Reservation Number':-4,'WO №':-4,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"ELBOW 90 LR, 3', SCH 40, CS A234- WPB, SMLS, ASME B16.9 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':-12,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05286','Reservation Number':-3,'WO №':-3,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"ELBOW 90 LR, 1/2', SCH 40, CS A105 SWE, B16.11 CL600 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':-1,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'05287','Reservation Number':-2,'WO №':-2,'closedMonth':11,'closedYear':2023,'Work Order Status Description':'Closed','Материал':"Nipoflange 3'' X 1'' ND, Cl300, BWxRF, CS A105 BE MSS-SP-97 MR0103 / Фланцевая бобышка",'Ед.изм.':'шт','Quantity':-2,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','Asset Description':'CofE', 'Объект':'CofE'},
        ]
    },
}
