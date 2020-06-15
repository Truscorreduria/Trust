import json
from django.db.models import Model
import datetime
import decimal
from django.db.models.fields.files import ImageFieldFile, FileField, FieldFile


class Codec(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.time):
            return obj.strftime('H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, FieldFile):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, FileField):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, Model):
            try:
                return str(obj)
            except:
                return 'null'
        elif obj is None:
            return 'null'
        else:
            return json.JSONEncoder.default(self, obj)
