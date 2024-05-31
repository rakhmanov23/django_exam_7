from django.urls import path

from apps.views import VacancyListCreateAPIView, VacancyRetrieveUpdateDestroyAPIView, SendVerificationCode, \
    CheckVerificationCode

# from apps.views import ProductListAPIView, CategoryListCreateAPIView

urlpatterns = [
    path('vacancy', VacancyListCreateAPIView.as_view(), name='vacancy_update'),
    path('vacancy<int:pk>', VacancyRetrieveUpdateDestroyAPIView.as_view(), name='vacancy_list'),
    path('send_code', SendVerificationCode.as_view(), name='login'),
    path('login', CheckVerificationCode.as_view(), name='login'),
]