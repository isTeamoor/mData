from calculations import calculations, months


slides = {}
slides['planMonthly'] = ['planMonthly',]
slides['planCumulative'] = ['planCumulative',]
slides['actualMonthly'] = ['actualMonthly',]
slides['actualCumulative'] = ['actualCumulative',]
slides['forecast'] = ['forecast',] 

for month in months:
    slides['planMonthly'].append(calculations['budget']['sum'][month])
    slides['planCumulative'].append(calculations['budget']['sumCum'][month])

    valSpare = calculations['spares']['actual']['sum'][month]
    valTrade = calculations['trades']['actual']['sum'][month]
    slides['actualMonthly'].append( valSpare + valTrade )

    valSpareCum = calculations['spares']['actual']['sumCum'][month]
    valTradeCum = calculations['trades']['actual']['sumCum'][month]
    slides['actualCumulative'].append( valSpareCum + valTradeCum )
slides['forecast'].append( calculations['spares']['forecast']['sum'] + calculations['trades']['forecast']['sum'] )

print(slides['planMonthly'])
print(slides['actualMonthly'])
print(slides['planCumulative'])
print(slides['actualCumulative'])
print(slides['forecast'])






slides['cumWithDisc'] = {}
for department in calculations['groups']['Department Name'].keys():
    if calculations['groups']['Department Name'][department]['spares']['actual']['sumCum']['Dec'] == 0 and calculations['groups']['Department Name'][department]['trades']['actual']['sumCum']['Dec'] == 0:
        continue
    slides['cumWithDisc'][department] = calculations['groups']['Department Name'][department]['spares']['actual']['sumCum']['Dec'] + calculations['groups']['Department Name'][department]['trades']['actual']['sumCum']['Dec']

for department in calculations['groups']['Short Department Name'].keys():
    if calculations['groups']['Short Department Name'][department]['spares']['actual']['sumCum']['Dec'] == 0 and calculations['groups']['Short Department Name'][department]['trades']['actual']['sumCum']['Dec'] == 0:
        continue
    if department.startswith(('SLU', 'SGU', 'PWU', 'U&O')):
        slides['cumWithDisc'][department] = calculations['groups']['Short Department Name'][department]['spares']['actual']['sumCum']['Dec'] + calculations['groups']['Short Department Name'][department]['trades']['actual']['sumCum']['Dec']


for department in slides['cumWithDisc'].keys():
    print (department, ',', slides['cumWithDisc'][department])





slides['monthlyTeams'] = {}
for team in ['SLU', 'SGU', 'PWU', 'U&O']:
    slides['monthlyTeams'][team] = {}
    for discipline in calculations['groups']['Department Name'].keys():
        if not discipline.startswith(team):
            continue
        slides['monthlyTeams'][team][discipline] = {}
        for month in months:
            val = calculations['groups']['Department Name'][discipline]['spares']['actual']['sum'][month] + calculations['groups']['Department Name'][discipline]['trades']['actual']['sum'][month]
            slides['monthlyTeams'][team][discipline][month] = val
        

for team in slides['monthlyTeams'].keys():
    print(team)
    for disc in slides['monthlyTeams'][team]:
        values = [disc, ]   
        for month in months:
            values.append(slides['monthlyTeams'][team][disc][month])
        values.append(calculations['groups']['Department Name'][disc]['spares']['forecast']['sum'])
        print(values)
    print('\n')