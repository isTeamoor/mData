from . import kpi_reqs
from . import payments


def draw_report():
    report = {}
    report['requisitions'] = kpi_reqs.reqs_report()
    kpi_reqs.reqs_toExcel()
    return report

def test():
    payments.departmentPayments('outsource')