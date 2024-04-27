import pandas as pd
from ...database.DF__budget import outsourceBudg, outsourceBudg_usd


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




    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    payments[[*months]] = 0
    for i in payments.index:
        payments.loc[ i, months[ int(payments.loc[i,'paidMonth'])-1] ] = payments.loc[i,'Sum']



    payments.loc[ payments['Initiator'] == 'Отдел контрактных услуг', 'Department'] = 'outsource'
    payments.loc[ payments['Contract'].isin(outsourceBudg['Contract'].unique()), 'Department'] = 'outsource'



    payments.loc[ (
                      (payments['Initiator'] == 'Отдел планирования ремонтных работ')
                    | (payments['Initiator'] == 'Отдел планирования регулярного технического обслуживания')
                  )
                  & 
                  (payments['Department']!='outsource'), 'Department'] = 'rmpd'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='rmpd', 'Contract' ].unique()) , 'Department'] = 'rmpd'



    payments.loc[ (payments['Initiator'] == 'Отдел центра передового опыта')
                  & 
                  (payments['Department']!='outsource')
                  & 
                  (payments['Department']!='rmpd'), 'Department'] = 'cofe'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='cofe', 'Contract' ].unique() ), 'Department'] = 'cofe'



    payments.loc[ (payments['Initiator'] == 'Гражданско-строительный отдел')
                 & 
                  (payments['Department']!='outsource')
                 & 
                  (payments['Department']!='rmpd')
                 & 
                  (payments['Department']!='cofe'), 'Department'] = 'civil'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='civil', 'Contract' ].unique() ), 'Department'] = 'civil'
    


    payments.loc[ (payments['Initiator'] == 'Отдел материально-технического контроля')
                 & 
                  (payments['Department']!='outsource')
                 & 
                  (payments['Department']!='rmpd')
                 & 
                  (payments['Department']!='cofe')
                 & 
                  (payments['Department']!='civil'), 'Department'] = 'mtk'
    
    payments.loc[ payments['Contract'].isin( payments.loc[ payments['Department']=='mtk', 'Contract' ].unique() ), 'Department'] = 'mtk'




    payments = payments.groupby(['Department','Currency','Contract','Company name']).sum()
    payments.reset_index(drop=False, inplace=True)
    payments = payments[['Department',	'Currency',	'Contract',	'Company name',	'Sum',	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]


    for i in payments.loc[ payments['Currency']=='eur' ].index:
        for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Sum']:
            payments.loc[i,m] = payments.loc[i,m] * 1.07


    return payments



def departmentPayments(department):
    payments = getPayments()

    payments = payments.loc[ payments['Department'] == department ]



    payments.loc[ payments.index[-1] + 1 ] = payments.loc[ payments['Currency'] == 'uzs' ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Company name'] = 'Summary local contracts in uzs'


    last_index = payments.index[-1] + 1
    for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Sum']:
        payments.loc[ last_index, m ] = payments.loc[ payments['Company name'] == 'Summary local contracts in uzs', m ].item() / 12500
    payments.loc[ payments.index[-1], 'Company name'] = 'Summary local contracts in usd'



    payments.loc[ payments.index[-1] + 1 ] = payments.loc[ (payments['Currency'] == 'usd') | (payments['Currency'] == 'eur') ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Company name'] = 'Summary foreign contracts in usd'


    
    payments.loc[ payments.index[-1]+1 ] = payments.loc[ payments['Company name'].isin(['Summary local contracts in usd', 'Summary foreign contracts in usd']) ].sum(numeric_only=True)
    payments.loc[ payments.index[-1], 'Company name'] = 'Summary all payments in usd'


    payments.to_excel('payments.xlsx')
