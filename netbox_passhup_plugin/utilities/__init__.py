"""Utilities init"""

import base64
import os

# pylint: disable=C0301
webhooks = [
    {
        "name": "[VM] Create Host-Simple",
        "app_label": "virtualization",
        "content_types": "virtualmachine",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": f"{os.getenv("VM_AGENT_BASE_URL")}/api/createvm",
        "ssl_verification": False,
        "body_template": base64.b64decode(os.getenv("VM_AGENT_BODY_TEMPLATE")).decode(),
    }
]


# pylint: disable=W0613
def create_webhook(app_config, **kwargs):
    """Create automatically plugin webhook"""
    if app_config.label == "virtualization":
        # pylint: disable=C0415
        from django.contrib.contenttypes.models import ContentType
        from extras.models import Webhook

        if "eventrule" in app_config.apps.all_models["extras"]:
            # pylint: disable=E0611
            from extras.models import EventRule

            wh_content_type = ContentType.objects.get(
                app_label="extras", model="webhook"
            )

            for webhook in webhooks:
                results = Webhook.objects.filter(name=webhook["name"])
                if len(results) == 0:
                    obj = Webhook(
                        name=webhook["name"],
                        description="Added automatically by the Netbox Passhup Plugin",
                        http_method=webhook["http_method"],
                        payload_url=webhook["payload_url"],
                        ssl_verification=webhook["ssl_verification"],
                        body_template=webhook["body_template"],
                    )
                    obj.save()

                    event_types = []

                    if webhook["type_create"]:
                        event_types.append("object_created")

                    if webhook["type_update"]:
                        event_types.append("object_updated")

                    if webhook["type_delete"]:
                        event_types.append("object_deleted")

                    if webhook["type_job_start"]:
                        event_types.append("job_started")

                    if webhook["type_job_end"]:
                        event_types.append("job_completed")

                    eventrule = EventRule(
                        name=webhook["name"],
                        description="Added automatically by the Netbox Passhup Plugin",
                        event_types=event_types,
                        action_object_id=obj.pk,
                        action_object_type=wh_content_type,
                    )
                    eventrule.save()

                    obj_content_type = ContentType.objects.get(
                        app_label=webhook["app_label"], model=webhook["content_types"]
                    )

                    print(obj_content_type.pk)

                    # pylint: disable=E1101
                    eventrule.object_types.set([obj_content_type.pk])
                    eventrule.save()

            return
