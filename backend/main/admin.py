from django.contrib import admin
from .models import Currency, Country, City, Language, Tag, Magazine


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """ Currency Model for admin """
    list_display = ('__str__', 'conversion_rate')
    list_editable = ('conversion_rate',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """ Country Model for admin """
    list_display = ('__str__',)
    search_fields = ('code',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """ City Model for admin """
    list_display = ('__str__',)
    list_filter = ('country',)
    search_fields = ('code',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """ Language Model for admin """
    list_display = ('__str__',)
    search_fields = ('code',)


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    """ Magazine Model for admin """
    list_display = ('__str__', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Tag Model for admin """
    list_display = ('__str__', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
