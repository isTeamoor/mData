import pandas as pd

def getPPE():
    ### 1. Создание DataFrame список сотрудников из штатного расписания
    stuff = pd.read_excel('МТХКР бўлими тузилмаси 09.08.2024.xlsx')
    stuff.columns = stuff.iloc[2]
    stuff = stuff.iloc[3:133]

    stuff['Лавозим mod'] = stuff['Лавозим'].apply(lambda x: x.split('/')[0])
    stuff['Лавозим mod'] = stuff['Лавозим mod'].apply(lambda x: x.split(' (')[0])
    stuff['Лавозим mod'].replace({
        "Участка бошлиғи SLU": "Участка бошлиғи",
        "Участка бошлиғи U&O": "Участка бошлиғи",
        "Участка бошлиғи PWU": "Участка бошлиғи",
        }, inplace=True)

    stuff.to_excel('stuff.xlsx', index=False)


    ### 2. Создание DataFrame нормарасход СИЗ
    ppe = pd.read_excel('Келишув_учун_СИЗлар_руйхати_таклифлар_2.xlsx')
    ppe.columns = ['#','Name','Quantity', "UOM", 'Period','1','2']
    ppe = ppe[['#','Name','Quantity', "UOM", 'Period']]
    ppe = ppe.iloc[2981:3615]

    # Удаление ненужных строк
    ppe = ppe.loc[ppe['Name']!="Qo'shimcha"]
    ppe = ppe.loc[ppe['#']!="Elektrotexnika laboratoriyasi"]

    # Форматирование названий СИЗ (+название должностей)
    ppe['Name'] = ppe['Name'].apply(lambda x: x.strip())
    ppe['Name'].replace({
        'Kombenizon (Bir martalik)':'Kombinzon  1 martalik',
        "Plash Suvdan (Yomg'irdan) himoya qilish uchun)":"Plash  Suvdan (Yomg'irdan) himoya qilish uchun"}, inplace = True)
    ppe['Name'] = ppe['Name'].apply(lambda x: x.strip() if 'Qishgi maxsus kiyim' not in x else "Qishgi maxsus kiyim  (Qishda tashqi ishlarda qo'shimcha umumiy ishlab chiqarish ifloslanishidan va mexanik ta'sirlardan himoya qilish uchun")

    # Замена названий штатных единиц, чтобы привести их в соответствие с df stuff
    ppe['Name'].replace({
        "Bo'lim boshlig'i": "Бўлим бошлиғи",
        "Bo'lim boshlig'I o'rinbosari": "Бўлим бошлиғи ўринбосари",
        "KTXKBT bo'yicha yetakchi muhandis (Kompyuterlashtirilgan texnik xizmat ko'rsatishni boshqarish tizimi)": "Техник хизмат кўрсатишни компютерлаштирилган бошқарув тизими етакчи мухандиcи",
        "KTXKBT muhandisi (Kompyuterlashtirilgan texnik xizmat ko'rsatishni boshqarish tizimi)": "Техник хизмат кўрсатишни компютерлаштирилган бошқарув тизими техниги",
        "Xarajatlar nazoratchisi": "Харажатлар назоратчиси",
        "Omborchi": "Омборчи",
        "Ish yurituvchi": "Иш юритувчи",
        "Uchastka boshlig'i": "Участка бошлиғи",
        "Statik uskunalar kichik  texnigi": "Статик ускуналар кичик техниги",
        "Statik uskunalar texnigi": "Статик ускуналар техниги",
        "Statik uskunalar muhandisi": "Статик ускуналар муҳандиси",
        "Statik uskunalar yetakchi mutaxassisi": "Статик ускуналар етакчи мутахассиси",
        "Elektr uskunalari muhandisi": "Электр ускуналари муҳандиси",
        "Elektr uskunalari yetakchi mutaxassisi": "Электр ускуналари етакчи мутахассиси",
        "Elektr uskunalari texnigi": "Электр ускуналари техниги",
        "Elektr uskunalari kichik texnigi": "Электр ускуналари кичик техниги",
        "Analizator bo`yicha yetakchi mutaxassis": "Анализаторлар етакчи мутахассиси",
        "Analizator bo`yicha texnik mutaxassis": "Анализаторлар техниги",
        "Analizator bo'yicha muhandis": "Анализаторлар мухадниси",
        "Analizator bo'yicha kichik texnik mutaxassis": "Анализаторлар кичик техниги",
        "Aylanuvchi mexanizmlar yetakchi mutaxassisi": "Айланувчи механизмлар етакчи мутахассиси",
        "Aylanuvchi mexanizmlar muhandisi": "Айланувчи механизмлар муҳандиси",
        "Aylanuvchi mexanizmlar bo'yicha texnik mutaxassis": "Айланувчи механизмлар техниги",
        "Aylanuvchi mexanizmlar bo'yicha kichik texnik mutaxassis": "Айланувчи механизмлар кичик техниги",
        "Nazorat o‘lchash asboblari yetakchi mutaxassisi": "Назорат ўлчаш асбоблари етакчи мутахассиси",
        "Nazorat o‘lchash asboblari muhandisi": "Назорат ўлчаш асбоблари муҳандиси",
        "Nazorat o‘lchash asboblari texnigi": "Назорат ўлчаш асбоблари техниги",
        "Nazorat o‘lchash asboblari kichik texnigi": "Назорат ўлчаш асбоблари кичик техниги",
        "Moylash mahsulotlarini hisobini yuritish va ehtiyot qismlar nazorati bo'yicha bosh mutaxassis": "Мойлаш маҳсулотлари ва эхтиёт қисмлар назорати бўйича бош мутахассиси",
        "Texnik xizmat ko'rsatishni rejalashtirish mutaxassisi": "Техник хизмат кўрсатишни режалаштириш етакчи мутахассиси",
        "Texnik xizmat ko'rsatishni rejalashtirish kichik mutaxassisi": "Техник хизмат кўрсатишни режалаштириш кичик мутахассиси",
        "Elektrotexnika laboratoriyasi boshlig'i": "Электротехника лабораторияси бошлиғи",
        "Elektr muhandisi": "Электротехника лабораторияси муҳандиси",
        "Elektromontyor": "Электротехника лабораторияси электромонтёри",
        "Yetakchi muhandis": "Электротехника лабораторияси етакчи мутахассиси"
    }, inplace=True)


    # Получение списка названий только штатных единиц
    stuff_name = ppe.loc[ ~(ppe['#'].isna()) ].copy()
    stuff_name = stuff_name.loc[ stuff_name['Name']!="Maxsus kiyim (Antistatik xususiyatlarga ega bo'lgan umumiy ishlab chiqarish ifloslanishi va mexanik ta'sirlardan himoya qilish uchun)" ]
    #stuff_name.to_excel('stuff_name.xlsx', index=False)
    aims = stuff_name['Name'].unique()

    
    # Добавления поля groups для дальнешейго заполнения вниз группирующего значения
    ppe['groups'] = ppe['Name'].copy().apply(lambda x: x if x in aims else None )
    ppe['groups'].fillna(method='ffill', inplace=True)

    #ppe.to_excel('ppe.xlsx', index=False)


    # Создание списка с кусками датафрейма норма расхода, сгруппированных по каждой штатке
    all_items = []
    for group_name, group_data in ppe.groupby('groups'):
        df = group_data.iloc[1:].copy()
        df['person'] = group_name
        all_items.append(df)

    all_items = pd.concat(all_items)
    all_items.to_excel('all_items.xlsx')

    # Перебор всех сотруднииков по списку, с добавлением для каждого датафрейма с нормой расхода для штатки
    result = []
    for i, row in stuff.iterrows():
        item = all_items.loc[ all_items['person']==row['Лавозим mod'] ]
        result.append(item)

    result = pd.concat(result)

    

    result = result.groupby(['Name','person','Period','UOM',]).sum()
    result.to_excel('result-old.xlsx')

    result.reset_index(drop=False, inplace=True)
    result['Freq'] = result['Period'].copy()
    result['Freq'].replace({
        'yaroqsiz holatga kelguncha':0.5,
        '3 yilda  1 marta':0.5,
        '1 yilda  1 marta':1,
        '1 yilda  2 marta':2,
        '5 yilda  1 marta':0.2,
        '2 yilda  1 marta':0.5,
        '1 yilda 1 marta':1,
        '6 oyda1 marta':2,
        '6 oyda 1 marta':2
    }, inplace=True)

    result['Qnty mod'] = result.apply(lambda x: x['Freq']*x['Quantity'], axis=1)
    result['Qnty mod'] = result.apply(lambda x: 12*x['Quantity'] 
                                      if x['Name']=="Qo'lqop  (Mexanik ta'sirlardan (jarohatlar, kesilishlardan) himoya qilish uchun)"
                                      else x['Qnty mod'], axis=1)
    

    # Создание суммарного и детализированных файлов
    total_RPMD = result.groupby(['Name','Freq','Period'])[['Qnty mod','Quantity']].sum()

    total_RPMD.to_excel('total_RMPD.xlsx')
    """result = result.groupby(['Name','person','Freq','UOM',]).sum()
    result.to_excel('result-old.xlsx')"""

### 2. Бюджет Outsource
outsourceBudg = pd.DataFrame(
    [
        {'Currency':'uzs','Company name':'UNGM-DR','SoW':'Maintenance Rotating Services','Contract':'03-0007/22/UZGTL-CON-2262','opex':'-','capex':'-','working capital':'-','Sum':1920000000,'Jan':160000000,'Feb':160000000,'Mar':160000000,'Apr':160000000,'May':160000000,'Jun':160000000,'Jul':160000000,'Aug':160000000,'Sep':160000000,'Oct':160000000,'Nov':160000000,'Dec':160000000},
        {'Currency':'uzs','Company name':'UZPROMARM','SoW':'Maintenance Rotating Services','Contract':'UZGTL-CON-2677','opex':'-','capex':'-','working capital':'-','Sum':0,'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0},
        {'Currency':'uzs','Company name':'Uzbekximmash','SoW':'Maintenance Rotating Services','Contract':'UZGTL-CON-2487','opex':'-','capex':'-','working capital':'-','Sum':1800000000,'Jan':200000000,'Feb':100000000,'Mar':200000000,'Apr':100000000,'May':200000000,'Jun':100000000,'Jul':200000000,'Aug':100000000,'Sep':200000000,'Oct':100000000,'Nov':100000000,'Dec':200000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz Scaffolding','SoW':'Maintenance Scaffolding','Contract':'UZGTL-CON-23-984','opex':'-','capex':'-','working capital':'-','Sum':2100000000,'Jan':200000000,'Feb':200000000,'Mar':100000000,'Apr':100000000,'May':100000000,'Jun':200000000,'Jul':200000000,'Aug':200000000,'Sep':200000000,'Oct':200000000,'Nov':200000000,'Dec':200000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz Insulation','SoW':'Maintenance Insulation ','Contract':'UZGTL-CON-23-985','opex':'-','capex':'-','working capital':'-','Sum':2100000000,'Jan':300000000,'Feb':300000000,'Mar':100000000,'Apr':100000000,'May':200000000,'Jun':100000000,'Jul':100000000,'Aug':100000000,'Sep':100000000,'Oct':200000000,'Nov':200000000,'Dec':300000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz','SoW':'Maintenance Welding & painting','Contract':'UZGTL-CON-23-182','opex':'-','capex':'-','working capital':'-','Sum':2400000000,'Jan':200000000,'Feb':200000000,'Mar':200000000,'Apr':200000000,'May':200000000,'Jun':200000000,'Jul':200000000,'Aug':200000000,'Sep':200000000,'Oct':200000000,'Nov':200000000,'Dec':200000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz (FGS)','SoW':'Instrumentation Services','Contract':'UZGTL-CON-24-269','opex':'-','capex':'-','working capital':'-','Sum':4140000000,'Jan':345000000,'Feb':345000000,'Mar':345000000,'Apr':345000000,'May':345000000,'Jun':345000000,'Jul':345000000,'Aug':345000000,'Sep':345000000,'Oct':345000000,'Nov':345000000,'Dec':345000000},
        {'Currency':'uzs','Company name':'SGCC(UZGTL-CON-2988)','SoW':'Maintenance Additional Services','Contract':'UZGTL-CON-2988','opex':'-','capex':'-','working capital':'-','Sum':600000000,'Jan':50000000,'Feb':50000000,'Mar':50000000,'Apr':50000000,'May':50000000,'Jun':50000000,'Jul':50000000,'Aug':50000000,'Sep':50000000,'Oct':50000000,'Nov':50000000,'Dec':50000000},
        {'Currency':'uzs','Company name':'Motor rewind and repair','SoW':'Maintenance Electrical Services','Contract':'?','opex':'-','capex':'-','working capital':'-','Sum':200000000,'Jan':0,'Feb':0,'Mar':50000000,'Apr':0,'May':0,'Jun':50000000,'Jul':0,'Aug':0,'Sep':50000000,'Oct':0,'Nov':0,'Dec':50000000},
        {'Currency':'uzs','Company name':'Transformer repair service','SoW':'Maintenance Electrical Services','Contract':'??','opex':'-','capex':'-','working capital':'-','Sum':200000000,'Jan':0,'Feb':0,'Mar':50000000,'Apr':0,'May':0,'Jun':50000000,'Jul':0,'Aug':0,'Sep':50000000,'Oct':0,'Nov':0,'Dec':50000000},
        {'Currency':'usd','Company name':'Team industrial services','SoW':'Maintenance static services','Contract':' ???','opex':'-','capex':'-','working capital':'-','Sum':150000,'Jan':0,'Feb':0,'Mar':37500,'Apr':0,'May':0,'Jun':37500,'Jul':0,'Aug':0,'Sep':37500,'Oct':0,'Nov':0,'Dec':37500},
        {'Currency':'usd','Company name':'Mitsubishi','SoW':'Maintenance Rotating Services','Contract':'UZGTL-CON-24-631','opex':'-','capex':'-','working capital':'-','Sum':100000,'Jan':0,'Feb':0,'Mar':25000,'Apr':0,'May':0,'Jun':25000,'Jul':0,'Aug':0,'Sep':25000,'Oct':0,'Nov':0,'Dec':25000},
        {'Currency':'usd','Company name':'ABB Service','SoW':'Maintenance Electrical Services','Contract':'????','opex':'-','capex':'-','working capital':'-','Sum':48000,'Jan':0,'Feb':0,'Mar':12000,'Apr':0,'May':0,'Jun':12000,'Jul':0,'Aug':0,'Sep':12000,'Oct':0,'Nov':0,'Dec':12000},
        {'Currency':'usd','Company name':'Siemens VSD repair service','SoW':'Maintenance Electrical Services','Contract':'?????','opex':'-','capex':'-','working capital':'-','Sum':60000,'Jan':0,'Feb':0,'Mar':15000,'Apr':0,'May':0,'Jun':15000,'Jul':0,'Aug':0,'Sep':15000,'Oct':0,'Nov':0,'Dec':15000},
        {'Currency':'usd','Company name':'EINSTEK (EPMS) Service','SoW':'Maintenance Electrical Services','Contract':'??????','opex':'-','capex':'-','working capital':'-','Sum':60000,'Jan':0,'Feb':0,'Mar':15000,'Apr':0,'May':0,'Jun':15000,'Jul':0,'Aug':0,'Sep':15000,'Oct':0,'Nov':0,'Dec':15000},
        {'Currency':'usd','Company name':'Gutor (UPS SYSTEM) Service & Training','SoW':'Maintenance Electrical Services','Contract':'UZGTL-CON-23-290','opex':'-','capex':'-','working capital':'-','Sum':48000,'Jan':0,'Feb':0,'Mar':12000,'Apr':0,'May':0,'Jun':12000,'Jul':0,'Aug':0,'Sep':12000,'Oct':0,'Nov':0,'Dec':12000},
        {'Currency':'usd','Company name':'GE Oil and Gas(Baker Hughes GE company)','SoW':'Vendor commissioning services','Contract':'???????','opex':'-','capex':'-','working capital':'-','Sum':415896.04,'Jan':0,'Feb':0,'Mar':110000,'Apr':0,'May':0,'Jun':110000,'Jul':0,'Aug':0,'Sep':110000,'Oct':0,'Nov':0,'Dec':85896.04},
        {'Currency':'usd','Company name':'Severn Glocon','SoW':'Instrumentation Services','Contract':'UZGTL-CON-24-694','opex':'-','capex':'-','working capital':'-','Sum':50000,'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':25000,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':25000},
        {'Currency':'usd','Company name':'MEX - CMMS online support','SoW':'Ehtiyoj bo`lgancha MEX sistemasiga qo`shimcha yangilanishlar kiritish uchun','Contract':'UZGTL-CON-1790','opex':'-','capex':'-','working capital':'-','Sum':10000,'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':10000,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0},
        {'Currency':'','Company name':'','SoW':'','Contract':'Summary local contracts in uzs','opex':'-','capex':'-','working capital':'-','Sum':15460000000,'Jan':1455000000,'Feb':1355000000,'Mar':1255000000,'Apr':1055000000,'May':1255000000,'Jun':1255000000,'Jul':1255000000,'Aug':1155000000,'Sep':1355000000,'Oct':1255000000,'Nov':1255000000,'Dec':1555000000},
        {'Currency':'','Company name':'','SoW':'','Contract':'Summary local contracts in usd','opex':'-','capex':'-','working capital':'-','Sum':1189230.76923077,'Jan':111923.076923077,'Feb':104230.769230769,'Mar':96538.4615384615,'Apr':81153.8461538462,'May':96538.4615384615,'Jun':96538.4615384615,'Jul':96538.4615384615,'Aug':88846.1538461538,'Sep':104230.769230769,'Oct':96538.4615384615,'Nov':96538.4615384615,'Dec':119615.384615385},
        {'Currency':'','Company name':'','SoW':'','Contract':'Summary foreign contracts in usd','opex':'-','capex':'-','working capital':'-','Sum':941896.04,'Jan':0,'Feb':0,'Mar':226500,'Apr':0,'May':0,'Jun':261500,'Jul':0,'Aug':0,'Sep':226500,'Oct':0,'Nov':0,'Dec':227396.04},
        {'Currency':'','Company name':'','SoW':'','Contract':'Summary all contracts in usd','opex':'-','capex':'-','working capital':'-','Sum':2131126.80923077,'Jan':111923.076923077,'Feb':104230.769230769,'Mar':323038.461538462,'Apr':81153.8461538462,'May':96538.4615384615,'Jun':358038.461538462,'Jul':96538.4615384615,'Aug':88846.1538461538,'Sep':330730.769230769,'Oct':96538.4615384615,'Nov':96538.4615384615,'Dec':347011.424615385},

    ]
)

### 3. Бюджет RMPD
rmpdBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':11489985, 'Jan':957499, 'Feb':957499, 'Mar':957499, 'Apr':957499, 'May':957499, 'Jun':957499, 'Jul':957499, 'Aug':957499, 'Sep':957499, 'Oct':957499, 'Nov':957499, 'Dec':957499},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':11489985, 'Jan':957499, 'Feb':957499, 'Mar':957499, 'Apr':957499, 'May':957499, 'Jun':957499, 'Jul':957499, 'Aug':957499, 'Sep':957499, 'Oct':957499, 'Nov':957499, 'Dec':957499},
    ]
)

### 4. Бюджет CofE
cofeBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':2325230, 'Jan':193770, 'Feb':193770, 'Mar':193770, 'Apr':193770, 'May':193770, 'Jun':193770, 'Jul':193770, 'Aug':193770, 'Sep':193770, 'Oct':193770, 'Nov':193770, 'Dec':193770},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':2325230, 'Jan':193770, 'Feb':193770, 'Mar':193770, 'Apr':193770, 'May':193770, 'Jun':193770, 'Jul':193770, 'Aug':193770, 'Sep':193770, 'Oct':193770, 'Nov':193770, 'Dec':193770},
    ]
)

### 5. Бюджет TAR
tarBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':19000000, 'Jan':1583333, 'Feb':1583333, 'Mar':1583333, 'Apr':1583333, 'May':1583333, 'Jun':1583333, 'Jul':1583333, 'Aug':1583333, 'Sep':1583333, 'Oct':1583333, 'Nov':1583333, 'Dec':1583333},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':19000000, 'Jan':1583333, 'Feb':1583333, 'Mar':1583333, 'Apr':1583333, 'May':1583333, 'Jun':1583333, 'Jul':1583333, 'Aug':1583333, 'Sep':1583333, 'Oct':1583333, 'Nov':1583333, 'Dec':1583333},
    ]
)

### 6. Бюджет MTK
mtkBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':924000000, 'Jan':77000000, 'Feb':77000000, 'Mar':77000000, 'Apr':77000000, 'May':77000000, 'Jun':77000000, 'Jul':77000000, 'Aug':77000000, 'Sep':77000000, 'Oct':77000000, 'Nov':77000000, 'Dec':77000000},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':73920, 'Jan':6160, 'Feb':6160, 'Mar':6160, 'Apr':6160, 'May':6160, 'Jun':6160, 'Jul':6160, 'Aug':6160, 'Sep':6160, 'Oct':6160, 'Nov':6160, 'Dec':6160},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':73920, 'Jan':6160, 'Feb':6160, 'Mar':6160, 'Apr':6160, 'May':6160, 'Jun':6160, 'Jul':6160, 'Aug':6160, 'Sep':6160, 'Oct':6160, 'Nov':6160, 'Dec':6160},
    ]
)