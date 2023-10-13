from .impo import budget
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

budget['Account Code'] = budget['Account Code'].astype('str')

def monthly():
    output = []
    for i in range(0,12):
        output.append({i:budget[ months[i] ].sum()})
    return output

def cumulat():
    output = []
    sum = 0
    for i in range(0,12):
        sum += budget[ months[i] ].sum()
        output.append({i:sum})
    return output


def Budget(budget):
    output = {}
    output['sum'] = {}
    output['sumCum'] = {}
    output['aCodes'] = {}
    output['aCodesCum'] = {}

    summary = 0
    for month in months:
        val = budget[month].sum()
        output['sum'][month] = val

        summary += val
        output['sumCum'][month] = summary

        output['aCodes'][month] = {}
        output['aCodesCum'][month] = {}
        for row in budget.index:
            output['aCodes'][month][budget['Account Code Description'][row]] = budget[month][row]

            sum = 0
            for m in months:
                sum += budget[m][row]
                if m == month:
                    break
            output['aCodesCum'][month][budget['Account Code Description'][row]] = sum
    return output

