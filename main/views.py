from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from main.models import Advertisement, Review
from main.paginators import AdsPaginator
from main.serializers import AdvertisementSerializer, ReviewSerializer

from users.permissions import IsAdmin, IsAuthor


class AdvertisementListAPIView(ListAPIView):
    """ Список объявлений. """
    queryset = Advertisement.objects.all()
    pagination_class = AdsPaginator
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)


class ReviewListAPIView(ListAPIView):
    """ Список отзывов. """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Review.objects.filter(ads=self.kwargs['pk'])
        return queryset


class ReviewRetrieveAPIView(RetrieveAPIView):
    """ Получение отдельного отзыва. """
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer


class AdvertisementRetrieveAPIView(RetrieveAPIView):
    """ Получение отдельного объявления. """
    queryset = Advertisement.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AdvertisementSerializer


class ReviewCreateAPIView(CreateAPIView):
    """ Создание отзыва. """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        ads = Advertisement.objects.filter(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, ads=ads.get(pk=self.kwargs['pk']))


class AdvertisementCreateAPIView(CreateAPIView):
    """ Создание объявления. """
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewUpdateAPIView(RetrieveUpdateAPIView):
    """ Редактирование отзыва. """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthor | IsAdmin]
    queryset = Review.objects.all()

    def perform_update(self, serializer):
        review = Review.objects.get(pk=self.kwargs['pk'])
        serializer.save(review=review)


class AdvertisementUpdateAPIView(RetrieveUpdateAPIView):
    """ Редактирование объявления. """
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthor | IsAdmin]
    queryset = Advertisement.objects.all()


class ReviewDestroyAPIView(DestroyAPIView):
    """ Удаление отзыва. """
    queryset = Review.objects.all()
    permission_classes = [IsAuthor | IsAdmin]


class AdvertisementDestroyAPIView(DestroyAPIView):
    """ Удаление объявления. """
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthor | IsAdmin]
