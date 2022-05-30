""" understory/home/wagtail_hooks.py """

from django.urls import re_path, reverse

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

from wagtail.models import Page

from .views import UnpublishedChangesReportView

@hooks.register('register_reports_menu_item')
def register_unpublished_changes_report_menu_item():
    return AdminOnlyMenuItem('Pages with unpublished changes', reverse(
        'unpublished_changes_report'), classnames='icon icon-' + UnpublishedChangesReportView.header_icon, order=700)

@hooks.register('register_admin_urls')
def register_unpublished_changes_report_url():
    return [
        re_path(r'^reports/unpublished-changes/$', UnpublishedChangesReportView.as_view(),
                name='unpublished_changes_report'),
    ]

# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `redact` feature, which a custom inline style type,
    and is stored as HTML with a `<span>` tag and some styling.
    """
    feature_name = 'redact'
    type_ = 'REDACT'
    tag = 'span'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'Redact',
        'description': 'Quasi-redact',
        'style': {'backgroundColor': 'currentcolor'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format':{
            'style_map': {
                type_: {
                    "element": tag,
                    "props": {
                        # instead of defining a class, define the style.
                        "style": {'backgroundColor': 'currentcolor'}
                    }
                }
            }
        }
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('redact')

@hooks.register('construct_explorer_page_queryset')
def add_translations_to_children_queryset(parent_page, pages, request):
    """
    When viewing individual Stories, FiveQuestions, and Invitations in the
    explorer, create a union Create a union between items with children and
    those with translations.
    """

    # Only do this for explorer QuerySets that have translations.
    if not hasattr(parent_page, 'translations'):
        return pages

    # The 'page' QuerySet is of type: <PageQuerySet [<Page: title >]. But an
    # An ArticlePage QS returns a PageQuerySet with [<ArticlePage: title>].
    # Because Page and ArticlePage are different base models, QuerySet
    # union isn't possible. The query+filter below returns a QS based on the
    # Page model, so union is possible.
    # Specifically, filter by id on Pages that have IDs in this parent_page's
    # translations.values.
    children = pages
    translations = Page.objects.filter(id__in=parent_page.translations.values('id'))
    return children | translations
