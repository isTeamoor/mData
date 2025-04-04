from .impo import assets



# Есть assets в БД, у которых relationships зациклен
errorIDs = [111171, 111173, 111172, 117487,	117468,	117490,	117470,	117640,	118436,	118437, 122320,	122319,
            122371,	122514,	122515,	122516,	122372, 122324,	122323,	122367,	122445,	122520,	122522,	122368]
assets = assets.loc[ ~assets['Asset ID'].isin(errorIDs) ]




### 1. Объект, показывающий наследников каждого asset
AssetsRelationships = {}
#################################Exception#########################
assets.loc [ assets['Asset ID']==234549, 'Parent Asset ID' ] = 77405
assets.loc [ assets['Asset ID']==227351, 'Parent Asset ID' ] = 77405
assets.loc [ assets['Asset ID']==222192, 'Parent Asset ID' ] = 77405
####################################################################
for row in assets.index:
    parent      = int(assets.loc[row,"Parent Asset ID"])
    asset       = int(assets.loc[row,"Asset ID"])
    description = assets.loc[row,"Asset Description"]
    assetNumber = assets.loc[row,"Asset Number"]
    if parent not in AssetsRelationships:
        AssetsRelationships[parent] = {}
    AssetsRelationships[parent][asset] = {'description': description,'assetNumber': assetNumber}



### 2. Показать все объекты, относящиеся к SGU
def unitChildren():
    SGU = 77437
    assetNumberlist = ['SGU','UzGTL AP','Air Products']

    def goThroughTree(assetID):
        subList = []
        for child in AssetsRelationships[assetID].keys():
            childAssetNumber = AssetsRelationships[assetID][child]['assetNumber']
            subList.append(childAssetNumber)
            if child in AssetsRelationships:
                subList.extend(goThroughTree(child))
        return subList

    assetNumberlist.extend(goThroughTree(SGU))
    return assetNumberlist




def checkRelationships(source):
    for item in source.index:
        flag = 0
        for parent in AssetsRelationships:
            if flag == 1:
                continue
            if item in AssetsRelationships[parent]:
                flag = 1
        if flag == 0:
            print(source.loc[item])




def rooting (parent, assetID, source, valueName):
    output = {}
    value = 0
    
    # Если нет WOC и нет наследников - вернуть пустой объект и count = 0
    if ((assetID not in source.index) and (assetID not in AssetsRelationships)):
        return output, value
        
    #Если есть WOC, то value увеличивается
    if assetID in source.index:
        value = source.loc[ assetID ].item()


    #Для каждого из наследников
    for key in AssetsRelationships[assetID]:
        #Если у наследника нет своих наследников
        if key not in AssetsRelationships:
            #Но если у наследника есть value
            if key in source.index:
                output[key] = {}
                output[key][valueName] = source.loc[ key ].item()
                output[key]['description'] = AssetsRelationships[assetID][key]['description']
                output[key]['assetNumber'] = AssetsRelationships[assetID][key]['assetNumber']
                value += output[key][valueName]
        #Если у наследника есть свои наследники
        else:
            (returnedObj, returnedvalue) = rooting(assetID, key, source, valueName)
            if returnedObj:
                value += returnedvalue
                output[key] = returnedObj
    if value>0:
        output['description'] = AssetsRelationships[parent][assetID]['description']
        output['assetNumber'] = AssetsRelationships[parent][assetID]['assetNumber']
        output[valueName]     = value
        
    return output, value


def byAssets(source, valueName):
    source = source[source != 0]
    output = {}
    output = rooting(0, 77405, source, valueName)[0]
    return output