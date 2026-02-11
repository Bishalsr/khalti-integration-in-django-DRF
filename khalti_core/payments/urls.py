from django.urls import path
from .views import KhaltiInitiateAPIView, KhaltiLookupAPIView,khalti_return_view

urlpatterns = [
    path("khalti/initiate/", KhaltiInitiateAPIView.as_view()),
    path("khalti/lookup/", KhaltiLookupAPIView.as_view()),
    path("khalti/return/", khalti_return_view),
]
