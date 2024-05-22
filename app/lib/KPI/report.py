from . import payments


def draw_report():
    payments.sumPayments(payments.getPayments(),'rmpd')
    #payments.summaryData('outsource')
    #payments.detailedData('outsource')

    """
    report['requisitions'] = kpi_reqs.reqs_report()
    kpi_reqs.reqs_toExcel()
    """