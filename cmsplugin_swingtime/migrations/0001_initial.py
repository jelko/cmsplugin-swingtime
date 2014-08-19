# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('cmsplugin_swingtime_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('where', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_description', null=True, to=orm['cms.Placeholder'])),
            ('uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('cmsplugin_swingtime', ['Event'])

        # Adding model 'Occurrence'
        db.create_table('cmsplugin_swingtime_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsplugin_swingtime.Event'])),
            ('hide_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cmsplugin_swingtime', ['Occurrence'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('cmsplugin_swingtime_event')

        # Deleting model 'Occurrence'
        db.delete_table('cmsplugin_swingtime_occurrence')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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