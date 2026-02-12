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
             {"field": 'Reserved By', "operator": "==", "value": "'Mirjahon Toirov CofE'"},
             "|",
             {"field": 'Reserved By', "operator": "==", "value": "'Jahongir Haydarov Ilhom o`g`li'"}
             ]
}


# Номера Материальных Кодов, относящихся к 014 Забалансовому счёту
is_014 = ['',
'06935', '05841', '07139', '05230', '04189', '03494', '02799', '05749', '01738', '01308', '01309', '01310', '01311', '01312', '01329', '01330', '01331', '01333', '01351', '01354', '01372', '01374', '01376','01876',
'01377', '01378', '00892', '02204', '04179', '00158', '00140', '00134', '00114', '00915', '01278', '01276', '01275', '01277', '01272', '01279', '03190', '02995', '02806', '02812', '02813', '02814', '02826', '02827',
'02828', '02830', '02896', '02897', '01307', '01353', '01373', '03904', '01375', '02325', '01393', '03484', '03017', '02786', '03019', '04662', '00899', '03745', '01367', '02890', '02891', '02892', '02893', '02894',
'02452', '02092', '02451', '02817', '00155', '00156', '00526', '00002', '04188', '02910', '06597', '07277', '01622', '01625', '01623', '01626', '01624', '03222', '01628', '01630', '01627', '01632', '00009', '00001',
'04346', '01274', '01273', '01352', '02854', '02863', '02885', '03480', '01349', '03226', '02824', '02935', '01344', '06601', '06600', '01337', '01313', '01315', '01316', '01317', '01320', '01321', '01322','31722',
'01323', '01325', '01326', '01327', '01568', '01635', '01570', '01571', '01588', '01590', '01591', '01636', '01603', '01604', '01621', '02804', '02807', '02809', '02815', '06598', '02816', '02818', '02819', '02820',
'02821', '02822', '02823', '02831', '02834', '02840', '02845', '02846', '02847', '02848', '02851', '02856', '02858', '02860', '02861', '02864', '02878', '02880', '02881', '02882', '02883', '02884', '02886', '60599',
'02887', '02888', '02899', '02900', '02901', '02902', '02903', '02906', '02936', '03260', '00809', '00810', '02453', '00678', '00157', '00203', '00113', '00158', '00159', '06136', '01575', '01578', '00154', '06899',
'02450', '05359', '06799', '03227', '01379', '01382', '01314', '01319', '02879', '01366', '02857', '02865', '00007', '00008', '05942', '04140', '05752', '06330', '01189', '01324', '00865', '01369', '00863', '01355',
'01387', '00804', '01587', '01328', '01332', '02829', '01406', '00806', '00805', '01338', '01342', '01343', '01339', '01340', '01341', '02855', '02852', '03223', '02862', '01334', '01335', '01336', '02850', '02859',
'02853', '01403', '01574', '01576', '01577', '01582', '01360', '01361', '01364', '01365', '01429', '01407', '00691', '00692', '00693', '00694', '00695', '00700', '00703', '00702', '00705', '00706', '00707', '00708',
'01350', '01371', '01380', '01381', '01383', '01384', '01385', '01386', '01394', '01395', '01396', '01398', '01399', '01589', '01639', '01606', '01620', '02835', '00189', '00745', '00140', '00230', '00738', '05232',
'05231', '00899', '00155', '00114', '00157', '00526', '00113', '01201', '01202', '01203', '01204', '06340', '02911', '02912', '02913', '07481', '07407', '07473', '07403', '02802', '03229', '05305', '06122', '06332',
'06900', '07497', '07883', '07882', '09300', '07331', '05831', '09767', '01875', '04183', '09359', '02811', '07626', '07627', '07628', '07629', '07616', '07617', '10920', '05157', '28160', '28335', '09361', '09331',
'03014', '06326', '00704', '05824', '09605', '09606', '12414', '09608', '01517', '02838', '11063', '02794', '10518', '12500', '27290', '24631', '06304', '06331', '12497', '12499', '19400', '09332', '37515',
'01572', '01585', '30445', '05318', '01874', '06333', '16999', '02907', '31108', '05965', '29618', '02032', '02033', '18881', '21146', '26188', '02803', '35091', '37388', '36826', '39771',
'29764','29763','29762','29767','29768','29769','29770','29771','29772','29773','29774','29775','29776','29777','29778','29779','29780','29765','29766','29760','29759','29757','29755','29756',
'29739','29740','29741','29742','29743','29744','29745','29746','29747','29748','29749','29750','29761','29733','29751','29752','29753','29758','29738','29731','29732','29737','29734','29735',
'29736','29754','33553','10517','18700','33471', '24617','24618','03259','07816','36067','36068','36069','36070','36071','36098','42108',
'36072','36073','36074','36075','36076','36077','36078','36079','36080','36081','36082','36083','36084','36085','17602','35761','34621','34622','34623','39478','39479','30715',


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
'39496',

#Кабель (Бобур использовал 1 раз, не может вернуть)
#'15698',

#Инструменты с TAR
'03014','30640','31438','31364','24788','24787','00705','00706','00707','00708','00691','00692',
'00693','00694','00695','00703','00702','00704','00701','30642','32399','32400','32401','32402','32403','32404',
'32405','32406','32407','32408','32409','32410','32411','32412','32413','32414','32415','32416','32417','32418',
'01619',
'26786','26787','26793','34546','37900',
'03015','41785','41748','41139','40095','41747','41749','41750', '41751', '41752', '41753', '41785',

#Cluster Filter Fisher Tropsh
'30652',

#Баллоны от Нормуминов Достона на времХран
'39700','39701','39702','39703','39704','39705','39706','39707','39708','39709','39710','39711','39712','39713',
'39714','39715','39716','39717','39718','39719','39720','39721','39722','39723','39724','39725','39726','39727',
'39728','39729','39730','39731','39732','39733','39734','39735','39736','39737','39738','39739','39740','39741',
'39742','39743','39744','39745','39746','39747','39748','39749','39750','39751','39752','39753','39754','39755',
'39756','39757','39758','39759','39760',
#Найденные запчасти Мирсаида Хайдарова. Часть 1
'40094','40093','40092','40091','40090','40089','40088','40087','40086','40085','40084','40083','40082','40081',
'40080','40079','40078','40077','40076','40075','40074','40073','40072','40071','40070','40069','40068','40067',
'40066','40065','40064','40063','40062','40061','40060','40059','40058','40057','40056','40055','40054','40053',
'40052','40051','40050','40049','40048','40047','40046','40045','40044','40043','40042','40041','40040','40039',
'40038','40037','40036','40035','40034','40033','40032','40031','40030','40029','40028','40027','40026','40025',
'40024','40023','40022','40021','40020','40019','40018','40017','40016','40015','40014','40013','40012','40011',
'40010','40009','40008','40007','40006','40005','40004','40003','40002','40001','40000','39999','39998','39997',
'39996','39995','39994','39993','39992','39991','39990','39989','39988','39987','39986','39985','39984','39983',
'39982','39981','39980','39979','39978','39977','39976','39975','39974','39973','39972','39971','39970','39969',
'39968','39967','39966','39965','39964','39963','39962','39961','39960','39959','39958','39957','39956','39955',
'39954','39953','39952','39951','39950','39949','39948','39947','39946','39945','39944','39943','39942','39941',
'39940','39939','39938','39937','39936','39935','39934','39933','39932','39931',
#Найденные запчасти Мирсаида Хайдарова. Часть 2
'40196','40195','40194','40193','40192','40191','40190','40189','40188','40187','40186','40185','40184','40183',
'40182','40181','40180','40179','40178','40177','40176','40175','40174','40173','40172','40171','40170','40169',
'40168','40167','40166','40165','40164','40163','40162','40161','40160','40159','40158','40157','40156','40155',
'40154','40153','40152','40151','40150','40149','40148','40147','40146','40145','40144','40143','40142','40141',
'40140','40139','40138','40137','40136','40135','40134','40133','40132','40131','40130','40129','40128','40127',
'40126','40125','40124','40123','40122','40121','40120','40119','40118','40117','40116','40115','40114','40113',
'40112',

#Используется для гидротеста
'12060',



]

is_wOff = ['09327', '09326', '07483', '12478', '09859',
           '07536', '05328', '06949', '09607', '16801', '09360', '11316','09297','08008',
           '28004','39616','06161',''
           
           ]

tempSave = { 
    'cofe':[],
    'rmpd':[
        #Уктам Ильхомов. Блайнд. Должен был быть списан в сентябре, в последний момент изменили. В октябре
        #26964,
        #Мирсаид Хайдоров 2359-письмо. Pump. Брали из нее прокладку, остальное возвращают
        #29199,
        #SLU
        #28105,28099,28386,28097,28096,28102,28098,28106,28101,
        
        #!!!Tar Jurabek письмо №ORD-083/15-2026!!! В феврале их на врем хран
        #здесь еще будет одна custom exception reservation когда возьму на баланс запчасть, списанную (материал код-35183 reserv-32428)
        #32790,33706,33704,34113,27095,33700,34112,33639,30874,32541,33442,33698,33848,


    ]
}
tempSaveLimits = {
    # Код товара
    'cofe':{
        #377 письмо временное хранение
        #'31335':{'wo':84795},
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
        30635:{'transactMonth':12,'transactYear':2025}
    }



    ### Возвращает transactMonth, transactYear из-за потери после группировки
    for i, row in MRs.iterrows():
        originalData = targetDF[(targetDF['Reservation Number'] == row['Reservation Number']) 
                                &
                                (targetDF['Catalogue Transaction Action Name'] == 'Issue')]
        
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
            raise RuntimeError("'Reservation not found in targetDF: ",row['Reservation Number'])
        


    ### Список spares с комментом-ссылкой на master Reservations
    childSpares = spares.loc[ (~spares['Spares Comment'].isna()) 
                              & 
                              (spares['Spares Comment'].str.isnumeric())
                            ].copy()
    childSpares['Spares Comment'] = childSpares['Spares Comment'].astype(float)

    ### !!!! Exception !!! #######################################################################
    # WO-141421, Master Reservation-23368
    childSpares.loc[ childSpares['Work Order Spare ID'] == 39821, 'Estimated Quantity' ] = 287.91
    ##############################################################################################



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

    ############## Exception Списать TAR материалы
    Limits.loc[ Limits['master WO №']==193250,'closedMonth' ] = 12
    Limits.loc[ Limits['master WO №']==193250,'closedYear' ] = 2025
    Limits.loc[ Limits['master WO №']==193250,'Work Order Status Description' ] = 'Closed'
    
    Limits.loc[ (Limits['master WO №']==193250) 
               & (Limits['Work Order Number'].isin([147084,174876,]))
               & (Limits['master Reservation Material Code']=='02025'),
               'closedMonth' ] = 1
    Limits.loc[ (Limits['master WO №']==193250) 
               & (Limits['Work Order Number'].isin([147084,174876,]))
               & (Limits['master Reservation Material Code']=='02025'),
               'closedYear' ] = 2026   
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
