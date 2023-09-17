from django.contrib import admin

from movies import models


class GenreFilmworkInline(admin.TabularInline):
    model = models.GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = models.PersonFilmwork


@admin.register(models.Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created', 'modified',)
    list_filter = ('type', 'genres', 'persons')
    search_fields = ('title', 'description', 'id')


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name',)
