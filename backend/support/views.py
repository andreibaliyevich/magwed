from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Feedback, Report
from .serializers import FeedbackSerializer, ReportSerializer


class FeedbackCreateView(generics.CreateAPIView):
    """ Feedback Create View """
    permission_classes = [AllowAny]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class ReportCreateView(generics.CreateAPIView):
    """ Report Create View """
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
