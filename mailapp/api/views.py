from rest_framework import generics
from mailapp.models import Email
from mailapp.api.serializers import EmailSerializer

class EmailListCreateAPIView(generics.ListCreateAPIView):
    queryset = Email.objects.order_by('-sent_at')
    serializer_class = EmailSerializer
