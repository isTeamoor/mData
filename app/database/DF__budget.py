from .impo import budget
import pandas as pd


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


budget['Account Code'] = budget['Account Code'].astype('str')


for month in months:
    budget[month] = budget[month].fillna(0)


budget = budget[['Account Code', 'Account Code Description','Total','Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']]







budget_cofe = pd.DataFrame(
    [
        ['Departmental Training',        '210500000000', 1000, 1000,8000,0,1000,1000,1000,8000,1000,1000,1000,1000],
        ['Maintenance Scaffolding',      '210108010000', 30000,30000,30000,20000,20000,20000,20000,20000,20000,20000,20000,20001],
        ['Maintenance Insulation',       '210108020000', 50000,	100000,	100000,	100000,	100000,	100000,	100000,	100000,	100000,	100000,	100000,	100000],
        ['Smaller Modifications',        '210109140000', 10000,	10000,	5000,	5000,	5000,	5000,	5000,	10000,	10000,	10000,	10000,	10000],
        ['Mechanical Services',          '210109090000', 1292,	1292,	1292,	1292,	1292,	1292,	1292,	1292,	1292,	1292,	1292,	1292],
        ['Maintenance Welding',          '210109010000', 20000,	20000,	20000,	20000, 20000,	20000,	20000,	20000,	20000,	20000,	20000,	20000],
        ['Electrical Spares',	         '210109030000', 2000,	2000,	2000,	2000,	2000,	2000,	2000,	2000,	2000,	2000,	2000,	2000],
        ['General Maintenance Material', '210109130000', 4000,	4000,	4000,	4000,	4000,	4000,	4000,	4000,	4000,	4000,	4000,	4000],
        ['Lubricants',                   '210106100000', 3000,	3000,	3000,	3000,	3000,	3000,	3000,	3000,	3000,	3000,	3000,	3000],
        ['Lab Equipment <$5000 USD',     '210110010000', 50000,	50000,	50000,	22000,	12000,	11000,	10000,	10000,	10000,	10000,	10000,	10000],
        ['Tools Equipment <$5000 USD',   '210110040000', 800000,	800000,	200000,	200000,	200000,	100000,	100000,	100000,	100000,	100000,	100000,	100000]
    ],
    columns = ['Account Code Description', 'Account Code', *months]
)
budget_cofe.loc[len(budget_cofe)] = budget_cofe.sum(numeric_only=True)
budget_cofe.loc[len(budget_cofe)-1, 'Account Code Description'] = 'Total'
budget_cofe['Summary'] = budget_cofe.sum(axis=1, numeric_only=True)


budget_cofe_mod = pd.DataFrame()
for i, row in budget_cofe.loc[budget_cofe['Account Code Description']!='Total'].iterrows():
    for m, month in enumerate(months):
        record = pd.DataFrame({'Account Code Description':row['Account Code Description'], 'month':m+1, 'value':row[month], 'year':2023}, index=[0])
        budget_cofe_mod = pd.concat([budget_cofe_mod, record]).reset_index(drop=True)
