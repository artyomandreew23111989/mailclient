from django.db.models.signals import post_save
from django.dispatch import receiver
from mailapp.models import Email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Email)
def email_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'emails',
            {
                'type': 'email_created',
                'email': {
                    'to': instance.to,
                    'subject': instance.subject,
                    'body': instance.body,
                    'sent_at': instance.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )
