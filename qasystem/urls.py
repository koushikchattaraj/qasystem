from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include("accounts.urls")),
    path('', include("questions.urls")),
    path('', include("accounts.urls")),
    path('', include("answers.urls")),
    path('', include("votes.urls")),
    path('', include("drive.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)