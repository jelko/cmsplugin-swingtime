# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventType'
        db.create_table('cmsplugin_swingtime_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbr', self.gf('django.db.models.fields.SlugField')(unique=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cmsplugin_swingtime', ['EventType'])

        # Adding field 'Event.event_type'
        db.add_column('cmsplugin_swingtime_event', 'event_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['cmsplugin_swingtime.EventType']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table('cmsplugin_swingtime_eventtype')

        # Deleting field 'Event.event_type'
        db.delete_column('cmsplugin_swingtime_event', 'event_type_id')


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmsplugin_swingtime.event': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Event'},
            'description': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_description'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmsplugin_swingtime.EventType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'cmsplugin_swingtime.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'abbr': ('django.db.models.fields.SlugField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cmsplugin_swingtime.occurrence': {
            'Meta': {'ordering': "('start_time', 'end_time')", 'object_name': 'Occurrence'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmsplugin_swingtime.Event']"}),
            'hide_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['cmsplugin_swingtime']