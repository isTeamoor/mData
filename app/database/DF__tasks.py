from .impo import tasks, taskStatus
from .DF__wo import wo

tasks.loc[tasks['Work Order Task Description'].isna(), 'Work Order Task Description'] = 'no name'

tasks  = tasks.merge(wo,         on='Work Order ID',      how='outer')
tasks  = tasks.merge(taskStatus, on='Work Order Task ID', how='left')


tasks = tasks.loc[~(tasks['Work Order Number'].isna())]

tasks.fillna({
    'Work Order Task Description':'not assigned', 
}, inplace=True)

tasks = tasks[[
'Work Order Number','Work Order Status Description',
'Work Order Task Description', 'Is Completed', 'Completed Date Time',
'Asset Description', 'Asset Number',
'raisedYear', 'raisedMonth','closedYear','closedMonth',
'Short Department Name', 'isMaintenance', 'isRMPD', 'Discipline',
'Department Description','Created By','Work Order Description'
]]
