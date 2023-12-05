import pandas as pd

budget       = pd.read_excel("app/database/csv/budget.xlsx")

wo           = pd.read_csv("app/database/csv/ccc_wo_wo.csv",           encoding="utf-8")
priority     = pd.read_csv("app/database/csv/ccc_wo_priority.csv",     encoding="utf-8")
departments  = pd.read_csv("app/database/csv/ccc_wo_departments.csv",  encoding="utf-8")
status       = pd.read_csv("app/database/csv/ccc_wo_status.csv",       encoding="utf-8")
jobType      = pd.read_csv("app/database/csv/ccc_wo_jobType.csv",      encoding="utf-8")
isMasterWO   = pd.read_csv("app/database/csv/ccc_wo_isMasterWO.csv",   encoding="utf-8")
closedDates  = pd.read_csv("app/database/csv/ccc_wo_closedDates.csv",  encoding="utf-8")


spares           = pd.read_csv("app/database/csv/ccc_sp_spares.csv",           encoding="utf-8")
reservations     = pd.read_csv("app/database/csv/ccc_sp_reservations.csv",     encoding="utf-8")
customFields     = pd.read_csv("app/database/csv/ccc_sp_customFields.csv",     encoding="utf-8")
transactions     = pd.read_csv('app/database/csv/ccc_sp_transactions.csv',     encoding="utf-8")
catalogueInfo    = pd.read_csv('app/database/csv/ccc_sp_catalogueInfo.csv',    encoding="utf-8")
assetIDcatalogID = pd.read_csv('app/database/csv/ccc_sp_assetIDcatalogID.csv', encoding="utf-8")
stockOnHand      = pd.read_csv('app/database/csv/ccc_sp_stockOnHand.csv',      encoding="utf-8")
stockReserved    = pd.read_csv('app/database/csv/ccc_sp_stockReserved.csv',    encoding="utf-8")


trades       = pd.read_csv("app/database/csv/ccc_tr_trades.csv",      encoding="utf-8")
tradeCodes   = pd.read_csv("app/database/csv/ccc_tr_tradeCodes.csv",  encoding="utf-8")


contactID    = pd.read_csv("app/database/csv/ccc_cm_contactID.csv",    encoding="utf-8")
assets       = pd.read_csv("app/database/csv/ccc_cm_assets.csv",       encoding="utf-8")
accountCodes = pd.read_csv("app/database/csv/ccc_cm_accountCodes.csv", encoding="utf-8")
uom          = pd.read_csv("app/database/csv/ccc_cm_uom.csv",          encoding="utf-8")
woComponent  = pd.read_csv("app/database/csv/ccc_cm_woComponent.csv",  encoding="utf-8")
jobCodes     = pd.read_csv("app/database/csv/ccc_cm_jobCodes.csv",     encoding="utf-8")




contactID.insert(1, 'Reserved By',      contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Created By',       contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Requisitioned By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Completed By',     contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Cancelled By',     contactID['First Name'] + " " + contactID['Last Name'])