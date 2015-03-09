# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'app_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jifang', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('jigui', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'app', ['Room'])

        # Adding model 'Switch'
        db.create_table(u'app_switch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(unique=True, max_length=15)),
            ('device', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('devices', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('port', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('paihao', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('idroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Room'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal(u'app', ['Switch'])

        # Adding model 'Mac'
        db.create_table(u'app_mac', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eth0', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('eth1', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('eth2', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('eth3', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('qcode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('cpu', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('mem', self.gf('django.db.models.fields.CharField')(default=0, max_length=30)),
            ('disk', self.gf('django.db.models.fields.CharField')(default=0, max_length=30)),
            ('uname', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('paihao', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('idroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Room'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal(u'app', ['Mac'])

        # Adding model 'Server'
        db.create_table(u'app_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(unique=True, max_length=15)),
            ('device', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('devices', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('mouth', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('fuwu', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ports', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('configid', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('whoandyou', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('youandwho', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_avlie', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('idroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Room'], on_delete=models.PROTECT)),
            ('idmac', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Mac__paihao', on_delete=models.PROTECT, to=orm['app.Mac'])),
            ('idswitch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Switch'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal(u'app', ['Server'])

        # Adding model 'Repair'
        db.create_table(u'app_repair', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repair', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('idmac', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Mac'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal(u'app', ['Repair'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'app_room')

        # Deleting model 'Switch'
        db.delete_table(u'app_switch')

        # Deleting model 'Mac'
        db.delete_table(u'app_mac')

        # Deleting model 'Server'
        db.delete_table(u'app_server')

        # Deleting model 'Repair'
        db.delete_table(u'app_repair')


    models = {
        u'app.mac': {
            'Meta': {'object_name': 'Mac'},
            'cpu': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'disk': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30'}),
            'eth0': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'eth1': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'eth2': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'eth3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idroom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Room']", 'on_delete': 'models.PROTECT'}),
            'mem': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30'}),
            'paihao': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'qcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'uname': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'})
        },
        u'app.repair': {
            'Meta': {'object_name': 'Repair'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idmac': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Mac']", 'on_delete': 'models.PROTECT'}),
            'repair': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        u'app.room': {
            'Meta': {'object_name': 'Room'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jifang': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'jigui': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'app.server': {
            'Meta': {'object_name': 'Server'},
            'configid': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'device': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'devices': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'fuwu': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idmac': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Mac__paihao'", 'on_delete': 'models.PROTECT', 'to': u"orm['app.Mac']"}),
            'idroom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Room']", 'on_delete': 'models.PROTECT'}),
            'idswitch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Switch']", 'on_delete': 'models.PROTECT'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'is_avlie': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'mouth': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'ports': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'whoandyou': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'youandwho': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'app.switch': {
            'Meta': {'object_name': 'Switch'},
            'device': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'devices': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idroom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Room']", 'on_delete': 'models.PROTECT'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'paihao': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'port': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['app']