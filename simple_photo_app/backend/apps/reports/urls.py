from django.urls import path
from .views import index_view, PhotoListCreateView, PhotoZipDownloadView, PhotoDestroyView, photos_exist_view
from .views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('photos/', PhotoListCreateView.as_view(), name='photo-list-create'),
    path('photos/zip/', PhotoZipDownloadView.as_view(), name='photo-zip'),
    path('photos/<int:pk>/', PhotoDestroyView.as_view(), name='photo-destroy'),
    path('photos/exists/', photos_exist_view, name='photo-exists'),  # 追加
]

urlpatterns += [
    path('photos/<int:pk>/', PhotoDestroyView.as_view(), name='photo-destroy'),
]