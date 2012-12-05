from haystack import indexes
from haystack import site
from swingtime.models import Event
from cms.models.pluginmodel import CMSPlugin
from django.utils.encoding import force_unicode
import re

def _strip_tags(value):
    """
    Returns the given HTML with all tags stripped.

    This is a copy of django.utils.html.strip_tags, except that it adds some
    whitespace in between replaced tags to make sure words are not erroneously
    concatenated.
    """
    return re.sub(r'<[^>]*?>', ' ', force_unicode(value))

class EventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(stored=True, indexed=False, model_attr='get_absolute_url')
    title = indexes.CharField(stored=True, indexed=False, model_attr='title')

    def get_model(self):
        return Event

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published=True)

    def prepare_text(self, obj):
        description_plugins = CMSPlugin.objects.filter(placeholder=obj.description)
        text = u''.join(self.prepared_data['text'])
        plugins = list(description_plugins)
        for base_plugin in plugins:
            instance, plugin_type = base_plugin.get_plugin_instance()
            if instance is None:
                # this is an empty plugin
                continue
            if hasattr(instance, 'search_fields'):
                text += u' '.join(force_unicode(_strip_tags(getattr(instance, field, ''))) for field in instance.search_fields)
            if getattr(instance, 'search_fulltext', False) or getattr(plugin_type, 'search_fulltext', False):
                text += _strip_tags(instance.render_plugin(context=RequestContext(request))) + u' '
        return text



site.register(Event, EventIndex)
