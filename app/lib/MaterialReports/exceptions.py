def corrections(transactions):
    transacts = transactions.loc[ transactions['Код товара']!='00nan'].copy() 



    ### 1. Это ОС ##############################################################################################
    #CofE
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([15589,20309,
                                                                       20232,
                                                                       22884,23146,23147,23148,23149,23150,23152,
                                                                       24187,
                                                                       30943,
                                                                       33233,
                                                                       33672,
                                                                       ])) ]
    #RMPD
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([16946,
                                                                       17501,17502,17503,17504,18755,20232,
                                                                       34796,34849,])) ]
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
    
    transacts.loc[ transacts['Reservation Number'].isin([6801,7605,7609,6802,6804,6805,6806,7237,7244,7604,7608,
                                                         7238,7245,7611,7612,7650,7651,8477,8478,9088,9089,9092,
                                                         7992,7993,8333,8334,8851,9140,9157,9160,9158,9162,9159,
                                                         9161,7752,8475 ]), 'Reserved By' ] = 'Mirjahon Toirov CofE'
   ############################################################################################################





    ### 4. Возвраты #############################################################################################
    #Листовые фильтры Мансур Хасанов, Тулкинакя
    transacts.loc[ transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]), 
                                                        'Work Order Status Description' ] = 'Pending for return'
    transacts.loc[ (transacts['Reservation Number'].isin([10968,10969,10970,10971,10972,10973,10974,10975,10976]))
                   &
                   (transacts['Catalogue Transaction Action Name']=='Return to Stock'), 'transactYear' ] = 2027
    
    #Не списывать CofE 4 AP будут возвращать
    transacts.loc[ transacts['Reservation Number'].isin([17113,]), 
                                                        'Work Order Status Description' ] = 'Pending for return'
    transacts.loc[ transacts['Reservation Number'].isin([16761,17100]), 
                                                        'Work Order Status Description' ] = 'Closed'
    ############################################################################################################

    
    

    ### 5. Технические ошибки ##################################################################################
    #Шохзод Юлдашев для SLU - он пока не в списке isRmpdPlaner. Проверить, можно удалить наверное, включил их в is_rmpdPlaner
    transacts.loc[ transacts['Reservation Number'].isin([19189,19146,19193,19666,19724,20441,19660,19679,21116,
                                                         15560,19680,15145,20369,21117,
                                                         4731,
                                                         29253]), 'isRMPD_planner' ] = 'yes'

    """#Временное хранение. Уктам Ильхомов. Блайнд. Было лень разбираться. есть письмо на временное хранение
    transacts.loc[ transacts['Reservation Number'].isin([26964,]), 'closedMonth' ] = 11

    #Временное хранение.Мирсаид Хайдаров. Было лень разбираться. есть письмо на временное хранение
    transacts.loc[ transacts['Reservation Number'].isin([29199,]), 'closedMonth' ] = 11"""

    #Баллон - это тара, будет на балансе, не в 014
    transacts.loc[ transacts['Код товара'].isin(['01876',]), 'Work Order Status Description' ] = "Тара"

    """#Возврат. сделали в ноябре, но октябрский
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([165725,]), 'transactMonth' ] = 10"""

    #Возврат. сдали на склад в ноябре, но транзакция в декабре
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([168307,]), 'transactMonth' ] = 11

    """#Мирсаид ошибся. сделали возврат списанных В декабре пересмотреть. есть корректирующее письмо
    #Взять обратно на баланс и сразу вернуть на склад
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([167055,167054,]), 'transactMonth' ] = 12
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([167055,167054,]), 'closedMonth' ] = 12
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([160900,160908,]), 'transactMonth' ] = 11
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([160900,160908,]), 'closedMonth' ] = 12"""
    transacts = transacts.loc[ ~( transacts['Catalogue Transaction ID'].isin([167055,167054,]) ) ]


    #Спецодежду для TAR команды не считать
    transacts = transacts.loc[ ~(transacts['Отдел']=="Training Sector") ]

    #Бобур сказал это не списывать, они еще раз будут его использовать, потом может на врем хран дадут
    transacts.loc[ transacts['Reservation Number'].isin([30127,]), 'Work Order Status Description' ] = 'Undefined'

    #Временное хранение. Оказывается Faruh mamurov письмо написал на врем.хран. лень разбираться.
    transacts.loc[ transacts['Reservation Number'].isin([28105,28099,28386,28097,28096,28102,28098,
                                                         28106,28101,]), 'Work Order Status Description' ] = 'Closed'
    transacts.loc[ transacts['Reservation Number'].isin([28105,28099,28386,28097,28096,28102,28098,
                                                         28106,28101,]), 'closedMonth' ] = 12
    

    #Транзакции в cmms ссылаются на одинаковую spareID
    transacts = transacts.loc[ ~(
        (transacts['Reservation Number'] == 29844) & (transacts['Catalogue Transaction ID'] == 165851) )]
    transacts = transacts.loc[ ~(
        (transacts['Reservation Number'] == 29846) & (transacts['Catalogue Transaction ID'] == 165838) )]
    

    #Взято для Tar, Jahongir Haydarov. Из-за фильтра попадает в мунтазам. Записываю в Cofe
    #почему то снова WO не закрыт, в декабре был закрыт. уже списал в декабрском
    transacts.loc[ transacts['Reservation Number'].isin([32898,]), 'Отдел' ] = 'TAR CofE'
    transacts.loc[ transacts['Reservation Number'].isin([32898,]), 'closedMonth' ] = 12 
    transacts.loc[ transacts['Reservation Number'].isin([32898,]), 'closedYear' ] = 2025
    transacts.loc[ transacts['Reservation Number'].isin([32898,]), 'Work Order Status Description' ] = 'Closed'
    

    #Взято для Tar, Bobur Aralov. Из-за фильтра попадает в мукаммаллик. Записываю в мунтазам
    transacts.loc[ transacts['Reservation Number'].isin([32886,]), 'isRMPD_planner' ] = 'yes'
    transacts.loc[ transacts['Reservation Number'].isin([32886,]), 'Reserved By' ] = 'Shohijahon Tilavov Abduxalil o`g`li'
    
    #Даврон Хидиров сказал оставить на балансе до тех пока не сделаю акт деффектации и металлолом
    transacts.loc[ transacts['Reservation Number'].isin([30865,33026,]), 'Work Order Status Description' ] = 'w8 4 yaroqsiz dalolat'
    
    #Незарегестрированные в 1с материалы, не учитывать в балансе
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([33975,33846,34104,33985,33847,33709,33707,
                                                                       34088,33702,33699,])) ]
    
    #Сделали транзакции в феврале, но возврат должен быть в январе
    transacts.loc[ transacts['Catalogue Transaction ID'].isin([175105,175106,175107,175108,175109,175110,175111,
                                                               175112,175113,175114,175115,]), 'transactMonth' ] = 1
    

    ############################################################################################################


    ### 6. AP ##################################################################################################   
    ############################################################################################################


    ### 7. Взято с временного хранения #########################################################################
    transacts = transacts.loc[ ~(transacts['Reservation Number'].isin([27599,
                                                                       29283,
                                                                       30954,30956,30955,
                                                                       #TAR декабрь
                                                                       32036,31655,32037,31644,32038,32501,32503,32504,33082,33081,33074,33080,31645,31648,32967,
                                                                        #TAR декабрь Cofe
                                                                        32098,
                                                                        #Январь RMPD
                                                                        33753,33754,33588,33622,33623,33606,33607,33608,33609,33624,33586,33637,33584,33595,33599,33601,33589,33591,33603,33602,33620,33625,33632,33638,
                                                                        #Январь CofE
                                                                        34961,
                                                                       ])) ]
    ############################################################################################################

    ### 8. TAR custom closed dates #############################################################################
    #32707, манометр. Сделал раздачу, оказывается запчасть. списать в январском
    transacts.loc[ transacts['Reservation Number'].isin([32707,]), 'closedMonth' ] = 1
    transacts.loc[ transacts['Reservation Number'].isin([32707,]), 'closedYear' ] = 2026

    tar_december = [32428,31661,31668,31662,31664,31663,31088,31089,31102,32212,30887,30888,31666,31665,31354,33209,28115,33168,33169,33173,30881,32771,27827,27829,27577,30344,27795,27826,27011,27033,27575,27820,30343,27587,28105,30346,27584,27828,27585,30350,27586,30349,27579,30352,30345,32695,32049,32797,32926,33061,32796,32925,29501,30542,31215,31272,31356,31805,31807,31971,32397,32448,32902,33238,32713,32809,32840,31067,32022,32023,32024,32025,32900,30612,32721,32728,32729,32720,32738,32788,31357,33027,27589,31803,31804,32786,31544,33094,29848,31306,32211,32488,32758,32763,33157,33231,30949,29598,29734,30388,32258,29599,29733,30389,31274,31623,31679,31685,31686,31688,31689,31690,31693,31735,31793,32364,32389,32527,32533,32804,32931,32932,33072,30866,31091,31095,30833,30835,30837,30839,30840,30841,31351,31785,32736,32499,30950,31352,31353,31900,31901,31902,31903,31904,31905,31906,31907,31908,31909,31910,31911,31912,31913,31914,31915,31916,31917,31918,31919,31920,31921,31922,31923,31924,31925,31926,31927,31928,31929,31930,31931,31932,31933,31934,31935,31936,31937,31938,31939,31940,31941,31951,31952,31953,31954,31955,31956,31957,31958,32052,32053,32054,32055,32056,32057,32058,32059,32060,32061,32062,32063,32064,32065,32066,32067,32068,32069,32070,32071,32072,32073,32074,32075,32077,32078,32079,32080,32081,32082,32083,32084,32085,32086,32087,32088,32089,32090,32099,32100,32101,32102,32103,32104,32105,32106,32107,32108,32109,32110,32111,32112,32113,32114,32115,32116,32117,32118,32119,32120,32121,32122,32123,32124,32125,32126,32127,32128,32129,32130,32131,32132,32133,32136,32141,32142,32143,32144,32145,32146,32147,32148,32149,32150,30637,27213,25871,31799,32242,32652,31801,31802,32244,32649,31800,32243,32650,33113,33060,33208,30919,26594,26593,32673,26591,30502,30508,30514,32961,29706,30351,26592,31638,29705,32255,32416,29704,32254,32417,27823,32969,27830,32968,30649,30046,32684,32708,32775,32972,25502,32794,32924,32706,24742,29617,30918,26595,29619,26597,33205,24750,26580,28099,26598,24744,13666,26684,32793,32923,28386,29710,30084,29709,32792,32922,33076,26583,26238,31440,31441,31439,27005,27019,27004,30590,32236,30584,33220,32235,26837,30583,32919,27021,27025,29600,29732,30390,25677,27006,27020,28134,30348,32257,32256,32699,27089,27825,27926,28136,32176,31961,26685,27723,33218,30941,32246,27454,31684,31103,33099,33100,33101,33102,33103,32930,30947,31531,31068,31230,31231,31232,31233,31234,31235,31236,31239,31240,31241,31242,31243,31244,31245,31246,31247,31248,31249,33042,33043,33044,33045,31261,31262,31263,31265,30899,31983,30585,32891,31569,30902,31667,30353,32838,32844,33065,32698,29656,33085,33086,33087,32505,32509,32506,32510,28726,33007,33008,33009,33010,33028,25868,25874,25867,32890,27012,32892,32893,27007,27024,27008,27027,32507,32508,32500,31974,32449,32451,30856,30857,31975,32265,33016,33017,33018,32431,31438,31437,26579,31962,32172,30589,33098,33104,33105,33106,26596,33174,31126,31106,32171,26578,28116,33251,27034,32712,31093,27009,27028,27590,27581,30347,26584,33023,31094,31733,32097,31419,31420,31421,31422,31423,31424,31425,31426,31427,31428,31430,31431,31432,31433,31434,31435,31436,31571,31572,31573,31574,31575,31576,31577,31578,31579,31580,31581,31582,31583,31584,31585,31586,31587,31588,31589,31590,31591,31592,31593,31594,31595,31596,31597,31598,31599,31600,31601,31602,31603,31604,31605,31606,31607,31608,31609,31610,31611,31612,31613,31615,31616,31617,31618,31619,31621,31622,31634,31987,31988,31989,31990,31991,31992,31993,31994,31995,31996,31997,31998,31999,32000,32001,27013,27036,32779,32697,31728,31682,30586,32137,31216,32789,29626,31545,31546,31547,31548,31549,31550,31551,31552,31553,31554,31556,31557,31558,31559,31560,31561,31562,31563,31564,31565,31566,31567,31568,32151,32152,32153,32154,32155,32156,32157,32158,32159,32160,32424,32425,32991,32971,32847,31073,31366,33092,33091,24932,29711,25933,30549,30145,31789,32477,32473,31107,30143,32423,28541,31033,33111,33167,29662,32033,32183,31117,26590,31125,26585,26586,26588,33158,26587,26589,32018,28097,28096,29854,25886,31766,30610,26576,29852,30233,31219,31220,32026,32027,32028,32029,29575,24920,28102,31629,33117,28098,32854,28106,25945,32341,29853,28101,25889,30846,32343,32344,32345,32346,32347,32348,32349,32350,32351,32352,32353,32354,32355,32356,32357,32358,32359,32360,32361,32362,31250,29625,25722,25986,32768,27032,27542,32174,33112,27831,26599,26840,25887,25888,32260,33011,33012,29597,29707,29731,30387,29612,30391,31367,25892,25891,25890,32134,26166,26167,32453,32454,32456,32457,32458,32459,32460,32461,32462,32463,32464,32465,32520,32521,32522,32523,32524,32525,32526,32546,32547,32548,32549,32550,32551,32552,32553,32554,32555,32693,32694,32719,31683,32515,28745,31798,32241,32651,31797,32240,32648,32245,32177,30105,32266,31031,32035,33093,32756,33203,32450,32514,30417,31639,31640,31641,31642,31643,31692,31694,31695,31696,31697,31698,31699,31700,31701,31702,31703,31704,31705,31706,31707,31708,31709,31710,31711,31712,31713,31714,31715,31716,31717,31718,31719,31720,31721,31722,31723,31724,31725,31726,31727,31809,31810,31811,31813,31814,31815,31816,31817,31818,31819,31820,31821,31822,31823,31824,31825,31826,31827,31828,31829,31830,31831,31832,31833,31834,31835,31836,31837,31838,31839,31840,31841,31842,31843,31844,31845,31846,31847,31848,31849,31850,31851,31852,31943,31944,31945,31946,31947,31948,31949,31950,31959,32032,32161,32162,32163,32164,32165,32166,32167,32168,32169,32170,32764,33221,32558,32927,32795,31442,32237,32238,32239,]
    transacts.loc[ transacts['Reservation Number'].isin(tar_december), 'Work Order Status Description' ] = 'Closed'
    transacts.loc[ transacts['Reservation Number'].isin(tar_december), 'closedMonth' ] = 12
    transacts.loc[ transacts['Reservation Number'].isin(tar_december), 'closedYear' ] = 2025

    tar_jan = [34300,]
    transacts.loc[ transacts['Reservation Number'].isin(tar_jan), 'Work Order Status Description' ] = 'Closed'
    transacts.loc[ transacts['Reservation Number'].isin(tar_jan), 'closedMonth' ] = 1
    transacts.loc[ transacts['Reservation Number'].isin(tar_jan), 'closedYear' ] = 2026
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
            {'Код товара':'12814','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':0,'Work Order Status Description':'NotClosed','Материал':"Алюминий",'Ед.изм.':'кг','Quantity':3.9,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #{'Код товара':'12813','Reservation Number':-2,'WO №':-2,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Мис",'Ед.изм.':'кг','Quantity':7.87,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            {'Код товара':'12815','Reservation Number':-3,'WO №':-3,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Нержавекеющая сталь",'Ед.изм.':'кг','Quantity':0.84,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},

        ],
        'currentMonth':[
            #Бумага
            {'Код товара':'06944','Reservation Number':-4,'WO №':-4,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':4,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            #{'Код товара':'31158','Reservation Number':-5,'WO №':-5,'closedMonth':5,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Бумага для офисной техники белая А3",'Ед.изм.':'пачка','Quantity':1,'Отдел':'rmpd','Reserved By':"rmpd",'Asset Description':'Бумага', 'Объект':'Бумага'},
            
            #Met
            #Алюминий
            #{'Код товара':'12814','Reservation Number':-1009,'WO №':-1009,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Алюминий",'Ед.изм.':'кг','Quantity':69.7,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Алюминий
            #{'Код товара':'12814','Reservation Number':-1100,'WO №':-1100,'closedMonth':0,'closedYear':0,'Work Order Status Description':'Open','Материал':"Алюминий",'Ед.изм.':'кг','Quantity':3.2,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Медь
            #{'Код товара':'12813','Reservation Number':-1010,'WO №':-1010,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Мис",'Ед.изм.':'кг','Quantity':791.63,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Алюминий 13
            #{'Код товара':'29422','Reservation Number':-1006,'WO №':-1006,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Алюмин 13",'Ед.изм.':'т','Quantity':0.075,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Никель 13
            #{'Код товара':'11064','Reservation Number':-1007,'WO №':-1007,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Никель 13",'Ед.изм.':'т','Quantity':0.1993,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Медь 13
            #{'Код товара':'21883','Reservation Number':-1008,'WO №':-1008,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Медь 13",'Ед.изм.':'т','Quantity':0.7995,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
            #Свинец 13
            #{'Код товара':'16797','Reservation Number':-6,'WO №':-6,'closedMonth':2,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Свинец 13",'Ед.изм.':'т','Quantity':0.527,'Отдел':'rmpd','Reserved By':"Metall",'Asset Description':'Metall', 'Объект':'Metall'},
        ],
        'currentReturn':[]
    },
    'cofe':{
        'begin':[
            #Корректировка кислород. Перенес в exception.corrections в reservation 28748
            #{'Код товара':'13688','Reservation Number':-1,'WO №':-1,'closedMonth':0,'closedYear':2024,'Work Order Status Description':'Open','Материал':"Кислород газообразный",'Ед.изм.':'м³','Quantity':0.12,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Корректировка Кислород', 'Объект':'Корректировка Кислород'},
            
            #Diesel
            #{'Код товара':'06933','Reservation Number':-2,'WO №':-2,'closedMonth':2,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':166,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            {'Код товара':'06933','Reservation Number':-3,'WO №':-3,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':307,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            #{'Код товара':'09683','Reservation Number':-4,'WO №':-4,'closedMonth':4,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':0.0199,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},

            #Задвижка от АХО. Списание в ноябре!
            #{'Код товара':'30892','Reservation Number':-10,'WO №':-10,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Задвижка металл. чугунная d=80мм (до 4 атмосфера)",'Ед.изм.':'комплект','Quantity':2,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Из АХО', 'Объект':'Из АХО'},
        
            #Взято актом приемки без налога
            {'Код товара':'40872', 'Reservation Number':-12, 'WO №':-12, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба 6 м х 48,3', 'Ед.изм.':'шт', 'Quantity':11893, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40873', 'Reservation Number':-13, 'WO №':-13, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба 4 м х 48,3', 'Ед.изм.':'Шт', 'Quantity':7325, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40874', 'Reservation Number':-14, 'WO №':-14, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба 3 м х 48,3', 'Ед.изм.':'Шт', 'Quantity':3063, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40875', 'Reservation Number':-15, 'WO №':-15, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба 2 м х 48,3', 'Ед.изм.':'шт', 'Quantity':1050, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40876', 'Reservation Number':-16, 'WO №':-16, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба 1,5м х 48,3 ', 'Ед.изм.':'Шт', 'Quantity':360, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40877', 'Reservation Number':-17, 'WO №':-17, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Труба ф48 х 1200 мм', 'Ед.изм.':'Шт', 'Quantity':280, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40878', 'Reservation Number':-18, 'WO №':-18, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Опорная плита: трубка 36х1,5х100мм подошва 150х150х6мм', 'Ед.изм.':'Шт', 'Quantity':150, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40879', 'Reservation Number':-19, 'WO №':-19, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Домкрат (башмак резбавой-опорный плита резбавой)', 'Ед.изм.':'Шт', 'Quantity':294, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40880', 'Reservation Number':-20, 'WO №':-20, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Хомут Неповоротный хомут 48*48', 'Ед.изм.':'Шт', 'Quantity':25000, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40881', 'Reservation Number':-21, 'WO №':-21, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Хомут поворотный хомут 48*48', 'Ед.изм.':'Шт', 'Quantity':9075, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40882', 'Reservation Number':-22, 'WO №':-22, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Муфты, болты и гайки 1/2`х21ММ EN74 гальваническое покрытие(соединитель наружный)', 'Ед.изм.':'Шт', 'Quantity':3025, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40883', 'Reservation Number':-23, 'WO №':-23, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Муфта рукава (соединитель внутренный)', 'Ед.изм.':'Шт', 'Quantity':2900, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40884', 'Reservation Number':-24, 'WO №':-24, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Стяжки одиночные, болты и гайки 1/2`х21ММ AS/NZS1576.2: 2009 гальваническое покрытие(Кобра)', 'Ед.изм.':'Шт', 'Quantity':1450, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40885', 'Reservation Number':-25, 'WO №':-25, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Зажим лучевой неповоротный 48,3ММ, болты, гайки М14х22ММ сталь кованная Q235 гальваническое покрытие (для балки-17)', 'Ед.изм.':'Шт', 'Quantity':4607, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40886', 'Reservation Number':-26, 'WO №':-26, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Зажим лучевой поворотный 48,3ММ, болты, гайки М14х22ММ сталь кованная Q235 гальваническое покрытие(для балки-17)', 'Ед.изм.':'Шт', 'Quantity':3050, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40887', 'Reservation Number':-27, 'WO №':-27, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Муфта кованая электро-оцинкованная 48,3ММ BS1139(бабочка)', 'Ед.изм.':'Шт', 'Quantity':2520, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40888', 'Reservation Number':-28, 'WO №':-28, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Хомут крепления доски (бабочка хомут)', 'Ед.изм.':'шт', 'Quantity':520, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40889', 'Reservation Number':-29, 'WO №':-29, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Зажимы для лестниц, болты и гайки 1/2`х21ММ BS 1139/EN 74-1 гальваническое покрытие', 'Ед.изм.':'Шт', 'Quantity':700, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40890', 'Reservation Number':-30, 'WO №':-30, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'(Ladder) Балка лестничный тип 10 метр) - Соединитель труб 10х0.4М OD48.3х3.2х305ММ', 'Ед.изм.':'Шт', 'Quantity':55, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40891', 'Reservation Number':-31, 'WO №':-31, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'(Ladder) Балка лестничный тип 6,0 метр) - Соединитель труб 6х0.4М OD48.3х3.2х305ММ', 'Ед.изм.':'Шт', 'Quantity':40, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40892', 'Reservation Number':-32, 'WO №':-32, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Настил металлический с крюками 420х45х3000х1.5ММ', 'Ед.изм.':'Шт', 'Quantity':2700, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40893', 'Reservation Number':-33, 'WO №':-33, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Настил металлический с крюками 420х45х3000х1.5ММ', 'Ед.изм.':'шт', 'Quantity':430, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40894', 'Reservation Number':-34, 'WO №':-34, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Настил с крюками 210х45х1.5х3000', 'Ед.изм.':'Шт', 'Quantity':600, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40895', 'Reservation Number':-35, 'WO №':-35, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Планка 1.2х45х210х2000ММ настил стальная с крючками', 'Ед.изм.':'Шт', 'Quantity':400, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40896', 'Reservation Number':-36, 'WO №':-36, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Доска(2м) сосна 40х200х2000ММ ГОСТ 8486-86', 'Ед.изм.':'Шт', 'Quantity':200, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40897', 'Reservation Number':-37, 'WO №':-37, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Доска (4м) сосна 40х200х4000ММ ГОСТ 8486-86', 'Ед.изм.':'Шт', 'Quantity':50, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40898', 'Reservation Number':-38, 'WO №':-38, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Доска (3м )сосна 40х200х3000ММ ГОСТ 8486-86', 'Ед.изм.':'Шт', 'Quantity':2050, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40899', 'Reservation Number':-39, 'WO №':-39, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Доска (6м) сосна 40х200х6000ММ ГОСТ 8486-86', 'Ед.изм.':'Шт', 'Quantity':50, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40900', 'Reservation Number':-40, 'WO №':-40, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Лестница 2000х2000х450х1.2х9', 'Ед.изм.':'Шт', 'Quantity':25, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40901', 'Reservation Number':-41, 'WO №':-41, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Лестница алюминий 3М 450ММ горизонтальная труба 29х29х1,2ММ вертикальная труба 63х24х1,2ММ', 'Ед.изм.':'Шт', 'Quantity':50, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40902', 'Reservation Number':-42, 'WO №':-42, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Лестница алюминий 4М 450ММ горизонтальная труба 29х29х1,2ММ вертикальная труба 63х24х1,2ММ', 'Ед.изм.':'Шт', 'Quantity':80, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },
            {'Код товара':'40903', 'Reservation Number':-43, 'WO №':-43, 'closedMonth':10, 'closedYear':2025, 'Work Order Status Description':'NotClosed', 'Материал':'Лестница алюминий 6М 450ММ горизонтальная труба 29х29х1,2ММ вертикальная труба 63х24х1,2ММ', 'Ед.изм.':'Шт', 'Quantity':94, 'Отдел':'CofE', 'Reserved By':'CofE', 'Asset Description':'CofE', 'Объект':'CofE', },


        ],
        'currentMonth':[
            #Бумага
            {'Код товара':'06944','Reservation Number':-5,'WO №':-5,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Бумага А4 SvetaCopy 80гр. В пачке 500 листов",'Ед.изм.':'пачка','Quantity':6,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Канцтовары', 'Объект':'Канцтовары'},
            
            #Хозтовары
            #{'Код товара':'22503','Reservation Number':-700,'WO №':-700,'closedMonth':12,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Мыло жидкое в ПЭТ бутылке объемом 500 ml",'Ед.изм.':'шт','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            {'Код товара':'36104','Reservation Number':-701,'WO №':-701,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Туалетная бумага Elma Panda Asian pack Econom 6 шт",'Ед.изм.':'упаковка','Quantity':15,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            {'Код товара':'36885','Reservation Number':-702,'WO №':-701,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Бумажные салфетки Elma Z ECO для дисп. 180 шт. (243)",'Ед.изм.':'упаковка','Quantity':20,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            
            #Хозтовары
            #{'Код товара':'36885','Reservation Number':-1,'WO №':-1,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Бумажные салфетки Elma Z ECO для дисп. 180 шт. (243)",'Ед.изм.':'упаковка','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            #{'Код товара':'36104','Reservation Number':-2,'WO №':-2,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Туалетная бумага Elma Panda Asian pack Econom 6 шт",'Ед.изм.':'упаковка','Quantity':10,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            #{'Код товара':'22503','Reservation Number':-4,'WO №':-4,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"Мыло жидкое в ПЭТ бутылке объемом 500 ml",'Ед.изм.':'упаковка','Quantity':5,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Хозтовары', 'Объект':'Хозтовары'},
            
            #Diesel
            {'Код товара':'06933','Reservation Number':-6,'WO №':-6,'closedMonth':1,'closedYear':2026,'Work Order Status Description':'Closed','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':266,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            {'Код товара':'06933','Reservation Number':-8,'WO №':-8,'closedMonth':0,'closedYear':2025,'Work Order Status Description':'Open','Материал':"Дизельное топливо GTL",'Ед.изм.':'л','Quantity':377,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'Diesel', 'Объект':'Diesel'},
            
            #Met
            #{'Код товара':'09683','Reservation Number':-9,'WO №':-9,'closedMonth':11,'closedYear':2025,'Work Order Status Description':'Closed','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':74.366,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},
            #{'Код товара':'09683','Reservation Number':-801,'WO №':-801,'closedMonth':0,'closedYear':2025,'Work Order Status Description':'Open','Материал':"СА-5 Qora metall chiqindilari ",'Ед.изм.':'тн','Quantity':0.0005,'Отдел':'CofE','Reserved By':"CofE",'Asset Description':'metall', 'Объект':'metall'},

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
