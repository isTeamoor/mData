from . import kpi_reqs


def draw_report():
    report = {}
    report['requisitions'] = kpi_reqs.reqs_report()
    return report