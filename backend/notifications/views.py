from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .pagination import NotificationPagination
from .serializers import NotificationListSerializer


class NotificationListView(generics.ListAPIView):
    """ Notification List View """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationListSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class NotViewedCountView(APIView):
    """ Not Viewed Count View """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        not_viewed_count = Notification.objects.filter(
            recipient=request.user,
            viewed=False,
        ).count()
        return Response(not_viewed_count, status=status.HTTP_200_OK)


class NotificationListDestroyView(APIView):
    """ Notification List Destroy View """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
