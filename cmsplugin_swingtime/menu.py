from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

class SwingtimeMenu(CMSAttachMenu):
    name = _("Events Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        try:
            nodes = [NavigationNode(
                _("Archiv"),
                reverse("swingtime-archive"),
                1
            )]
            return nodes
        except:
            return []

menu_pool.register_menu(SwingtimeMenu) # register the menu.
