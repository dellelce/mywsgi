# 
# vim:syntax=python
#

import os,sys,site,json
from stat import S_ISDIR
import os.path as p

class localconf(object):

 def __init__(self, name="env.json"):
  localpath = p.dirname(p.realpath(__file__))
  sys.path.append(localpath)
  os.chdir(localpath)

  f = open(name)

  j = json.load(f)

  self.name = j["name"]
  self.settings = j["settings"]
  self.env = j["env"]

 def application(self):
  '''return a WSGI application'''

  mode = os.stat(self.env).st_mode

  if (S_ISDIR(mode)):
   site.addsitedir(self.env)

  settings = self.settings
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

  # this to be done only after environment is setup correctly
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()

  return application


conf = localconf()

application = conf.application()



## EOF ##
