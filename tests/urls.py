from django.urls import path, include

urlpatterns = [
    path('', include('bi.urls', namespace='bi')),
    path('accounts/', include('django.contrib.auth.urls')),
]
