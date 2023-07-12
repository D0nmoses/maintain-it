from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'devices'

urlpatterns=[
    path('', views.home_view, name='home'),
    re_path(r'^profile/(\d+)', views.profile, name="profile"),
    path('records/', views.MaintenanceRecordListView.as_view(), name='maintenance_record_list'),
    path('records/<int:id>/', views.MaintenanceRecordDetailView.as_view(), name='maintenance_record_detail'),
    path('documentation/', views.DocumentationRecordListView.as_view(), name='documentation_record_list'),
    path('documentation/<int:id>/', views.DocumentationRecordDetailView.as_view(), name='documentation_record_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)