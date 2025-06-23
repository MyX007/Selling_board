from rest_framework import serializers
from main.models import Advertisement, Review
from main.validators import AdvertisementValidator, ReviewValidator


class AdvertisementSerializer(serializers.ModelSerializer):
    """ Сериализатор объявления. """
    class Meta:
        model = Advertisement
        fields = "__all__"
        validators = [AdvertisementValidator()]


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор отзывов. """
    class Meta:
        model = Review
        fields = "__all__"
        validators = [ReviewValidator()]
