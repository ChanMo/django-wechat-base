import os
import sys
import hashlib
import urllib
#import urllib2 #python2.7
import json
import time
import datetime
import random
import string
import collections

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings

import xmltodict #pip install xmltodict
