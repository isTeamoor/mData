import pandas as pd


budget       = pd.read_excel("app/database/csv/budget.xlsx")
wo           = pd.read_csv("app/database/csv/ccc_r_workOrders.csv",             encoding="utf-8")
spares       = pd.read_csv("app/database/csv/ccc_r_workOrdersSpare.csv",        encoding="utf-8")[['Work Order Spare Description', 'Estimated Quantity', 'Estimated Unit Cost', 'Actual Quantity', 'UOMID', 'Work Order Spare ID', 'Work Order ID', 'Work Order Component ID',]]
trades       = pd.read_csv("app/database/csv/ccc_r_workOrdersTrade.csv",        encoding="utf-8")[['Trade Code ID', 'Estimated Duration Hours', 'Actual Duration Hours', 'Hourly Rate', 'Work Order Trade ID', 'Work Order ID', 'Work Order Component ID',]]
reservations = pd.read_csv("app/database/csv/ccc_r_reservations.csv",           encoding="utf-8")
pm           = pd.read_csv("app/database/csv/ccc_m_pm.csv",                     encoding="utf-8")[['Preventative Maintenance ID', 'Preventative Maintenance Number', 'Preventative Maintenance Description' ]]
woComponent  = pd.read_csv("app/database/csv/ccc_r_workOrdersComponent.csv",    encoding="utf-8")[['Work Order Component Description', 'Account Code ID', 'Work Order Component ID', 'Job Code Major ID',]]
accountCodes = pd.read_csv("app/database/csv/ccc_m_accountCodes.csv",           encoding="utf-8")[['Account Code ID', 'Account Code Name', 'Account Code Description']]
jobCodes     = pd.read_csv("app/database/csv/ccc_m_JobCodes.csv",               encoding="utf-8")[['Job Code Major ID', 'Job Code Major Description']]
uom          = pd.read_csv("app/database/csv/ccc_m_UOM.csv",                    encoding="utf-8")[['UOMID', 'UOMDescription']]
woStatus     = pd.read_csv("app/database/csv/ccc_m_workOrdersStatusID.csv",     encoding="utf-8")[['Work Order Status ID', 'Work Order Status Description']]
contactID    = pd.read_csv("app/database/csv/ccc_m_ContactID.csv",              encoding="utf-8")[['Contact ID', 'First Name', 'Last Name']]
priorityID   = pd.read_csv("app/database/csv/ccc_m_priorityID.csv",             encoding="utf-8")[['Priority ID', 'Priority Description']]
departament  = pd.read_csv("app/database/csv/ccc_m_departaments.csv",           encoding="utf-8")[['Department ID', 'Department Name', 'Department Description']]
jobType      = pd.read_csv("app/database/csv/ccc_m_jobTypes.csv",               encoding="utf-8")[['Job Type ID', 'Job Type Description']]
tradeID      = pd.read_csv("app/database/csv/ccc_m_tradeID.csv",                encoding="utf-8")[['Trade Code ID', 'Trade Code Description', 'Trade Code Name']]
assets       = pd.read_csv("app/database/csv/ccc_m_assets.csv",                 encoding="utf-8")
transactions = pd.read_csv('app/database/csv/ccc_wh_transactions.csv',          encoding="utf-8")
catalogInfo  = pd.read_csv('app/database/csv/ccc_wh_catalogInfo.csv',           encoding='utf-8').rename(columns={'User Defined Text Box1': 'Material Code'})
requisitions = pd.read_csv('app/database/csv/ccc_m_requisitions.csv',           encoding='utf-8')[['Requisition ID', 'Requisition Number','Requisition Description','Requisitioned By Contact ID','Required By Date Time','Account Code ID', 'Comment', 'User Defined Text Box','Created By Contact ID', 'Raised Date Time', 'Approval Path ID']]
requisitItems= pd.read_csv('app/database/csv/ccc_m_requisitionItems.csv',       encoding='utf-8')[['Requisition ID', 'Asset ID','Requisition Line Description','Requisitioned Quantity', 'UOMID','Work Order Spare ID', 'Expected Purchase Price', 'Completed Date Time','Completed By Contact ID', 'Cancelled By Contact ID', 'Cancelled Date Time',]]
approvalPath = pd.read_csv('app/database/csv/ccc_m_approvalPath.csv',           encoding='utf-8')[['Approval Path ID', 'Approval Path Name']]
isGrouppedWO = pd.read_csv('app/database/csv/ccc_r_groupped_workOrders.csv',    encoding='utf-8')
customFieldSpares = pd.read_csv('app/database/csv/ccc_r_customFieldSpares.csv', encoding='utf-8')



woNumbers = wo[['Work Order ID', 'Work Order Number']].copy()
woNumbers.rename(columns={'Work Order Number':'Group WO number'}, inplace=True)


contactID.insert(1, 'Reserved By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Created By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Requisitioned By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Completed By', contactID['First Name'] + " " + contactID['Last Name'])
contactID.insert(1, 'Cancelled By', contactID['First Name'] + " " + contactID['Last Name'])



isGrouppedWO['Is Group Work Order'] = 'yes'

