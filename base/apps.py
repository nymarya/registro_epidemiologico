from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    default_site = 'base.admin.MyAdminSite'


class BaseConfig(AppConfig):
    name = 'base'
