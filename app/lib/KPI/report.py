import xlsxwriter
from . import kpi_reqs
from . import payments
from ...database import DF__budget


def draw_report():
    payments.summaryData('outsource')
    payments.detailedData('outsource')

    """
    report['requisitions'] = kpi_reqs.reqs_report()
    kpi_reqs.reqs_toExcel()
    """