from django.urls import path

from main.apps import MainConfig
from main.views import (AdvertisementCreateAPIView, AdvertisementListAPIView, AdvertisementRetrieveAPIView,
                        AdvertisementUpdateAPIView, ReviewUpdateAPIView, ReviewCreateAPIView,
                        ReviewListAPIView, ReviewDestroyAPIView, AdvertisementDestroyAPIView, ReviewRetrieveAPIView)

app_name = MainConfig.name

urlpatterns = [
    path("ads/new/", AdvertisementCreateAPIView.as_view(), name="ads-create"),
    path("ads/<int:pk>/reviews/", ReviewListAPIView.as_view(), name="ads-review-list"),
    path("ads/", AdvertisementListAPIView.as_view(), name="ads-list"),
    path("ads/<int:pk>/", AdvertisementRetrieveAPIView.as_view(), name="ads-detail"),
    path("ads/<int:pk>/update/", AdvertisementUpdateAPIView.as_view(), name="ads-update"),
    path("ads/<int:pk>/delete/", AdvertisementDestroyAPIView.as_view(), name="ads-delete"),
    path("review/<int:pk>/", ReviewRetrieveAPIView.as_view(), name="review-detail"),
    path("ads/<int:pk>/review/create/", ReviewCreateAPIView.as_view(), name="review-create"),
    path("review/<int:pk>/update/", ReviewUpdateAPIView.as_view(), name="review-update"),
    path("review/<int:pk>/delete/", ReviewDestroyAPIView.as_view(), name="review-delete"),
]
