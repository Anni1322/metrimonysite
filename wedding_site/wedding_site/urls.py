
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
from biodata import views as biodata_views

urlpatterns = [
    path('', RedirectView.as_view(url='biodata/', permanent=False)),
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    path('matrimony/', include('matrimony.urls')),
    path('weddings/', include('weddings.urls')),
    path('biodata/', include('biodata.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
