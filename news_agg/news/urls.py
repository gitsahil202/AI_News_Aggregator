from django.urls import path
from .views import SummaryView
urlpatterns = [
    path('news/',SummaryView.as_view(),name="News")
]
