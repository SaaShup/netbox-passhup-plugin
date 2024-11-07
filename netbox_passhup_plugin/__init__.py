"""Netbox Plugin Configuration"""

from django.db.models.signals import post_migrate
from netbox.plugins import PluginConfig
from .utilities import create_webhook


class NetBoxPasshupConfig(PluginConfig):
    """Plugin Config Class"""

    name = "netbox_passhup_plugin"
    verbose_name = " NetBox Passhup Plugin"
    description = "Manage Passhup Netbox distribution initialization and behaviours."
    version = "0.0.1"
    base_url = "passhup"
    min_version = "4.1.0"
    author = "Vincent Simonin <vincent@saashup.com>"
    author_email = "vincent@saashup.com"

    def ready(self):
        post_migrate.connect(create_webhook)

        super().ready()


# pylint: disable=C0103
config = NetBoxPasshupConfig
