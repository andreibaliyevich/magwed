from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from portfolio.models import Album, Photo


class Command(BaseCommand):
    """
    Calculates the rating of photos and albums.
    python manage.py update_ratings
    python manage.py update_ratings --type albums
    python manage.py update_ratings --type photos
    """
    help = 'Updates the rating of photos, albums or all at once'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['all', 'albums', 'photos'],
            default='all',
            help='Type of objects to update: photos, albums, or all (default)',
        )

    def handle(self, *args, **options):
        update_type = options['type']
        now = timezone.now()

        if update_type in ['all', 'photos']:
            coefficients = {
                'views': 0.1,
                'likes': 0.25,
                'comments': 0.2,
                'favorites': 0.35,
                'time': 0.1,
            }

            photos = Photo.objects.annotate(
                like_count=Count("likes"),
                comment_count=Count("comments"),
                favorite_count=Count("favorites"),
            )

            # Finding the maximum values for normalization
            aggr_values = photos.aggregate(
                max_view_count=Max('view_count'),
                max_like_count=Max('like_count'),
                max_comment_count=Max('comment_count'),
                max_favorite_count=Max('favorite_count'),
                min_upload_date=Min('uploaded_at'),
            )
            max_upload_days = (now - aggr_values['min_upload_date']).days
            max_values = {
                'views': aggr_values['max_view_count'],
                'likes': aggr_values['max_like_count'],
                'comments': aggr_values['max_comment_count'],
                'favorites': aggr_values['max_favorite_count'],
                'upload_days': max_upload_days,
            }

            for photo in photos:
                # Normalization of values
                norm_views = photo.view_count / max_values['views'] if max_values['views'] else 0
                norm_likes = photo.like_count / max_values['likes'] if max_values['likes'] else 0
                norm_comments = photo.comment_count / max_values['comments'] if max_values['comments'] else 0
                norm_favorites = photo.favorite_count / max_values['favorites'] if max_values['favorites'] else 0
                since_upload_days = (now - photo.uploaded_at).days
                norm_time = 1 - (since_upload_days / max_values['upload_days']) if max_values['upload_days'] else 0

                # Calculating the rating
                photo.rating = ((coefficients['views'] * norm_views
                                 + coefficients['likes'] * norm_likes
                                 + coefficients['comments'] * norm_comments
                                 + coefficients['favorites'] * norm_favorites
                                 + coefficients['time'] * norm_time
                                 ) * 100)
                photo.save(update_fields=['rating'])
            self.stdout.write(f'Rating updated for {photos.count()} photos.')

        if update_type in ['all', 'albums']:
            coefficients = {
                'views': 0.1,
                'likes': 0.2,
                'comments': 0.15,
                'favorites': 0.3,
                'time': 0.1,
                'photo_rating': 0.15,
            }

            albums = Album.objects.annotate(
                like_count=Count("likes"),
                comment_count=Count("comments"),
                favorite_count=Count("favorites"),
                photo_rating_avg=Avg("photos__rating"),
            )

            # Finding the maximum values for normalization
            aggr_values = albums.aggregate(
                max_view_count=Max('view_count'),
                max_like_count=Max('like_count'),
                max_comment_count=Max('comment_count'),
                max_favorite_count=Max('favorite_count'),
                min_create_date=Min('created_at'),
                max_photo_rating_avg=Max('photo_rating_avg'),
            )
            max_create_days = (now - aggr_values['min_create_date']).days
            max_values = {
                'views': aggr_values['max_view_count'],
                'likes': aggr_values['max_like_count'],
                'comments': aggr_values['max_comment_count'],
                'favorites': aggr_values['max_favorite_count'],
                'create_days': max_create_days,
                'photo_rating': aggr_values['max_photo_rating_avg'],
            }

            for album in albums:
                # Normalization of values
                norm_views = album.view_count / max_values['views'] if max_values['views'] else 0
                norm_likes = album.like_count / max_values['likes'] if max_values['likes'] else 0
                norm_comments = album.comment_count / max_values['comments'] if max_values['comments'] else 0
                norm_favorites = album.favorite_count / max_values['favorites'] if max_values['favorites'] else 0
                since_create_days = (now - album.created_at).days
                norm_time = 1 - (since_create_days / max_values['create_days']) if max_values['create_days'] else 0
                norm_photo_rating = album.photo_rating_avg / max_values['photo_rating'] if max_values['photo_rating'] else 0

                # Calculating the rating
                album.rating = ((coefficients['views'] * norm_views
                                 + coefficients['likes'] * norm_likes
                                 + coefficients['comments'] * norm_comments
                                 + coefficients['favorites'] * norm_favorites
                                 + coefficients['time'] * norm_time
                                 + coefficients['photo_rating'] * norm_photo_rating
                                 ) * 100)
                album.save(update_fields=['rating'])
            self.stdout.write(f'Rating updated for {albums.count()} albums.')
