
from .base import *



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SmartCare',
        'USER': 'root_arthur',
        'PASSWORD': 'arthur_root',
        'HOST': '127.0.0.1',  # or the hostname where MySQL is running
        'PORT': '3306',  # MySQL default port
    }
}
