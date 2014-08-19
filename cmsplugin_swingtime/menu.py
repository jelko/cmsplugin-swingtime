from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from models import EventType

class SwingtimeMenu(CMSAttachMenu):
    name = _("Events Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        nodes = []
        for type in EventType.objects.all():
            # the menu tree consists of NavigationNode instances
            # Each NavigationNode takes a label as first argument, a URL as
            # second argument and a (for this tree) unique id as third
            # argument.
            node = NavigationNode(
                type.label,
                reverse('swingtime-type-index', kwargs={'event_type':type.abbr}),
                type.pk
            )
            nodes.append(node)
        try:
            nodes.append(NavigationNode(
                _("Archiv"),
                reverse("swingtime-archive"),
                None
            ))
        except:
            pass
        return nodes

menu_pool.register_menu(SwingtimeMenu) # register the menu.
