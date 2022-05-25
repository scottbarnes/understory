from django.utils.safestring import mark_safe

from wagtail.admin.ui.components import Component
from wagtail.core import hooks
from wagtail.core.models import Page

from article.models import ArticlePage


class WelcomePanel(Component):
    order = 50

    def render_html(self, parent_context):
        return mark_safe("""
        <section class="panel summary nice-padding">
          <h3>No, but seriously -- welcome to the admin homepage.</h3>
        </section>
        """)

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(WelcomePanel())


# @hooks.register('before_edit_page')
# def before_edit_page(request, page):

#     qs = page.translations.all()
#     if qs:
#         for q in qs:


    # page.test_field = "updated from hook again"
    # page.blob = Page.objects.get(id=40)
    # page.save()

from wagtail.admin import widgets as wagtailadmin_widgets

@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False, next_url=None):
    yield wagtailadmin_widgets.PageListingButton(
        'A page listing button',
        '/goes/to/a/url/',
        priority=10
    )


from wagtail.admin import widgets as wagtailadmin_widgets

@hooks.register('register_page_header_buttons')
def page_header_buttons(page, page_perms, next_url=None):
    yield wagtailadmin_widgets.Button(
        'A dropdown button',
        '/goes/to/a/url/',
        priority=60
    )

from django.urls import reverse

from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
  return MenuItem('Frank', 'frank', icon_name='folder-inverse', order=10000)


# from django.utils.html import format_html_join
# from django.utils.safestring import mark_safe
# from django.templatetags.static import static

# @hooks.register('insert_editor_js')
# def editor_js():
#     js_files = [
#         'js/fireworks.js', # https://fireworks.js.org
#     ]
#     js_includes = format_html_join('\n', '<script src="{0}"></script>',
#         ((static(filename),) for filename in js_files)
#     )
#     return js_includes + mark_safe(
#         """
#         <script>
#             window.addEventListener('DOMContentLoaded', (event) => {
#                 var container = document.createElement('div');
#                 container.style.cssText = 'position: fixed; width: 100%; height: 100%; z-index: 100; top: 0; left: 0; pointer-events: none;';
#                 container.id = 'fireworks';
#                 document.getElementById('main').prepend(container);
#                 var options = { "acceleration": 1.2, "autoresize": true, "mouse": { "click": true, "max": 3 } };
#                 var fireworks = new Fireworks(document.getElementById('fireworks'), options);
#                 fireworks.start();
#             });
#         </script>
#         """
#     )


@hooks.register('construct_explorer_page_queryset')
def show_my_profile_only(parent_page, pages, request):
    # print(f"We are inside: {parent_page}")
    # print(vars(parent_page))

    if not hasattr(parent_page, 'language') or not parent_page.translations.all():
        print(f"The QS is as follows: \n {pages}")
        print("BAILING OUT")
        return pages

    if parent_page.specific.slug == 'stories':
        print(f"stories QS is\n {pages}")

    if parent_page.language == "English" and isinstance(parent_page, ArticlePage):
        print(f"{parent_page.title} has triggered the QS mod")
        pages = parent_page.translations.all()
        print(f"QS is: \n{pages}")
        return pages

    # if parent_page.specific.slug == 'stories':
    # print(vars(parent_page))
    # print(pages)
        # pages = pages.filter(owner=request.user)
        # pages = pages.filter(id=43)

    return pages


