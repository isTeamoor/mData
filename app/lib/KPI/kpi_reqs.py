from ..Analysis.hub import getVal

def reqs_finished():
    return getVal('rq_raised_monthly')




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
    return report