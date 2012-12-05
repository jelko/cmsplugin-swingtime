from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from swingtime.menu import SwingtimeMenu

class SwingtimeApp(CMSApp):
        name = _("Events")
        urls = ["swingtime.urls"]
        menus = [SwingtimeMenu]

apphook_pool.register(SwingtimeApp)
