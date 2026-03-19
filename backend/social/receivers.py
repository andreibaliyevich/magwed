from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Favorite


@receiver(pre_delete, sender=Article)
def article_deleting(sender, instance, **kwargs):
    """ Delete favorites of article """
    favorites = Favorite.objects.filter(
        content_type=ContentType.objects.get_for_model(Article),
        object_uuid=instance.uuid,
    ).delete()


@receiver(pre_delete, sender=Album)
def album_deleting(sender, instance, **kwargs):
    """ Delete favorites of album """
    favorites = Favorite.objects.filter(
        content_type=ContentType.objects.get_for_model(Album),
        object_uuid=instance.uuid,
    ).delete()


@receiver(pre_delete, sender=Photo)
def photo_deleting(sender, instance, **kwargs):
    """ Delete favorites of photo """
    favorites = Favorite.objects.filter(
        content_type=ContentType.objects.get_for_model(Photo),
        object_uuid=instance.uuid,
    ).delete()
