from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # ✅ Serve manifest, favicon, logos from static directly
    re_path(r'^(favicon\.ico|manifest\.json|logo192\.png|logo512\.png)$',
            serve, {'document_root': settings.STATIC_ROOT}),
    
    # ✅ React app catch-all (keep this LAST)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
