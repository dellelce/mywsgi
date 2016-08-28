# 
# vim:syntax=python
#

import os,sys,site,json
from stat import S_ISDIR
import os.path as p
import string
import random

class localconf(object):

 def __init__(self, name="env.json"):
  localpath = p.dirname(p.realpath(__file__))
  localdir = p.dirname(localpath)
  sys.path.append(localdir)
  sys.path.append(localpath)
  os.chdir(localpath)

  f = open(name)

  j = json.load(f)

  self.name = j["name"]
  self.settings = j["settings"]
  self.env = j["env"]

 def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

 ##
 def application(self):
  '''return a WSGI application'''

  # let's use a castom DJNGO_SETTINGS_MODULE for every environment
  self.id=self.id_generator()
  self.envvar = "DJANGO_SETTINGS_MODULE_" + self.id

  mode = os.stat(self.env).st_mode

  if (S_ISDIR(mode)):
   site.addsitedir(self.env)

  settings = self.settings

  # this to be done only after environment is setup correctly
  from django.core.wsgi import get_wsgi_application
  from django import conf as conf
  
  conf.ENVIRONMENT_VARIABLE = self.envvar # used by django/conf/__init__.py
  os.environ.setdefault(self.envvar, settings)
  application = get_wsgi_application()

  return application


# "main"
conf = localconf()
application = conf.application()

## EOF ##
