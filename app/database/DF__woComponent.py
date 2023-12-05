from .impo import woComponent, jobCodes, accountCodes

woComponent = woComponent.merge(jobCodes,     how='left', on='Job Code Major ID')
woComponent = woComponent.merge(accountCodes, how='left', on='Account Code ID')


woComponent.rename(columns={'Account Code Name': 'Account Code'}, inplace=True)


woComponent = woComponent[['Work Order Component ID', 'Work Order Component Description', 'Job Code Major Description', 'Account Code', 'Account Code Description']]