import pandas as pd
from ...database.DF__budget import outsourceBudg


def getPayments():
    payments = pd.read_excel('1c.xls')



    payments['Дата оплаты'] = pd.to_datetime(payments['Дата оплаты'], format="%d.%m.%Y")
    payments['paidYear']  = payments['Дата оплаты'].dt.year
    payments['paidMonth'] = payments['Дата оплаты'].dt.month



    payments.rename(columns={
                        'Статус': 'Status', 
                        'Контрагент': 'Company name', 
                        'Валюта':'Currency', 
                        'Номер.1':'Contract', 
                        'Сумма':'Sum',
                        'Инициатор':'Initiator',
                        'Назначение платежа':'Scope'
                        }, inplace=True)
    
    payments['Currency'].replace({
                                'USD': 'usd', 
                                'сум': 'uzs',
                                'Евро': 'eur'
                                }, inplace=True)
    
    payments['Contract'] = payments['Contract'].str.upper()




    payments = payments.loc[ (payments['Status'] == 'Оплачен полностью') & ( payments['paidYear'] == 2024) ][['Initiator','Currency','Company name','Contract','Scope','paidMonth','Sum']]

    '''
    ### Exception старый контракт с 2023 года Махсусэнергогаз. Последняя оплата была в январе, стоимость закрыта
    payments.loc[ payments['Contract'] == 'UZGTL-CON-2858', 'Contract' ] = 'UZGTL-CON-23-984'
    ############################################################################################################
    '''


    ### Распределение по месяцам суммы оплаты в заависимости от PaidMonth
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    payments[[*months]] = 0
    for i in payments.index:
        payments.loc[ i, months[ int(payments.loc[i,'paidMonth'])-1] ] = payments.loc[i,'Sum']



    ### Пометка Outsource контрактов
    payments.loc[ payments['Initiator'] == 'Отдел контрактных услуг', 'Department'] = 'outsource'
    payments.loc[ payments['Contract'].isin(outsourceBudg['Contract'].unique()), 'Department'] = 'outsource'


    ### Пометка RMPD контрактов
    payments.loc[ (
                      (payments['Initiator'] == 'Отдел планирования ремонтных работ')
                    | (payments['Initiator'] == 'Отдел планирования регулярного технического обслуживания')
                  )
                  & 
                  (payments['Department']!='outsource'), 'Department'] = 'rmpd'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='rmpd', 'Contract' ].unique()) , 'Department'] = 'rmpd'


    ### Пометка CofE контрактов
    payments.loc[ (payments['Initiator'] == 'Отдел центра передового опыта')
                  & 
                  (payments['Department']!='outsource')
                  & 
                  (payments['Department']!='rmpd'), 'Department'] = 'cofe'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='cofe', 'Contract' ].unique() ), 'Department'] = 'cofe'
 

    ### Пометка MTK контрактов
    payments.loc[ (payments['Initiator'] == 'Отдел материально-технического контроля')
                 & 
                  (payments['Department']!='outsource')
                 & 
                  (payments['Department']!='rmpd')
                 & 
                  (payments['Department']!='cofe'), 'Department'] = 'mtk'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='mtk', 'Contract' ].unique() ), 'Department'] = 'mtk'



    ### Суммирование по каждому контракту, удаление не относящихся к maintenance 
    payments = payments.groupby(['Department','Currency','Contract','Company name']).sum()
    payments.reset_index(drop=False, inplace=True)
    payments = payments[['Department',	'Currency',	'Contract',	'Company name',	'Sum',	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]



    ### EUR -> USD
    for i in payments.loc[ payments['Currency']=='eur' ].index:
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Sum']:
            payments.loc[i,m] = payments.loc[i,m] * 1.07

    return payments


def sumPayments(df, department=False):    
    payments = df.copy()

    if department:
        payments = payments.loc[ payments['Department'] == department ]


    payments.loc[ payments.index[-1] + 1 ] = payments.loc[ payments['Currency'] == 'uzs' ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Contract'] = 'Summary local contracts in uzs'


    last_index = payments.index[-1] + 1
    for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Sum']:
        payments.loc[ last_index, m ] = payments.loc[ payments['Contract'] == 'Summary local contracts in uzs', m ].item() / 12500
    payments.loc[ payments.index[-1], 'Contract'] = 'Summary local contracts in usd'


    payments.loc[ payments.index[-1] + 1 ] = payments.loc[ (payments['Currency'] == 'usd') | (payments['Currency'] == 'eur') ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Contract'] = 'Summary foreign contracts in usd'

    
    payments.loc[ payments.index[-1]+1 ] = payments.loc[ payments['Contract'].isin(['Summary local contracts in usd', 'Summary foreign contracts in usd']) ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Contract'] = 'Summary all contracts in usd'

    payments.to_excel('sumpaym.xlsx')
    return payments   


def summaryData(department = False):
    payments = sumPayments(department)

    output = pd.DataFrame([
        {'':'Total budget, usd'},
        {'':'Total paid, usd'},
        {'':'Total budget used, %'},

        {'':'Local contracts budget, usd'},
        {'':'Local contracts budget paid, usd'},
        {'':'Local contracts budget used, %'},

        {'':'Local contracts budget, uzs'},
        {'':'Local contracts budget paid, uzs'},
        {'':'Local contracts budget used, %'},

        {'':'Foreign contracts budget, usd'},
        {'':'Foreign contracts budget paid, usd'},
        {'':'Foreign contracts budget used, %'},
    ])

    struct = [
        'Summary all contracts in usd',
        'Summary all contracts in usd',
        '',
        'Summary local contracts in usd',
        'Summary local contracts in usd',
        '',
        'Summary local contracts in uzs',
        'Summary local contracts in uzs',
        '',
        'Summary foreign contracts in usd',
        'Summary foreign contracts in usd',
        ''
    ]

    budgetSRC = {
        'outsource':outsourceBudg
    }
    budget = budgetSRC[department]

    


    for m in ['Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        for i in range(0, 12, 3):
            output.loc[ i, m ] = budget.loc[ budget['Contract'] == struct[i], m ].item()
        for i in range(1, 12, 3):
            output.loc[ i, m ] = payments.loc[ payments['Contract'] == struct[i], m ].item() 
        for i in range(2, 12, 3):
            output.loc[ i, m ] = output.loc[ i-1, m ].item() / output.loc[ i-2, m ].item()




    output.loc[ 12, '' ] = 'Cumulative'
    


    
    for i in range(0, 12):
        output.loc[ i + 13, '' ] = output.loc[ i, '' ]
        sum = 0
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            sum += output.loc[ i, m ].item()
            output.loc[ i + 13, m ] = sum 
    
    for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        for i in range(15, 25, 3):
            output.loc[ i, m ] = output.loc[ i-1, m ].item() / output.loc[ i-2, m ].item()
    

    output.to_excel('summaryData.xlsx')


def detailedData(department = False):
    payments = getPayments(department)

    output = pd.DataFrame([{'Contract':'Local contracts execution:'},])
    
    i = -2
    for x in outsourceBudg.loc[ outsourceBudg['Currency'] == 'uzs' ].index:
        i += 3
        for m in ['Company name', 'Contract', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            output.loc[ i, m ] = outsourceBudg.loc[ x, m ]
            if payments.loc[ payments['Contract'] == outsourceBudg.loc[ x, 'Contract' ] ].empty:
                output.loc[ i + 1, m ] = 0
            else:
                output.loc[ i + 1, m ] = payments.loc[ payments['Contract'] == outsourceBudg.loc[ x, 'Contract' ], m ].item()
            output.loc[ i + 2, m ] = (output.loc[ i + 1, m ] /  output.loc[ i, m ]) if m not in ['Company name', 'Contract'] else ''

    for x in payments.loc[ (~(payments['Contract'].isin(outsourceBudg['Contract']))) & (payments['Currency'] == 'uzs') ].index:
        i += 3
        for m in ['Company name', 'Contract', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            output.loc[ i, m ] = 0
            output.loc[ i + 1, m ] = payments.loc[ x, m ]
            output.loc[ i + 2, m ] = 0




    i += 3
    output.loc[ i, 'Contract' ] = 'Foreign contracts execution:'

    i -= 2
    for x in outsourceBudg.loc[ outsourceBudg['Currency'] == 'usd' ].index:
        i += 3
        for m in ['Company name', 'Contract', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            output.loc[ i, m ] = outsourceBudg.loc[ x, m ]
            if payments.loc[ payments['Contract'] == outsourceBudg.loc[ x, 'Contract' ] ].empty:
                output.loc[ i + 1, m ] = 0
            else:
                output.loc[ i + 1, m ] = payments.loc[ payments['Contract'] == outsourceBudg.loc[ x, 'Contract' ], m ].item()
            output.loc[ i + 2, m ] = (output.loc[ i + 1, m ] /  output.loc[ i, m ]) if m not in ['Company name', 'Contract'] else ''

    for x in payments.loc[ (~(payments['Contract'].isin(outsourceBudg['Contract']))) & ( (payments['Currency'] == 'usd') | (payments['Currency'] == 'eur') ) ].index:
        i += 2
        for m in ['Company name', 'Contract', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            output.loc[ i, m ] = 0
            output.loc[ i + 1, m ] = payments.loc[ x, m ]
            output.loc[ i + 2, m ] = 0


    
    ### Cumulative

    i += 1
    output.loc[ i, 'Contract' ] = 'Local contracts cumulative execution:'
    
    start_index = output.loc[ output['Contract'] == 'Local contracts execution:' ].index.to_list()[0] + 1
    finish_index = output.loc[ output['Contract'] == 'Foreign contracts execution:' ].index.to_list()[0]

    
    for x in range(start_index, finish_index, 3):
        i += 1
        output.loc[ i, 'Company name' ] = output.loc[ x, 'Company name' ]
        output.loc[ i, 'Contract' ] = output.loc[ x, 'Contract' ]
        sum = 0
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            sum += output.loc[ x, m ]
            output.loc[ i, m ] = sum
        
        i += 1
        output.loc[ i, 'Company name' ] = output.loc[ x + 1, 'Company name' ]
        output.loc[ i, 'Contract' ] = output.loc[ x + 1, 'Contract' ]
        sum = 0
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            sum += output.loc[ x + 1, m ]
            output.loc[ i, m ] = sum

        i += 1
        output.loc[ i, 'Company name' ] = ''
        output.loc[ i, 'Contract' ] = ''
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if output.loc[ i-2, m ].item() != 0:
                output.loc[ i, m ] = output.loc[ i-1, m ].item() / output.loc[ i-2, m ].item()
            else:
                output.loc[ i, m ] = 0




    i += 1
    output.loc[ i, 'Contract' ] = 'Foreign contracts cumulative execution:'
    
    start_index = output.loc[ output['Contract'] == 'Foreign contracts execution:' ].index.to_list()[0] + 1
    finish_index = output.loc[ output['Contract'] == 'Local contracts cumulative execution:' ].index.to_list()[0]

    
    for x in range(start_index, finish_index, 3):
        i += 1
        output.loc[ i, 'Company name' ] = output.loc[ x, 'Company name' ]
        output.loc[ i, 'Contract' ] = output.loc[ x, 'Contract' ]
        sum = 0
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            sum += output.loc[ x, m ]
            output.loc[ i, m ] = sum
        
        i += 1
        output.loc[ i, 'Company name' ] = output.loc[ x + 1, 'Company name' ]
        output.loc[ i, 'Contract' ] = output.loc[ x + 1, 'Contract' ]
        sum = 0
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            sum += output.loc[ x + 1, m ]
            output.loc[ i, m ] = sum

        i += 1
        output.loc[ i, 'Company name' ] = ''
        output.loc[ i, 'Contract' ] = ''
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if output.loc[ i-2, m ].item() != 0:
                output.loc[ i, m ] = output.loc[ i-1, m ].item() / output.loc[ i-2, m ].item()
            else:
                output.loc[ i, m ] = 0

    

    output = output[['Company name', 'Contract', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    output.to_excel('detailedData.xlsx')
    
    
