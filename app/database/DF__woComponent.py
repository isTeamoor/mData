from .impo import woComponent, jobCodes, accountCodes

woComponent = woComponent.merge(jobCodes,     how='left', on='Job Code Major ID')
woComponent = woComponent.merge(accountCodes, how='left', on='Account Code ID')


woComponent.rename(columns={'Account Code Name': 'Account Code'}, inplace=True)
woComponent['Account Code'] = woComponent['Account Code'].astype('str')
woComponent.loc[woComponent['Account Code']=='nan', ['Account Code', 'Account Code Description']] = 'undefined'


woComponent = woComponent[['Work Order Component ID', 'Work Order Component Description', 'Job Code Major Description', 'Account Code', 'Account Code Description']]
