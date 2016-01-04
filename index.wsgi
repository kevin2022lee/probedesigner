import sys
import os.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'OligoDesigner.settings' 
sys.path.append(os.path.join(os.path.dirname(__file__), 'OligoDesigner'))


import sae
import django.core.handlers.wsgi

application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler())