from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Glovo",
        default_version='v1',),
    public=True,
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('glovo.urls')) ,
    path('accounts/', include('allauth.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
