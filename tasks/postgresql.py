from __future__ import with_statement

from fabric.api import *
from fabric.contrib import django
from fabric.utils import warn

import os.path
import settings as django_settings

from helpers import yes_or_no_input

django.settings_module("settings")

DB_NAME     = django_settings.DATABASES['default']['NAME']
DB_USER     = django_settings.DATABASES['default']['USER']
DB_PASSWORD = django_settings.DATABASES['default']['PASSWORD'] 

POSTGRES_ADMIN_USER = "postgres"

# Commands to set up database

@task
def create_db(name, user):
  sudo("createdb %s -E UTF-8 -O %s" % (name, user), user=POSTGRES_ADMIN_USER)

@task
def drop_db(name):
  if yes_or_no_input("Are you sure you want to drop the database %s?" % name):
    sudo("dropdb %s" % name, user=POSTGRES_ADMIN_USER)
  else:
    print "Skipping drop"
    return False
  
@task
def drop_user(user):
  if yes_or_no_input("Are you sure you want to drop the user %s?" % user):
    sudo('psql -c "DROP USER %s"' % (user), user=POSTGRES_ADMIN_USER)
  else:
    print "Skipping drop"
    return False

@task
def create_user(user, password):
  sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER \
                 ENCRYPTED PASSWORD E\'%s\'"' % (user, password), user=POSTGRES_ADMIN_USER)

@task
def reset():
  drop_db(name=DB_NAME)
  drop_user(user=DB_USER)
  create_user(user=DB_USER, password=DB_PASSWORD)
  create_db(name=DB_NAME, user=DB_USER)

  local("./manage.py syncdb --noinput")

@task
def create():
  create_user(user=DB_USER, password=DB_PASSWORD)
  create_db(name=DB_NAME, user=DB_USER)

@task
def export(filename=None):
  if not filename:
    filename = "%s.sql" % DB_NAME

  if os.path.isfile(filename) and not yes_or_no_input("That file already exists. Overwrite?"):
    print "Aborting..."
    return
  else:
    print "Exporting %s to %s" % (DB_NAME, filename)
    sudo("pg_dumpall -f %s -c %s" % (filename, DB_NAME), user=POSTGRES_ADMIN_USER)
