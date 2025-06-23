from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse

from users.models import User
from main.models import Advertisement, Review


class AdvertisementTestCase(APITestCase):
    """ Тестирование модели объявлений. """

    def setUp(self):
        """ Настройка тестового окружения. """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='testuser@user.ru', password=make_password('testpassword'), is_active=True, first_name='testuser')
        self.token_url = reverse('users:token_obtain_pair')
        self.protected_url = '/users/protected/'
        self.advertisement = Advertisement.objects.create(
            pk=1,
            author=self.user,
            title="title",
            description="description",
            price=1000
        )
        self.user2 = User.objects.create(
            email="user2@user2.ru", password=make_password("testpassword"), first_name='user2'
        )
        self.user_admin = User.objects.create(
            email="user3@user.ru", password=make_password("testpassword"), first_name='user3', user_role="Администратор"
        )
        self.advertisement2 = Advertisement.objects.create(
            pk=2,
            author=self.user2,
            title="title2",
            description="description2",
            price=2000
        )

    def test_create_advertisement(self):
        """ Тестирование создания объявления. """
        self.client.force_authenticate(user=self.user)
        url = reverse("main:ads-create")
        body = {
            "pk": 3,
            "title": "title",
            "description": "description",
            "price": 1000,
        }
        request = self.client.post(url, body, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 3)

    def test_blocked_word_in_advertisement_title(self):
        """ Тестирование валидации в названии объявления. """
        self.client.force_authenticate(user=self.user)
        url = reverse("main:ads-create")
        body = {
            "pk": 3,
            "title": "Полиция",
            "description": "description",
            "price": 1000,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Advertisement.objects.count(), 2)
        self.assertEqual(response.get('non_field_errors'), ['В названии присутсвует запрещенное слово: полиция'], )

    def test_blocked_word_in_advertisement_description(self):
        """ Тестирование валидации в описании объявления. """
        self.client.force_authenticate(user=self.user)
        url = reverse("main:ads-create")
        body = {
            "pk": 3,
            "title": "title",
            "description": "Полиция",
            "price": 1000,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Advertisement.objects.count(), 2)
        self.assertEqual(response.get('non_field_errors'), ['В описании присутсвует запрещенное слово: полиция'], )

    def test_negative_value_in_advertisement_price(self):
        """ Тестирование валидации цены объявления. """
        self.client.force_authenticate(user=self.user)
        url = reverse("main:ads-create")
        body = {
            "pk": 3,
            "title": "title",
            "description": "Полиция",
            "price": 1000,
        }
        request = self.client.post(url, body, format="json")
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Advertisement.objects.count(), 2)

    def test_advertisement_author(self):
        """ Тестирование создания объявления на соответствие автора и текущего пользователя. """
        self.client.force_authenticate(user=self.user)
        url = reverse("main:ads-create")
        body = {
            "pk": 3,
            "title": "title",
            "description": "description",
            "price": 1000,
        }

        request = self.client.post(url, body, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 3)
        self.assertEqual(Advertisement.objects.first().author, self.user)

    def test_update_advertisement(self):
        """ Тестирование эндпойнта обновления объявления. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'testuser@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))

        url = reverse("main:ads-update", kwargs={"pk": self.advertisement.pk})
        body = {
            "title": "title3",
            "description": "description2",
            "price": 1500,
        }
        self.client.force_authenticate(user=self.user, token=token)
        request = self.client.patch(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Advertisement.objects.count(), 2)

    def test_delete_advertisement(self):
        """ Тестирование эндпойнта удаления объявления. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'testuser@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))

        url = reverse("main:ads-delete", kwargs={"pk": self.advertisement.pk})

        self.client.force_authenticate(user=self.user, token=token)
        request = self.client.delete(url, format="json")
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Advertisement.objects.count(), 1)

    def test_retrieve_advertisement_without_authorization(self):
        """ Тестирование ограничения доступа к отдельным объявлениям неавторизованным пользователям. """
        url = reverse("main:ads-detail", kwargs={"pk": self.advertisement2.pk})
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_advertisement_not_being_an_author(self):
        """ Тестирование ограничения прав редактирования объявлений пользователям, не являющимся автором объявления. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'testuser@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user, token=token)

        url = reverse("main:ads-update", kwargs={"pk": self.advertisement2.pk})
        body = {
            "title": "title3",
            "description": "description2",
            "price": 1500,
        }

        request = self.client.patch(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_advertisement_not_being_an_author(self):
        """ Тестирование ограничения прав удаления объявлений пользователям, не являющимся автором объявления. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'testuser@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))

        url = reverse("main:ads-delete", kwargs={"pk": self.advertisement2.pk})

        self.client.force_authenticate(user=self.user, token=token)
        request = self.client.delete(url, format="json")
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Advertisement.objects.count(), 2)

    def test_update_advertisement_with_admin_status(self):
        """ Тестирование доступа к редактированияю чужих объявлений пользователям, имеющим статус Администратора. """

        auth = self.client.post(
            self.token_url,
            {
                'email': 'user3@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user_admin, token=token)

        url = reverse("main:ads-update", kwargs={"pk": self.advertisement2.pk})
        body = {
            "title": "title3",
            "description": "description2",
            "price": 1500,
        }

        request = self.client.patch(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_advertisement_with_admin_status(self):
        """ Тестирование доступа к удалению чужих объявлений пользователям, имеющим статус Администратора. """

        auth = self.client.post(
            self.token_url,
            {
                'email': 'user3@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user_admin, token=token)

        url = reverse("main:ads-delete", kwargs={"pk": self.advertisement2.pk})

        request = self.client.delete(url, format="json")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Advertisement.objects.count(), 1)


class ReviewTestCase(APITestCase):
    """ Тестирование отзывов."""
    def setUp(self):
        """ Настройка окружения."""
        self.factory = APIRequestFactory()
        self.token_url = reverse('users:token_obtain_pair')
        self.user = User.objects.create(
            email="user@user.ru", password=make_password('testpassword'), is_active=True, first_name='testuser'
        )
        self.advertisement = Advertisement.objects.create(
            pk=1,
            author=self.user,
            title="title",
            description="description",
            price=1000,
        )
        self.user2 = User.objects.create(
            email="user2@user2.ru", password=make_password('testpassword'), is_active=True, first_name='testuser2'
        )
        self.advertisement2 = Advertisement.objects.create(
            pk=2,
            author=self.user2,
            title="title2",
            description="description2",
            price=2000,
        )
        self.review = Review.objects.create(
            pk=1,
            author=self.user,
            content='content',
            ads=self.advertisement,
        )
        self.review2 = Review.objects.create(
            pk=2,
            author=self.user2,
            content='content2',
            ads=self.advertisement2,
        )
        self.user_admin = User.objects.create(
            email="user3@user.ru", password=make_password("testpassword"), first_name='user3', user_role="Администратор"
        )

    def test_create_review(self):
        """ Тестирование создания отзыва. """
        self.client.force_authenticate(user=self.user)
        ads = Advertisement.objects.get(pk=self.advertisement.pk)
        url = reverse("main:review-create", kwargs={"pk": ads.pk})
        body = {
            "pk": 3,
            "content": "content4",
        }

        request = self.client.post(url, body, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)

    def test_blocked_word_in_review(self):
        """ Тестирование валидации отзыва. """
        self.client.force_authenticate(user=self.user)
        ads = Advertisement.objects.get(pk=self.advertisement.pk)
        url = reverse("main:review-create", kwargs={"pk": ads.pk})
        body = {
            "pk": 3,
            "content": "Полиция",
        }

        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(response.get('non_field_errors'), ['В комментарии присутсвует запрещенное слово: полиция'], )

    def test_review_author(self):
        """ Тестирование создания отзыва на соответствие автора и текущего пользователя. """
        self.client.force_authenticate(user=self.user)
        ads = Advertisement.objects.get(pk=self.advertisement.pk)
        url = reverse("main:review-create", kwargs={"pk": ads.pk})
        body = {
            "pk": 3,
            "content": "content4",
        }

        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)
        self.assertEqual(Review.objects.first().author, self.user)

    def test_update_review(self):
        """ Тестирование обновленипя отзыва. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'user@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user, token=token)

        url = reverse("main:review-update", kwargs={"pk": self.review.pk})
        body = {
            "pk": 1,
            "content": "content1",
        }

        request = self.client.patch(url, body, format="json")
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        """ Тестирование удаления отзыва. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'user@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user, token=token)

        url = reverse("main:review-delete", kwargs={"pk": self.review.pk})
        request = self.client.delete(url, format="json")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1)

    def test_retrieve_review_without_auth(self):
        """ Тестирование ограничения доступа к отзыву неавторизованным пользователям. """
        url = reverse("main:review-detail", kwargs={"pk": self.review.pk})
        request = self.client.get(url)

        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review_not_author(self):
        """ Тестирование ограничения прав редактирования отзыва пользователям, не являющимся автором. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'user2@user2.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user2, token=token)

        url = reverse("main:review-update", kwargs={"pk": self.review.pk})
        body = {
            "pk": 1,
            "content": "content1",
        }

        request = self.client.patch(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_not_author(self):
        """ Тестирование ограничения прав удаления отзывов пользователям, не являющимся автором. """
        auth = self.client.post(
            self.token_url,
            {
                'email': 'user2@user2.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user2, token=token)

        url = reverse("main:review-delete", kwargs={"pk": self.review.pk})
        request = self.client.delete(url, format="json")

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 2)

    def test_update_review_with_admin_status(self):
        """ Тестирование доступа к редактированияю чужих отзывов пользователям, имеющим статус Администратора. """

        auth = self.client.post(
            self.token_url,
            {
                'email': 'user3@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user_admin, token=token)

        url = reverse("main:review-update", kwargs={"pk": self.review.pk})

        body = {
            "pk": 1,
            "content": "content12",
        }

        request = self.client.patch(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_review_with_admin_status(self):
        """ Тестирование доступа к удалению чужих отзывов пользователям, имеющим статус Администратора. """

        auth = self.client.post(
            self.token_url,
            {
                'email': 'user3@user.ru',
                'password': 'testpassword',
            },
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.client.force_authenticate(user=self.user_admin, token=token)

        url = reverse("main:review-delete", kwargs={"pk": self.review.pk})

        request = self.client.delete(url, format="json")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1)
