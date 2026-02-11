# feature_flags_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from features.views import FeatureFlagViewSet

router = DefaultRouter()
router.register(r'features', FeatureFlagViewSet, basename='features')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(
        template_name='features_dashboard/index.html'
    ), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'feature_flags_project' / 'static'
    )
