from django.urls import path
from .views import SurvivalPredictionView

urlpatterns = [
    path('predict-survival/', SurvivalPredictionView.as_view(), name='predict-survival'),
]
