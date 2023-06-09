from django.contrib import admin

from testing.models import IQTest, Letter, TestLogin, LetterEQTest, EQTest


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
    )


@admin.register(LetterEQTest)
class LetterEQTestAdmin(admin.ModelAdmin):
    list_display = (
        'letter',
        'eq_test',
        'index'
    )


@admin.register(TestLogin)
class TestLoginAdmin(admin.ModelAdmin):
    list_display = (
        'login',
        'get_iqtest',
        'get_eqtest'
    )


@admin.register(EQTest)
class EQTestAdmin(admin.ModelAdmin):
    list_display = (
        'login',
        'created_at',
    )


@admin.register(IQTest)
class IQTestAdmin(admin.ModelAdmin):
    list_display = (
        'login',
        'point'
    )
