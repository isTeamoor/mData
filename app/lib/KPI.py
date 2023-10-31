from ..database.DF__spares import spares_RMPD
from ..database.DF__trades import trades_RMPD
from ..database.DF__wo import wo_RMPD

CofeTrades = ['INSULATE','Metrology Engineer','Workshop machinist junior','WELDER','Pipe Fitter','Scaffolder','F&G Supervisor','WELD ENG','Piping Engineer','JET TECH',
              'PSV Technician','Fire and Gas engineer','Work Shop machinist','SUPV PSV','PSV Junior Technician','HVAC Supervisor','VALVE Supervisor','Valve Engineer',
              'HVAC ENG','Field instrumentation Junior technician','Valve technician','PIPING JUNIOR','Insulation Coordinator','Metrology Supervisor','Workshop Supervisor CofE',]


def kpiRep():
    spares_RMPD[['Work Order Spare Description','Estimated Cost','Actual Cost','Estimated Quantity','Estimated Unit Cost','Actual Quantity',
                'UOMID','Work Order Spare ID','Work Order ID','Work Order Component ID','reservYear','reservMonth','Reservation Number',
                'Reserved By','raisedYear','raisedMonth','raisedDay','closedYear','closedMonth','closedDay','Work Order Number',
                'Work Order Description','Asset ID','Created By','Work Order Closed Contact ID','Work Order Status Description',
                'Priority Description','Department Name','Department Description','Job Type Description','Short Department Name','Discipline',
                'Work Order Component Description','Account Code ID','Job Code Major ID','Account Code','Account Code Description','Job Code Major Description','UOMDescription'
                ]].to_excel('spares_RMPD.xlsx')
    wo_RMPD[['raisedYear','raisedMonth','raisedDay','closedYear','closedMonth','closedDay','Work Order Number','Work Order Description',
            'Work Order ID','Asset ID','Created By','Work Order Closed Contact ID','Work Order Status Description','Priority Description',
            'Department Name','Department Description','Job Type Description','Short Department Name','Discipline']].to_excel('wo_RMPD.xlsx')
    trades_RMPD[['Trade Code ID','Estimated Cost','Actual Cost','Estimated Duration Hours','Actual Duration Hours','Hourly Rate',
                'Work Order Trade ID','Work Order ID','Work Order Component ID','raisedYear','raisedMonth','raisedDay','closedYear',
                'closedMonth','closedDay','Work Order Number','Work Order Description','Asset ID','Created By','Work Order Closed Contact ID',
                'Work Order Status Description','Priority Description','Department Name','Department Description','Job Type Description',
                'Short Department Name','Discipline','Trade Code Description','Work Order Component Description','Account Code ID',
                'Job Code Major ID','Account Code','Account Code Description','Job Code Major Description']].to_excel('trades_RMPD.xlsx')




'''
spares = DF__spares.spares
trades = DF__trades.trades
wo     = DF__wo.wo
CofeTrades = impo.CofeTrades


spares_CofE = spares.loc[ ((spares['Reserved By'] == 'Mirjakhon Toirov') | (spares['Reserved By'] == 'Bobur Aralov')) 
                         | (spares['Department Name'] == 'CofE') ]
trades_CofE = trades.loc [ trades['Trade Code Description'].isin(CofeTrades) ]
wo_CofE     = wo.loc [ (spares['Department Name'] == 'CofE') | (wo['Work Order Number'].isin(spares_CofE['Work Order Number'].unique())) 
                     | (wo['Work Order Number'].isin(trades_CofE['Work Order Number'].unique()))   ]

spares_CofE[['Work Order Spare Description','Estimated Cost','Actual Cost','Estimated Quantity','Estimated Unit Cost','Actual Quantity',
             'UOMID','Work Order Spare ID','Work Order ID','Work Order Component ID','reservYear','reservMonth','Reservation Number',
            'Reserved By','raisedYear','raisedMonth','raisedDay','closedYear','closedMonth','closedDay','Work Order Number',
            'Work Order Description','Asset ID','Created By','Work Order Closed Contact ID','Work Order Status Description',
            'Priority Description','Department Name','Department Description','Job Type Description','Short Department Name','Discipline',
            'Work Order Component Description','Account Code ID','Job Code Major ID','Account Code','Account Code Description','Job Code Major Description','UOMDescription'
            ]].to_excel('reports/KPI report/spares_CofE.xlsx')
wo_CofE[['raisedYear','raisedMonth','raisedDay','closedYear','closedMonth','closedDay','Work Order Number','Work Order Description',
         'Work Order ID','Asset ID','Created By','Work Order Closed Contact ID','Work Order Status Description','Priority Description',
         'Department Name','Department Description','Job Type Description','Short Department Name','Discipline']].to_excel('reports/KPI report/wo_CofE.xlsx')
trades_CofE[['Trade Code ID','Estimated Cost','Actual Cost','Estimated Duration Hours','Actual Duration Hours','Hourly Rate',
             'Work Order Trade ID','Work Order ID','Work Order Component ID','raisedYear','raisedMonth','raisedDay','closedYear',
             'closedMonth','closedDay','Work Order Number','Work Order Description','Asset ID','Created By','Work Order Closed Contact ID',
             'Work Order Status Description','Priority Description','Department Name','Department Description','Job Type Description',
             'Short Department Name','Discipline','Trade Code Description','Work Order Component Description','Account Code ID',
             'Job Code Major ID','Account Code','Account Code Description','Job Code Major Description']].to_excel('reports/KPI report/trades_CofE.xlsx')'''