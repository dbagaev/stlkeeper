import os
import sys

# sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'stlkeeper.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/home/devil/Projects/part-modeller/stlkeeper'
if path not in sys.path:
    sys.path.append(path)


