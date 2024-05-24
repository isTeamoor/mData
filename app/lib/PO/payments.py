import pandas as pd
from ...database.DF__budget import outsourceBudg

### Оплаты за 2024 год!
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
    for i, month in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
        payments[month] = payments.apply(lambda x: x['Sum'] if x['paidMonth'] == i + 1 else 0, axis=1)



    ### Пометка Outsource контрактов
    payments.loc[ payments['Contract'].isin(outsourceBudg['Contract'].unique()), 'Department'] = 'outsource'
    payments.loc[ payments['Initiator'] == 'Отдел контрактных услуг', 'Department'] = 'outsource'
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='outsource', 'Contract' ].unique() ) , 'Department'] = 'outsource'


    ### Пометка RMPD контрактов
    payments.loc[ (
                      (payments['Initiator'] == 'Отдел планирования ремонтных работ')
                    | (payments['Initiator'] == 'Отдел планирования регулярного технического обслуживания')
                  )
                  & 
                  (payments['Department']!='outsource'), 'Department'] = 'rmpd'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='rmpd', 'Contract' ].unique() ) , 'Department'] = 'rmpd'


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
    payments = payments.loc[ ~(payments['Department'].isna()) ]
    payments = payments.groupby(['Department','Currency','Contract','Company name']).sum()
    payments.reset_index(drop=False, inplace=True)
    payments = payments[['Department',	'Currency',	'Contract',	'Company name',	'Sum',	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]



    ### EUR -> USD
    for i in payments.loc[ payments['Currency']=='eur' ].index:
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Sum']:
            payments.loc[i,m] = payments.loc[i,m] * 1.07

    return payments


### Добавляет суммирующие строки в payments и фильтрует по выбранному департаменту
def sumPayments(department=False):    
    payments = getPayments()


    if department:
        payments = payments.loc[ payments['Department'] == department ]


    sum_row = payments[ payments['Currency'] == 'uzs' ].sum(numeric_only=True)
    sum_row['Contract'] = 'Summary local contracts in uzs'
    payments.loc[ len(payments) ] = sum_row

    sum_row = sum_row.apply(lambda x: x/12500 if pd.api.types.is_number(x) else x)
    sum_row['Contract'] = 'Summary local contracts in usd'
    payments.loc[ len(payments) ] = sum_row

    sum_row = payments[ (payments['Currency'] == 'usd') | (payments['Currency'] == 'eur') ].sum(numeric_only=True)
    sum_row['Contract'] = 'Summary foreign contracts in usd'
    payments.loc[ len(payments) ] = sum_row

    sum_row = payments[ payments['Contract'].isin(['Summary local contracts in usd', 'Summary foreign contracts in usd']) ].sum(numeric_only=True)
    sum_row['Contract'] = 'Summary all contracts in usd'
    payments.loc[ len(payments) ] = sum_row


    return payments   


### Отчёт об использовании бюджета (%), с cumulative
def summaryData(budget, department = False):
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
    

    return output


### Отчёт об использовании средств по каждому контракту, с cumulative
def detailedData(budget_src, type, cur, department = False):
    payments_src = sumPayments(department)

    if cur == 'local':
        budget = budget_src.loc[ budget_src['Currency'] == 'uzs' ].copy()
        payments = payments_src.loc[ payments_src['Currency'] == 'uzs' ].copy()
    if cur == 'foreign':
        budget = budget_src.loc[ (budget_src['Currency'] == 'usd') | (budget_src['Currency'] == 'eur') | (budget_src['Currency'] == 'rub') ].copy()
        payments = payments_src.loc[ (payments_src['Currency'] == 'usd') | (payments_src['Currency'] == 'eur') | (payments_src['Currency'] == 'rub') ].copy()



    if type == 'cumulative':
        budget[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']] = budget[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']].apply(lambda x: x.cumsum(), axis=1)
        payments[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']] = payments[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']].apply(lambda x: x.cumsum(), axis=1)



    budget['type'] = 'Plan'
    payments['type'] = 'Fact'



    output = pd.DataFrame([{'':'Local contracts'},])

    
    merged = budget.merge(payments, how = 'outer', on = ['Contract', 'type','Company name','Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    for contract in merged['Contract'].unique():
        plan = merged.loc[ (merged['Contract'] == contract) & (merged['type'] == 'Plan') ]
        fact = merged.loc[ (merged['Contract'] == contract) & (merged['type'] == 'Fact') ]
        if plan.empty:
            plan = pd.DataFrame({'Contract':contract, 'type':'Plan','Company name':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}, index=[0,])
        if fact.empty:
            fact = pd.DataFrame({'Contract':contract, 'type':'Fact','Company name':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}, index=[0,])

        sum_row = {}
        sum_row['type'] = '%'
        for m in ['Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if plan[m].item() == 0:
                sum_row[m] = 1
            else:
                sum_row[m] = fact[m].item()/plan[m].item()
        sum_row = pd.DataFrame(sum_row, index=[0,])
        
        output = pd.concat([output, plan, fact, sum_row], ignore_index=True)




    return output[['Company name', 'Contract', 'type', 'Sum', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    
    
def draw_report(department = False):

    budgetSRC = {
        'outsource':outsourceBudg
    }
    budget = budgetSRC[department]

    summaryData(budget, department).to_excel(f'{department}_summary.xlsx', index=False)

    detailedData(budget, 'monthly', 'local', department).to_excel(f'{department}_local_monthly.xlsx', index=False)
    detailedData(budget, 'cumulative', 'local', department).to_excel(f'{department}_local_cumulative.xlsx', index=False)

    detailedData(budget, 'monthly', 'foreign', department).to_excel(f'{department}_foreign_monthly.xlsx', index=False)
    detailedData(budget, 'cumulative', 'foreign', department).to_excel(f'{department}_foreign_cumulative.xlsx', index=False)

