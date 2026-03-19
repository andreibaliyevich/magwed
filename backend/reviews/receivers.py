from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_organizer_rating(sender, **kwargs):
    """ Update rating of organizer """
    user = kwargs['instance'].user
    user_rating = user.user_reviews.aggregate(
        total_rating=Coalesce(Avg('rating'), Value(0.0)))
    user.organizer.rating = user_rating['total_rating']
    user.organizer.save(update_fields=['rating'])
