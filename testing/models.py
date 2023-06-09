from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


from string import ascii_lowercase, ascii_uppercase
from random import choices


LETTER_CHOICE = (
    ('а', 'а'),
    ('б', 'б'),
    ('в', 'в'),
    ('г', 'г'),
    ('д', 'д')
)


class TestLogin(models.Model):
    login = models.CharField(verbose_name='Логин', max_length=10)

    def save(self, *args, **kwargs):
        letters_and_digits = ascii_lowercase + ascii_uppercase
        self.login = ''.join(choices(letters_and_digits, k=10))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.login

    def get_iqtest(self):
        return IQTest.objects.get(login=self)

    def get_eqtest(self):
        return [
            i.get('symbol') for i in EQTest.objects.get(
                login=self
            ).letters.values('symbol')
        ]


class CommonTest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IQTest(CommonTest):
    login = models.OneToOneField(
        TestLogin,
        related_name='iqtests',
        on_delete=models.CASCADE
    )
    point = models.IntegerField(
        'Баллы',
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0, 'Меньше чем 0 не бывает!!'),
            MaxValueValidator(50, 'Больше чем 50 не бывает!')
        ]
    )


class EQTest(CommonTest):
    login = models.OneToOneField(
        TestLogin,
        related_name='eqtests',
        on_delete=models.CASCADE,
        unique=True
    )
    letters = models.ManyToManyField('Letter', through='LetterEQTest')


class Letter(models.Model):
    symbol = models.CharField(
        verbose_name='Буква', max_length=1, choices=LETTER_CHOICE, unique=True
    )

    def __str__(self) -> str:
        return self.symbol


class LetterEQTest(models.Model):
    eq_test = models.ForeignKey(EQTest, on_delete=models.CASCADE)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер', default=1
    )

    class Meta:
        ordering = ['index']
