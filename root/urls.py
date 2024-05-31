from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from root.settings import STATIC_URL, STATIC_ROOT, MEDIA_ROOT, MEDIA_URL

schema_view = get_schema_view(
    openapi.Info(
        title="P19 group API",
        default_version='v1',
        description="nimadir yozamiz!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),
                  path("admin/", admin.site.urls),
                  path("api/v1/", include('apps.urls')),
                  path('api/v1/', include('rest_framework.urls')),
                  path("__debug__/", include("debug_toolbar.urls")),

              ] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)