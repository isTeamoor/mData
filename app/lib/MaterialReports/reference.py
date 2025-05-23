import pandas as pd
import numpy as np


# Фильтры для отделения transactions отдела
department_Filters = {
    'rmpd': [
        [
            {"field": 'isRMPD_planner', "operator": "==", "value": "'yes'"},
            "&",
            {"field": 'Reserved By', "operator": "!=","value": "'Mirjahon Toirov CofE'"}
        ],
        "|",
        [
            {"field": 'Отдел', "operator": "==","value": "'Turnaround'"},
            "&",
            {"field": 'Reserved By', "operator": "!=","value": "'Boburjon Aralov Akbar o`g`li'"},
        ],        
    ],
    'cofe': [{"field": 'Reserved By', "operator": "==", "value": "'Boburjon Aralov Akbar o`g`li'"},
             "|",
             {"field": 'Reserved By', "operator": "==", "value": "'Mirjahon Toirov CofE'"}
             ]
}


# Номера Материальных Кодов, относящихся к 014 Забалансовому счёту
is_014 = ['',
'06935', '05841', '07139', '05230', '04189', '03494', '02799', '05749', '01738', '01308', '01309', '01310', '01311', '01312', '01329', '01330', '01331', '01333', '01351', '01354', '01372', '01374', '01376',
'01377', '01378', '00892', '02204', '04179', '00158', '00140', '00134', '00114', '00915', '01278', '01276', '01275', '01277', '01272', '01279', '03190', '02995', '02806', '02812', '02813', '02814', '02826', '02827',
'02828', '02830', '02896', '02897', '01307', '01353', '01373', '03904', '01375', '02325', '01393', '03484', '03017', '02786', '03019', '04662', '00899', '03745', '01367', '02890', '02891', '02892', '02893', '02894',
'02452', '02092', '02451', '02817', '00155', '00156', '00526', '00002', '04188', '02910', '06597', '07277', '01622', '01625', '01623', '01626', '01624', '03222', '01628', '01630', '01627', '01632', '00009', '00001',
'04346', '01274', '01273', '01352', '02854', '02863', '02885', '03480', '01349', '03226', '02824', '02935', '01344', '06601', '06600', '01337', '01313', '01315', '01316', '01317', '01320', '01321', '01322',
'01323', '01325', '01326', '01327', '01568', '01635', '01570', '01571', '01588', '01590', '01591', '01636', '01603', '01604', '01621', '02804', '02807', '02809', '02815', '06598', '02816', '02818', '02819', '02820',
'02821', '02822', '02823', '02831', '02834', '02840', '02845', '02846', '02847', '02848', '02851', '02856', '02858', '02860', '02861', '02864', '02878', '02880', '02881', '02882', '02883', '02884', '02886', '60599',
'02887', '02888', '02899', '02900', '02901', '02902', '02903', '02906', '02936', '03260', '00809', '00810', '02453', '00678', '00157', '00203', '00113', '00158', '00159', '06136', '01575', '01578', '00154', '06899',
'02450', '05359', '06799', '03227', '01379', '01382', '01314', '01319', '02879', '01366', '02857', '02865', '00007', '00008', '05942', '04140', '05752', '06330', '01189', '01324', '00865', '01369', '00863', '01355',
'01387', '00804', '01587', '01328', '01332', '02829', '01406', '00806', '00805', '01338', '01342', '01343', '01339', '01340', '01341', '02855', '02852', '03223', '02862', '01334', '01335', '01336', '02850', '02859',
'02853', '01403', '01574', '01576', '01577', '01582', '01360', '01361', '01364', '01365', '01429', '01407', '00691', '00692', '00693', '00694', '00695', '00700', '00703', '00702', '00705', '00706', '00707', '00708',
'01350', '01371', '01380', '01381', '01383', '01384', '01385', '01386', '01394', '01395', '01396', '01398', '01399', '01589', '01639', '01606', '01620', '02835', '00189', '00745', '00140', '00230', '00738', '05232',
'05231', '00899', '00155', '00114', '00157', '00526', '00113', '01201', '01202', '01203', '01204', '06340', '02911', '02912', '02913', '07481', '07407', '07473', '07403', '02802', '03229', '05305', '06122', '06332',
'06900', '07497', '07883', '07882', '09300', '07331', '05831', '09767', '01875', '04183', '09359', '02811', '07626', '07627', '07628', '07629', '07616', '07617', '10920', '05157', '28160', '28335', '09361', '09331',
'03014', '06326', '00704', '05824', '09605', '09606', '12414', '09608', '01517', '02838', '11063', '02794', '10518', '12500', '27290', '24631', '06304', '06331', '12497', '12499', '19400', '09332',
'01572', '01585', '30445', '05318', '01874', '06333', '16999', '02907', '31108', '05965', '29618', '02032', '02033', '18881', '21146', '26188', '02803', 
'29764','29763','29762','29767','29768','29769','29770','29771','29772','29773','29774','29775','29776','29777','29778','29779','29780','29765','29766','29760','29759','29757','29755','29756',
'29739','29740','29741','29742','29743','29744','29745','29746','29747','29748','29749','29750','29761','29733','29751','29752','29753','29758','29738','29731','29732','29737','29734','29735',
'29736','29754','33553','10517','18700','33471', '24617','24618','03259','',

#инструменты от ЕЕ
'30741','30742','30743','30744','30745','30746','30747','30748','30749','30750','30751','30752','30753','30754',
'30755','30756','30757','30758','30759','30760','30761','30762','30763','30764','30765','30766','30767','30768',
'30769','30770','30771','30772','30773','30774','30775','30776','30777','30778','30779','30780','30781','30782',
'30783','30784','30785','30786','30787','30788','30789','30790','30791','30792','30793','30794','30795','30796',
'30797','30798','30799','30800','30801','30802','30803','30804','30805','30806','30807','30808','30809','30810',
'30811','30812','30813','30814','30815','30816','30817','30818','30819','30820','30821','30822','30823','30824',
'30825','30826','30827','30828','30829','30830','30831','30832','30833','30834','30835','30836','30837','30838',
'30839','30840','30841', '31757',

#Контейнеры
'33094','33095','33096','33097','33098','33099','33100','33101','33102','33103','33104',
'32795','32796','32797','32798','32799','32800','32801','32802','32803','32804','32805','32806','33152',

#Кабель (Бобур использовал 1 раз, не может вернуть)
#'15698',

#Инструменты с TAR
'03014','30640','31438','31364','24788','24787','00705','00706','00707','00708','00691','00692',
'00693','00694','00695','00703','00702','00704','00701','30642','32399','32400','32401','32402','32403','32404',
'32405','32406','32407','32408','32409','32410','32411','32412','32413','32414','32415','32416','32417','32418',
'01619',

]

is_wOff = ['09327', '09326', '07483', '12478', '09859',
           '07536', '05328', '06949', '09607', '16801', '09360', '11316','09297','08008',]

tempSave = { 
    'cofe':[],
    'rmpd':[
    #25
    14660,14683,14665,14669,14684,14687,14692,14693,14809,16406,16413,18000,
    #28
    18752,19523,18753,18754,18898,19063,19274,19064,19273,19386,19585,19387,
    19419,19420,19421,19422,19522,20328,20329,
    #31
    18089,18090,18097,18281,18283,18285,18286,18287,18288,18289,18291,18292,
    18293,18295,18296,18297,18299,18303,18309,18311,18313,18314,18315,18316,
    18317,18318,18319,18320,18321,18540,18541,18550,18551,18552,18554,18557,
    18566,18594,18595,18622,
    #33
    18290,
    #35
    14691,18487,18509,
    #90
    14616,14618,14620,14645,14675,16407,16408,16409,18170,18171,18172,19474,
    #47
    16776,16771,16772,16774,16775,#!!! Есть 5-значный 16773
    #48
    18696,18909,
    #50
    16343,18117,18272,18273,18274,  
    #54
    15906,15956,15958,15971,15974,16335,16483,16495,16500,16506,16546,16548,16740,16745,15039,15041,15042,
    15148,15151,15153,15159,15160,15163,15173,15180,15182,15185,15878,15885,16547,16556,16741,16746,
    #57
    18008, 18009, 18010, 18011, 18031,
    #Буньед Лукмонов 68
    16545,16346,
    #Мирсаид Хайдоров #454
    18118,18122,
    #Мирсаид Хайдоров #453
    19379,19380,19381,19382,19383,19384,
    #Мирсаид Хайдоров #638
    18023,15899,15932,15992,18025,19227,19228,19229,

    #Мирсаид Хайдоров #

    ]
}
tempSaveLimits = {
    'cofe':{
        #377 письмо временное хранение
        '31335':{'wo':84795},
    },
    'rmpd':{}
}



# Читает отчёт из 1С и возвращает цену в сумах, группу учёта
def OneC():
    output = pd.read_excel("1. 1C.xlsx")

    output.rename(columns={
        'Unnamed: 1': 'Kod',
        'Unnamed: 2': 'Name',
        'Unnamed: 5': 'Qty1',
        'Unnamed: 6': 'Sum1',
        'Unnamed: 7': 'Qty2',
        'Unnamed: 8': 'Sum2'
    }, inplace=True)

    output = output.iloc[16:][['Kod', 'Name', 'Qty1', 'Sum1', 'Qty2', 'Sum2']]

    output.fillna({'Sum1': 0, 'Sum2': 0, 'Qty1': 0, 'Qty2': 0}, inplace=True)
    output['Цена'] = (output['Sum1']+output['Sum2']) / \
        (output['Qty1']+output['Qty2'])

    output['Kod'] = output['Kod'].astype(str)
    output['Kod'] = output['Kod'].map(lambda x: x.strip())
    output['Код товара'] = output['Kod'].copy().map(lambda x: '0000' + x if len(x) == 1 else '000' +
                                                    x if len(x) == 2 else '00' + x if len(x) == 3 else '0' + x if len(x) == 4 else x[-5:])

    output['Account'] = output['Kod'].copy()
    output.loc[~output['Name'].isna(), 'Account'] = np.nan
    output['Account'] = output['Account'].ffill()

    return output.loc[~output['Name'].isna(), ['Account', 'Код товара', 'Цена', 'Qty1', 'Sum1', 'Qty2', 'Sum2']]


# Читает и распечатывает накладную из 1С
def OneCW():
    waybill = pd.read_excel("1. 1CW.xlsx")
    waybill = waybill[['Unnamed: 6', 'Unnamed: 1', 'Unnamed: 11',
                       'Unnamed: 23', 'Unnamed: 15', 'Unnamed: 24']].iloc[16:]
    waybill = waybill.loc[~waybill['Unnamed: 6'].isnull()]
    waybill.to_excel('4. waybill.xlsx', index=False)


# Transactions из сгруппированных WO расщепляются с учётом spares из зависимых WO
def spread(transactions, spares, inactive_Master_Reservations, repMonth, repYear):
    transacts = transactions.copy()




    ### Список Master Reservations
    targetDF = transacts.loc[(transacts['Is Master Work Order'] == 'yes') 
                             & 
                             (~(transacts['Reservation Number'].isin(inactive_Master_Reservations)))
                             ]




    ### Master Reservations с реальным Qty, учитывающим уменьшение от Return to Stock
    MRs = targetDF.copy().groupby(['Reservation Number', 'Код товара', 'Материал', 'Ед.изм.', 'Work Order Status Description', 'closedMonth',
                                   'Отдел', 'Reserved By', 'WO №', 'reservYear', 'reservMonth', 'Asset Description', 'Объект', 'closedYear',
                                   'Catalogue Number','isRMPD_planner','raisedYear','raisedMonth','isRMPD',]).sum()
    MRs.reset_index(drop=False, inplace=True)


    ### !!! Exception 2 parts reservation execution
    excepts = {
        12533:{'transactMonth':8,'transactYear':2024},
        16650:{'transactMonth':11,'transactYear':2024},
        18649:{'transactMonth':12,'transactYear':2024},
        18982:{'transactMonth':12,'transactYear':2024},
        19620:{'transactMonth':1,'transactYear':2025},
    }



    ### Возвращает transactMonth, transactYear из-за потери после группировки
    for i, row in MRs.iterrows():
        originalData = targetDF[(targetDF['Reservation Number'] == row['Reservation Number']) 
                                &
                                (targetDF['Catalogue Transaction Action Name'] == 'Issue')]
        if row['Reservation Number']==12533:
            print(row['Reservation Number'] in excepts.keys())
        
        if len(originalData)>1 and row['Reservation Number'] in excepts.keys():
            MRs.at[i, 'transactMonth'] = excepts[ row['Reservation Number'] ]['transactMonth']
            MRs.at[i, 'transactYear']  = excepts[ row['Reservation Number'] ]['transactYear']
        elif len(originalData)>1 and row['Reservation Number'] not in excepts.keys():
            print('Error, 2 times taken: ', row['Reservation Number'])
            raise RuntimeError("'Error, 2 times taken: ",row['Reservation Number'])
        elif len(originalData)==1:
            MRs.at[i, 'transactMonth'] = originalData['transactMonth'].iloc[0]
            MRs.at[i, 'transactYear']  = originalData['transactYear'].iloc[0]
        else:
            print('Error, not found: ', row['Reservation Number'])
            return
        


    ### Список spares с комментом-ссылкой на master Reservations
    childSpares = spares.loc[ (~spares['Spares Comment'].isna()) 
                              & 
                              (spares['Spares Comment'].str.isnumeric())
                            ].copy()
    childSpares['Spares Comment'] = childSpares['Spares Comment'].astype(float)

    """### Exception overlimit Bobur
    childSpares = childSpares.loc[ ~((childSpares['Work Order Number']==137430)
                                  &
                                  (childSpares['Spares Comment']==22611))]
    childSpares.loc[ (childSpares['Work Order Number']==126413)
                    &
                    (childSpares['Spares Comment']==5387), 'Estimated Quantity'] = 8.74"""




    Limits = pd.DataFrame()

    checkHasValues = False



    for i, MR in MRs.iterrows():
        # Проверка - есть ли вобще изменения в лимите для каждой master Reservation
        if childSpares.loc[ childSpares['Spares Comment'] == MR['Reservation Number'] ].size != 0:
            checkHasValues = True

            for i, childSpare in childSpares.loc[childSpares['Spares Comment'] == MR['Reservation Number']].iterrows():
                record = pd.DataFrame({
                    'master WO №': MR['WO №'],
                    'master WO Status': MR['Work Order Status Description'],
                    'master Reservation Reserved By': MR['Reserved By'],
                    'master Reservation №': MR['Reservation Number'],
                    'master Reservation material': MR['Материал'],
                    'master Reservation Material Code': MR['Код товара'],
                    'master Reservation Qty': MR['Quantity'],
                    'master Reservation transactYear': MR['transactYear'],
                    'master Reservation transactMonth': MR['transactMonth'],
                    'is child transaction': 'yes'
                }, index=[0])
                for key in childSpare.index:
                    record[key] = childSpare[key]

                Limits = pd.concat([Limits, record]).reset_index(drop=True)

        else:
            record = pd.DataFrame({
                'master WO №': MR['WO №'],
                'master WO Status': MR['Work Order Status Description'],
                'master Reservation Reserved By': MR['Reserved By'],
                'master Reservation №': MR['Reservation Number'],
                'master Reservation material': MR['Материал'],
                'master Reservation Material Code': MR['Код товара'],
                'master Reservation Qty': MR['Quantity'],
                'master Reservation transactMonth': MR['transactMonth'],
                'master Reservation transactYear': MR['transactYear'],
                'is child transaction': 'no'
            }, index=[0])

            Limits = pd.concat([Limits, record]).reset_index(drop=True)
    
    
    ### Если ни одного изменения не было, то отмена
    if checkHasValues == False:
        print('no changes in limits')
        return transacts
    print('limits were changed')




    ############## Exception Электроды кг->тн расход
    Limits.loc[ Limits['master Reservation Material Code']=='05140','Estimated Quantity' ] /= 1000
    Limits.loc[ Limits['master Reservation Material Code']=='05140','UOMDescription' ] = 'тн'
    #######################################################################################




    ### Суммирует Estimated Q-ty зависимых WO и уменьшает количество в Master Reservation Q-ty
    for i, MR in MRs.iterrows():
        usedQty = Limits.loc[ Limits['master Reservation №'] == MR['Reservation Number'], 'Estimated Quantity' ].sum().item()
        Limits.loc[ 
                    Limits['master Reservation №'] == MR['Reservation Number'],'Remain Qty'
                   ] = Limits['master Reservation Qty'] - usedQty



    ### Создает Limits2 на основании Limits
    Limits2 = Limits.groupby(['master Reservation №', 'master WO №', 'master Reservation material',
                             'master Reservation Qty', 'Remain Qty'])['Actual Quantity'].count()
    Limits2 = Limits2.reset_index(drop=False)
    Limits2 = Limits2[['master WO №', 'master Reservation №',
                       'master Reservation material', 'master Reservation Qty',	'Remain Qty']]



    ### Удаляет Master Reservations
    transacts = transacts.drop(targetDF.index)



    ### Создаёт псевдотранзакции для использования лимитов в зависимых WO
    counter = -9999
    for i, childSpare in Limits.loc[ Limits['is child transaction'] == 'yes' ].iterrows():
        counter -= 1
        pseudoTransaction = pd.DataFrame({
            'Код товара': childSpare['master Reservation Material Code'],
            'Материал': childSpare['master Reservation material'],
            'Ед.изм.': childSpare['UOMDescription'],
            'Quantity': childSpare['Estimated Quantity'],
            'Reservation Number': counter,
            'Work Order Status Description': childSpare['Work Order Status Description'],
            'closedMonth': childSpare['closedMonth'],
            'closedYear': childSpare['closedYear'],
            'transactMonth':childSpare['master Reservation transactMonth'],
            'transactYear': childSpare['master Reservation transactYear'],
            'Отдел': childSpare['Short Department Name'],
            'Reserved By': childSpare['master Reservation Reserved By'],
            'WO №': childSpare['Work Order Number'],
            'Asset Description': childSpare['Asset Description'],
            'Объект': childSpare['Asset Number'],
            'Catalogue Transaction Action Name': 'Issue'
        }, index=[0])

        transacts = pd.concat(
            [transacts, pseudoTransaction]).reset_index(drop=True)


    ### Создаёт псевдотранзакции для остатков Master Reservation Q-ty
    for i, MR in MRs.iterrows():
        pseudoTransaction = {}
        for field in MR.index:
            pseudoTransaction[field] = MR[field]
            pseudoTransaction['Catalogue Transaction Action Name'] = 'Issue'


        returned = targetDF.loc[(targetDF['Catalogue Transaction Action Name'] == 'Return to Stock')
                                & (targetDF['Reservation Number'] == MR['Reservation Number'])
                                & (targetDF['transactMonth'] == repMonth)
                                & (targetDF['transactYear'] == repYear)
                                ]
        

        pseudoTransaction['Quantity'] = Limits2.loc[
                                                    Limits2['master Reservation №'] == MR['Reservation Number'], 'Remain Qty'
                                                    ].item() - returned['Quantity'].sum().item() 
        
        pseudoTransaction = pd.DataFrame(pseudoTransaction, index=[0])
        transacts = pd.concat(
            [transacts, pseudoTransaction]).reset_index(drop=True)

        if returned.size > 0:
            for i, MRreturned in returned.iterrows():
                pseudoTransaction = {}
                for column in MRreturned.index:
                    pseudoTransaction[column] = MRreturned[column]
                pseudoTransaction = pd.DataFrame(pseudoTransaction, index=[0])
                transacts = pd.concat(
                    [transacts, pseudoTransaction]).reset_index(drop=True)

    Limits[['master Reservation Reserved By',	'master WO №',	'master WO Status',	'master Reservation №',	'master Reservation Material Code',
            'master Reservation material',	'master Reservation Qty',	'Work Order Spare Description',	'Estimated Quantity',	'Work Order Number',	'Work Order Description',
            'Work Order Status Description', 'closedMonth', 'closedYear',	'Asset Description',	'Asset Number']].to_excel('limits.xlsx', index=False)
    Limits2.to_excel('limits2.xlsx', index=False)

    return transacts
