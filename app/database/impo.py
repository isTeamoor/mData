import pandas as pd


budget       = pd.read_excel("app/database/csv/budget.xlsx")
wo           = pd.read_csv("app/database/csv/ccc_r_workOrders.csv",           encoding="utf-8")
isGrouppedWO = pd.read_csv('app/database/csv/ccc_r_groupped_workOrders.csv',  encoding='utf-8')
spares       = pd.read_csv("app/database/csv/ccc_r_workOrdersSpare.csv",      encoding="utf-8")
reservations = pd.read_csv("app/database/csv/ccc_r_reservations.csv",         encoding="utf-8")
trades       = pd.read_csv("app/database/csv/ccc_r_workOrdersTrade.csv",      encoding="utf-8")
contactID    = pd.read_csv("app/database/csv/ccc_m_ContactID.csv",            encoding="utf-8")[['Contact ID', 'First Name', 'Last Name']]
assets       = pd.read_csv("app/database/csv/ccc_m_assets.csv",               encoding="utf-8")
transactions = pd.read_csv('app/database/csv/ccc_wh_transactions.csv',        encoding="utf-8")







contactID.insert(1, 'Reserved By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Created By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Requisitioned By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Completed By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Cancelled By', contactID['First Name'] + " " + contactID['Last Name'])