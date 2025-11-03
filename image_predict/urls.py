from django.urls import path
from .views import ImagePredictionView

urlpatterns = [
    path('', ImagePredictionView.as_view(), name='image_predict'),
]
