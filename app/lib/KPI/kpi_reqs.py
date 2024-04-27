import xlsxwriter
from ..Analysis.hub import getVal

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def reqs_report():
    report = {}

    report['raised'] = {}
    report['raised']['overall'] = {}
    report['raised']['overall']['monthly'] = getVal('rq_raised_monthly')['data']
    report['raised']['overall']['cumulative'] = getVal('rq_raised_monthly')['simple_solidCumulative']
    report['raised']['overall']['cumulat_yearly'] = getVal('rq_raised_monthly')['cumulative']
    report['raised']['by_ApprovPath'] = {}
    report['raised']['by_ApprovPath']['monthly'] = getVal('rq_raised_Departments_monthly')['data']
    report['raised']['by_ApprovPath']['cumulative'] = getVal('rq_raised_Departments_monthly')['solidCumulative']
    report['raised']['by_ApprovPath']['cumulat_yearly'] = getVal('rq_raised_Departments_monthly')['cumulative']

    report['required'] = {}
    report['required']['overall'] = {}
    report['required']['overall']['monthly'] = getVal('rq_required_monthly')['data']
    report['required']['overall']['cumulative'] = getVal('rq_required_monthly')['simple_solidCumulative']
    report['required']['overall']['cumulat_yearly'] = getVal('rq_required_monthly')['cumulative']
    report['required']['by_ApprovPath'] = {}
    report['required']['by_ApprovPath']['monthly'] = getVal('rq_required_Departments_monthly')['data']
    report['required']['by_ApprovPath']['cumulative'] = getVal('rq_required_Departments_monthly')['solidCumulative']
    report['required']['by_ApprovPath']['cumulat_yearly'] = getVal('rq_required_Departments_monthly')['cumulative']
    return report

def reqs_toExcel():
    source = reqs_report()

    workbook = xlsxwriter.Workbook('reqs.xlsx')
    worksheet = workbook.add_worksheet('1')
    
    col = 1
    for y in range(2022,2025):
        for m in range(1,13):
            if (y==2022 and m<9) or (y==2022 and m>9):
                continue
            worksheet.write(0,col,y)
            worksheet.write(1,col,months[m-1])

            worksheet.write(2,0,'raised')
            worksheet.write(2,col, source['raised']['overall']['monthly'][y][m] if y in source['raised']['overall']['monthly'] and m in source['raised']['overall']['monthly'][y] else 0)
            worksheet.write(3,0,'raised-cumulat')
            worksheet.write(3,col, source['raised']['overall']['cumulative'][y][m] if y in source['raised']['overall']['cumulative'] and m in source['raised']['overall']['cumulative'][y] else 0)
            worksheet.write(4,0,'required-cumulat')
            worksheet.write(4,col, source['required']['overall']['cumulative'][y][m] if y in source['required']['overall']['cumulative'] and m in source['required']['overall']['cumulative'][y] else 0)

            col += 1
    
    workbook.close()
