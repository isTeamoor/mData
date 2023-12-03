"""Добавленные вручную товарные позиции"""
extra = {
    'rmpd':{
        'begin':[],
        'currentMonth':[]
    },
    'cofe':{
        'begin':[
            {'Код товара':'5943','Материал':'Газ сжиженный ПБФ','Ед.изм.':'бал','Quantity':3,'Reservation Number':-1,'Work Order Status Description':'OnHand','closedMonth':13,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-1,'reservYear':2023,'reservMonth':13,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5287','Материал':"Nipoflange 3'' X 1'' ND, Cl300, BWxRF, CS A105 BE MSS-SP-97 MR0103 / Фланцевая бобышка",'Ед.изм.':'шт','Quantity':2,'Reservation Number':-2,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-2,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5149','Материал':"Клапан запорный 3/4' #300 фланцевый*",'Ед.изм.':'комплект','Quantity':1,'Reservation Number':-3,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-3,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5286','Материал':"ELBOW 90 LR, 1/2', SCH 40, CS A105 SWE, B16.11 CL600 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':1,'Reservation Number':-4,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-4,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5239','Материал':"ELBOW 90 LR, 3', SCH 40, CS A234- WPB, SMLS, ASME B16.9 MR0103, / Отвод",'Ед.изм.':'шт','Quantity':12,'Reservation Number':-5,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-5,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5237','Материал':"PIPE 1/2', SCH 160, A106- B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':0.9,'Reservation Number':-6,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-6,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5236','Материал':"PIPE 1-1/2', SCH 160, A106- B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':0.8,'Reservation Number':-7,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-7,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
            {'Код товара':'5234','Материал':"PIPE 3', SCH STD, A106-B, BE, B36.10M MR0103 SEAMLESS, / Труба бесшовная",'Ед.изм.':'м','Quantity':98.08,'Reservation Number':-8,'Work Order Status Description':'Open','closedMonth':10,'Отдел':'CofE','Reserved By':'Mirjakhon Toirov','WO №':-8,'reservYear':2022,'reservMonth':12,'Asset Description':'CofE', 'Объект':'CofE'},
        ],
        'currentMonth':[]
    },
}
"""Example"""
#{'Код товара':'','Материал':'','Ед.изм.':'','Quantity':0,'Reservation Number':0,'Work Order Status Description':'','closedMonth':0,'Отдел':'','Reserved By':'','WO №':0,'reservYear':2023,'reservMonth':0,'Asset Description':'', 'Объект':''},


def corrections(transactions):
    transacts = transactions

    transacts.loc [ transacts['Catalogue Transaction ID'].isin([101733,101734]), 'transactMonth'] = 11 #Ulugbek Hamroyev LTFT Возврат труб был в ноябре письмо

    transacts.loc[ transacts['Reservation Number'] == 5388, 'Quantity' ] = 162 # 9356 - Высокотемпературный силиконовый герметик "TYTAN"
    transacts.loc[ transacts['Reservation Number'] == 4450, 'Quantity' ] = 4794.6 # 7633 - Рулон оцинкованный ГОСТ 14918-80 Ст08пс Zn120,  0,65x1250 БТ н/обр.
    
    transacts.loc[ transacts['Reservation Number'] == 5778, 'closedMonth' ] = 10 # Миржахон что то поменял в закрытом WO

    return transacts


