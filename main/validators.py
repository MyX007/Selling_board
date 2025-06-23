from rest_framework.serializers import ValidationError

from main.models import Advertisement, Review


block_words_list = ["Полиция", "Обман", "Наркотики", "Казино", "Оружие", "Криптовалюта", "Радар", "Крипта", "Бесплатно"]


class AdvertisementValidator:
    def validate_title(self, atttrs):
        for word in atttrs["title"].lower().split():
            for blocked_word in block_words_list:
                if word.lower() in blocked_word.lower():
                    raise ValidationError(f'В названии присутсвует запрещенное слово: {word}')

    def validate_description(self, atttrs):
        for word in atttrs["description"].lower().split():
            for blocked_word in block_words_list:
                if word.lower() in blocked_word.lower():
                    raise ValidationError(f'В описании присутсвует запрещенное слово: {word}')

    def __call__(self, attrs):
        self.validate_title(attrs)
        self.validate_description(attrs)


class ReviewValidator:
    def validate_content(self, atttrs):
        for word in atttrs["content"].lower().split():
            for blocked_word in block_words_list:
                if word.lower() in blocked_word.lower():
                    raise ValidationError(f'В комментарии присутсвует запрещенное слово: {word}')

    def __call__(self, attrs):
        self.validate_content(attrs)