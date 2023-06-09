import re

from rest_framework.exceptions import ValidationError


def check_test_exists(model, login, name):
    if model.objects.filter(login__login=login).exists():
        raise ValidationError(f'{name} Тест уже пройден!')


def regex_validator(symbols):
    residue = re.sub(r'[а-д]+', '', symbols)
    if len(residue) > 0:
        suf = 'а' if len(residue) == 1 else 'ов'
        raise ValidationError(
            {
                'letters':
                f"Символ{suf} '{', '.join(residue)}' нет в наборе возможных!"
            }
        )


def set_validation(letters):
    if len(set(letters)) < len(letters):
        raise ValidationError(
            {'letters': 'Все символы должны быть уникальными!'}
        )
    return letters
