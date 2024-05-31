import redis
import time
from random import randint

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.filters import VacancyFilter
from apps.models import Vacancy, User
from apps.serializers import VacancySerializer, VerificationCodeSerializer, EmailSerializer
from root import settings


class VacancyListCreateAPIView(ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VacancyFilter

    def get_object(self):
        return self.request.user


class VacancyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class SendVerificationCode(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def post(self, request):
        user_email = request.data.get('email')

        verification_code = randint(100000, 999999)

        subject = 'Hisob tasdiqlash kodi'
        message = f'Assalomu alaykum!\nSizning tasdiqlash kodingiz: {verification_code}'
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, [user_email])
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        redis_conn.set(user_email, verification_code)
        redis_conn.set(f"{user_email}:timestamp", int(time.time()))
        return Response('Verification code sent successfully')


class CheckVerificationCode(GenericAPIView):
    serializer_class = VerificationCodeSerializer

    def post(self, request):
        user_email = request.data.get('email')
        provided_code = request.data.get('code')

        if not user_email or not provided_code:
            return Response({'error': 'Email and verification code are required'},)

        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        stored_code = redis_conn.get(user_email)
        stored_timestamp = redis_conn.get(f"{user_email}:timestamp")

        if stored_code == provided_code:
            if stored_timestamp:
                current_timestamp = int(time.time())
                stored_timestamp = int(stored_timestamp.decode('utf-8'))
                if current_timestamp - stored_timestamp <= 60:
                    redis_conn.delete(user_email)
                    redis_conn.delete(f"{user_email}:timestamp")
                    return Response('Verification successful',)

            return Response('Verification code has expired',)
        else:
            return Response({'error': 'Invalid verification code'},)