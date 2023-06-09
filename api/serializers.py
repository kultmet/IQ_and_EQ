from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator
)

from api.validators import check_test_exists, regex_validator, set_validation
from testing.models import Letter, TestLogin, IQTest, EQTest, LetterEQTest


class CreateTestLoginSerializer(serializers.ModelSerializer):
    login = serializers.CharField(required=False)

    class Meta:
        model = TestLogin
        fields = ('login',)


class CreateIQSerializer(serializers.ModelSerializer):
    login = serializers.CharField(required=True)
    point = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(0, 'Меньше чем 0 не бывает!!'),
            MaxValueValidator(50, 'Больше чем 50 не бывает!')
        ]
    )

    class Meta:
        model = IQTest
        fields = ('login', 'point',)

    def validate(self, data):
        check_test_exists(IQTest, data.get('login'), 'IQ')
        return data

    def create(self, validated_data):
        login_test = get_object_or_404(
            TestLogin, login=validated_data['login']
        )
        iq_test = IQTest.objects.create(
            login=login_test, point=validated_data['point']
        )
        return iq_test


class CreateEQSerializer(serializers.ModelSerializer):
    login = serializers.CharField(required=True, write_only=True)
    letters = serializers.ListField(
        required=True,
        write_only=True,
        validators=[
            MinLengthValidator(5, 'Слишком мало букв!'),
            MaxLengthValidator(5, 'Слишком много букв!')
        ]
    )

    class Meta:
        model = EQTest
        fields = ('login', 'letters')

    def validate(self, data: dict):
        set_validation(data.get('letters'))
        try:
            regex_validator(''.join(data.get('letters')))
        except TypeError:
            raise ValidationError(
                {
                    'letters':
                    'Проверте корректность введенных данных. '
                    'Элементы списка должны иметь тип str (String)'
                }
            )
        check_test_exists(EQTest, data.get('login'), 'EQ')
        return data

    def create(self, validated_data):
        login_test = get_object_or_404(
            TestLogin, login=validated_data['login']
        )
        letters = validated_data.pop('letters')
        eq_test = EQTest.objects.create(login=login_test)
        letter_eq_objs = [
            LetterEQTest(
                letter=Letter.objects.get(
                    symbol=symbol
                ), eq_test=eq_test, index=index
            ) for index, symbol in enumerate(letters, 1)
        ]
        LetterEQTest.objects.bulk_create(
            objs=letter_eq_objs,
            batch_size=len(letter_eq_objs)
        )
        return eq_test

    def to_representation(self, instance):
        return {'message': 'Сохранен успешно'}


class ReadIQSerializer(serializers.ModelSerializer):
    class Meta:
        model = IQTest
        fields = ('point', 'created_at')


class ReadEQSerializer(serializers.ModelSerializer):
    letters = serializers.SerializerMethodField('get_letters')

    class Meta:
        model = EQTest
        fields = ('letters', 'created_at')

    def get_letters(self, obj):
        return [i.get('symbol') for i in obj.letters.values('symbol')]


class RetrieveTestSerializer(serializers.ModelSerializer):
    iq = ReadIQSerializer(source='iqtests')
    eq = ReadEQSerializer(source='eqtests')

    class Meta:
        model = TestLogin
        fields = ('login', 'iq', 'eq')
        lookup_field = 'login'
        extra_kwargs = {
            'url': {'lookup_field': 'login'}
        }
