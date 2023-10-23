from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from . import models

def _update_order(room):
    for idx, config in enumerate(room.configs.all(), 1):
        config.order = idx
        config.save()

@receiver(post_save, sender=models.Room)
def create_new_room_handler(sender, instance, created, **kwargs):
    if created:
        for idx, owner in enumerate(instance.participants.all(), 1):
            _ = models.Config.objects.create(room=instance, owner=owner, order=idx)

@receiver(m2m_changed, sender=models.Room.participants.through)
def update_assigned_user_handler(sender, instance, action, reverse, **kwargs):
    pk_set = kwargs.get('pk_set', None)

    if not reverse and pk_set is not None:
        pks = list(pk_set)

        if action == 'post_add':
            users = models.User.objects.filter(pk__in=pks)

            for owner in users:
                _ = models.Config.objects.get_or_create(room=instance, owner=owner)
            _update_order(instance)
        elif action == 'post_remove':
            queryset = models.Config.objects.filter(room=instance, owner__pk__in=pks)
            queryset.delete()
            _update_order(instance)