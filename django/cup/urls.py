from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from cup import views

app_name = 'cup'

urlpatterns = [
    path('img_upload/', views.img_upload, name='img_upload'),
    path('predict/', views.pred_img, name='pred_img'),
    path('detect_text/<str:file_name>/', views.detect_img_text, name='detect_img_text'),
    path('delete/<str:file_name>', views.delete, name='delete')
]
