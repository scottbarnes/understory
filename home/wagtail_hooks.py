""" understory/home/wagtail_hooks.py """

from django.conf.urls import url
from django.urls import reverse

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.core import hooks

from .views import UnpublishedChangesReportView

@hooks.register('register_reports_menu_item')
def register_unpublished_changes_report_menu_item():
    return AdminOnlyMenuItem('Pages with unpublished changes', reverse(
        'unpublished_changes_report'), classnames='icon icon-' + UnpublishedChangesReportView.header_icon, order=700)

@hooks.register('register_admin_urls')
def register_unpublished_changes_report_url():
    return [
        url(r'^reports/unpublished-changes/$', UnpublishedChangesReportView.as_view(),
            name='unpublished_changes_report'),
    ]

