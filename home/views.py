"""
understory/views.py

Home of the various custom reports.
"""

from wagtail.admin.views.reports import PageReportView
from wagtail.core.models import Page


class UnpublishedChangesReportView(PageReportView):
    """ Show all pages with unpublished changes. """

    header_icon = 'doc-empty-invorse'
    template_name = 'reports/unpublished_changes_report.html'
    title = 'Pages with unpublished changes'

    list_export = PageReportView.list_export + ['last_published_at']
    export_headings = dict(last_published_at='Last published', **PageReportView.export_headings)

    def get_queryset(self):
        return Page.objects.filter(has_unpublished_changes=True)
