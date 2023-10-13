from handlers import common
from src import DF__wo

woDF = DF__wo.wo



def workOrders(filter=[]):
    df = common.filterDF(woDF, filter)

    statusDF, lists = common.groupDF(df, ['raisedYear', 'raisedMonth', 'Work Order Status Description'], 'count')
    yearsLst  = lists[0]
    statusLst = lists[2]

    byStatus = common.createObj(yearsLst, ['raised', 'notClosed', *statusLst])

    for year in yearsLst:
        for month in range(1,13):
            dataChunk = common.filterDF(statusDF, [{'field':'raisedYear', 'value':year, 'math':'=='}, '&', {'field':'raisedMonth', 'value':month, 'math':'=='} ])[['Work Order Status Description', 'Work Order Number']]
            if dataChunk.size == 0:
                continue
            byStatus['raised']['monthly'][year][month] = int(dataChunk['Work Order Number'].sum().item())
            byStatus['raised']['cumulat'][year][month] = int((byStatus['raised']['monthly'][year][month]) + (byStatus['raised']['cumulat'][year][month-1] if month>1 else 0))      
            byStatus['notClosed']['monthly'][year][month] = int(dataChunk.loc[ (dataChunk['Work Order Status Description'] != 'Closed') & (dataChunk['Work Order Status Description'] != 'Cancelled'), 'Work Order Number'].sum().item())
            byStatus['notClosed']['cumulat'][year][month] = int((byStatus['notClosed']['monthly'][year][month]) + (byStatus['notClosed']['cumulat'][year][month-1] if month>1 else 0))

            for row in dataChunk.index:
                statusName = dataChunk.loc[  row, 'Work Order Status Description' ]
                woCount    = dataChunk.loc[  row, 'Work Order Number' ]
                byStatus[statusName]['monthly'][year][month]    = int(woCount)
                byStatus[statusName]['cumulat'][year][month] = (byStatus[statusName]['monthly'][year][month]) + (byStatus[statusName]['cumulat'][year][month-1] if month>1 else 0)

    output = {}
    output['byStatus'] = byStatus
    #common.writeJSON(output, 'info')
    return output
    

 