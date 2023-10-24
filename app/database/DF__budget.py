from .impo import budget
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

budget['Account Code'] = budget['Account Code'].astype('str')

for month in months:
    budget[month] = budget[month].fillna(0)

